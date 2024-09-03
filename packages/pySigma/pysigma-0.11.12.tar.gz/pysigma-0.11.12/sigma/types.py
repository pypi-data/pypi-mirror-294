import re
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto
from ipaddress import IPv4Network, IPv6Network, ip_network
from math import inf
from typing import (
    ClassVar,
    Dict,
    Pattern,
    Set,
    Union,
    List,
    Tuple,
    Optional,
    Any,
    Iterable,
    Callable,
    Iterator,
)

from sigma.exceptions import (
    SigmaPlaceholderError,
    SigmaRuleLocation,
    SigmaValueError,
    SigmaRegularExpressionError,
    SigmaTypeError,
)


class SpecialChars(Enum):
    """Enumeration of supported special characters"""

    WILDCARD_MULTI = auto()
    WILDCARD_SINGLE = auto()


@dataclass
class Placeholder:
    """
    Placeholder class used as stub in a SigmaString to be later replaced by a value contained in a string or
    receives some configuration-specific special treatment, e.g. replacement with a SIEM specific list item.
    """

    name: str


escape_char = "\\"
char_mapping = {
    "*": SpecialChars.WILDCARD_MULTI,
    "?": SpecialChars.WILDCARD_SINGLE,
}
special_char_mapping = {v: k for k, v in char_mapping.items()}


class SigmaType(ABC):
    """Base class for Sigma value types"""

    def to_plain(self):
        """
        Return plain Python value (str, int etc.) from SigmaType instance for usage in conversion of
        Sigma rules back to dicts. Uses the first annotated member as return value.
        """
        return self.__getattribute__(list(self.__annotations__.keys())[0])


class NoPlainConversionMixin:
    """Mixin for declaring a SigmaType as non-convertible into a plain representation."""

    def to_plain(self):
        raise SigmaValueError(
            f"Sigma type '{ self.__class__.__name__ }' can't be converted into a plain representation."
        )


class SigmaNull(SigmaType):
    """Empty/none/null value"""

    null: ClassVar[None] = None

    def __init__(self, dummy: Optional[Any] = None):
        pass

    def __eq__(self, other: "SigmaNull") -> bool:
        return isinstance(other, self.__class__)


@dataclass
class SigmaExists(SigmaType):
    """Field existence check."""

    exists: bool

    def __bool__(self):
        return self.exists


class SigmaString(SigmaType):
    """
    Strings in Sigma detection values containing wildcards.
    """

    original: str  # the original string, untouched
    s: Tuple[
        Union[str, SpecialChars, Placeholder]
    ]  # the string is represented as sequence of strings and characters with special meaning

    def __init__(self, s: Optional[str] = None):
        """
        Initializes SigmaString instance from raw string by parsing it:

        * characters from char_mapping are interpreted as special characters and interrupt the plain string in the resulting sequence
        * escape_char disables special character mapping in the next character
        * if escaping character is followed by a character without special meaning the escaping character is used as plain character
        """
        if s is None:
            s = ""

        self.original = s

        r = list()
        acc = ""  # string accumulation until special character appears
        escaped = False  # escape mode flag: characters in this mode are always accumulated
        for c in s:
            if escaped:  # escaping mode?
                if (
                    c in char_mapping or c == escape_char
                ):  # accumulate if character is special or escaping character
                    acc += c
                else:  # accumulate escaping and current character (this allows to use plain backslashes in values)
                    acc += escape_char + c
                escaped = False
            elif c == escape_char:  # escaping character? enable escaped mode for next character
                escaped = True
            else:  # "normal" string parsing
                if c in char_mapping:  # character is special character?
                    if acc != "":
                        r.append(
                            acc
                        )  # append accumulated string to parsed result if there was something
                    r.append(char_mapping[c])  # append special character to parsed result
                    acc = ""  # accumulation reset
                else:  # characters without special meaning aren't accumulated
                    acc += c
        if escaped:  # String ended in escaping mode: accumulate escaping character
            acc += escape_char
        if acc != "":  # append accumulated remainder
            r.append(acc)
        self.s = tuple(r)

    @classmethod
    def from_str(cls, s: str) -> "SigmaString":
        sigma_string = SigmaString()
        sigma_string.s = (s,)
        sigma_string.original = s
        return sigma_string

    def __getitem__(self, idx: Union[int, slice]) -> "SigmaString":
        """
        Index SigmaString parts with transparent handling of special characters.

        :param key: Integer index or slice.
        :type key: Union[int, slice]
        :return: SigmaString containing only the specified part.
        :rtype: SigmaString
        """
        # Set start and end indices from given index
        length = len(self)
        if isinstance(idx, int):
            start = idx
            end = None
        elif isinstance(idx, slice):
            if idx.step is not None:
                raise IndexError("SigmaString slice index with step is not allowed")
            start = idx.start or 0
            end = idx.stop or inf
        else:
            raise TypeError("SigmaString indices must be integers or slices")

        # Handling of negative indices and deferred setting of end index if only character index was set
        if start < 0:
            start = length + start
        if end is None:
            end = start + 1
        elif end < 0:
            end = length + end

        # Range checks
        if start > end or start >= length:
            return SigmaString("")
        if start < 0 or end < 0 or (end != inf and end > length):
            raise IndexError("SigmaString index out of range")

        i = 0  # Pointer to SigmaString element
        result = []  # Result: indexed string part

        # Find start. The variables start and end now contain the remaining characters until the
        # indexed part begins/ends relative to the current element.
        while start > 0 and i < len(self.s):
            e = self.s[i]
            if isinstance(e, str):  # Current SigmaString part is string
                e_len = len(e)
                # if e_len <= start:
                if e_len > start:
                    # else:
                    if end < e_len:  # end lies within this string part
                        return SigmaString(e[start:end])
                    else:  # end lies behind the current string part
                        result.append(e[start:])
                        # end -= start
                        # start = 0
                start -= e_len
                end -= e_len
            else:  # Current SigmaString part is a special character or placeholder
                start -= 1
                end -= 1

            i += 1

        # Append until end of string or indexed part is reached.
        while end > 0 and i < len(self.s):
            e = self.s[i]
            if isinstance(e, str):  # Current SigmaString part is string
                e_len = len(e)
                if end < e_len:  # end lies within this string part
                    result.append(e[:end])
                else:
                    result.append(e)
                end -= e_len
            else:  # Current SigmaString part is a special character or placeholder
                result.append(e)
                end -= 1

            i += 1

        if len(result) == 0:  # Special case: start begins after string - return empty string
            return SigmaString("")
        else:  # Return calculated result
            s = SigmaString()
            s.s = tuple(result)
            return s

    def insert_placeholders(self) -> "SigmaString":
        """
        Replace %something% placeholders with Placeholder stub objects that can be later handled by the processing
        pipeline. This implements the expand modifier.
        """
        res = []
        for part in self.s:  # iterate over all parts and...
            if isinstance(part, str):  # ...search in strings...
                lastpos = 0
                for m in re.finditer("(?<!\\\\)%(?P<name>\\w+)%", part):  # ...for placeholders
                    s = part[lastpos : m.start()].replace("\\%", "%")
                    if s != "":
                        res.append(
                            s
                        )  # append everything until placeholder (if not empty) as string part to new string
                    res.append(
                        Placeholder(m["name"])
                    )  # insert placeholder stub at position of placeholder
                    lastpos = m.end()
                s = part[lastpos:].replace("\\%", "%")
                if s != "":
                    res.append(
                        s
                    )  # append everything from end of last placeholder until end of string (if not empty) to result string
            else:  # special characters are passed to the result
                res.append(part)
        self.s = tuple(res)  # finally replace the string with the result

        return self

    def replace_with_placeholder(self, regex: Pattern, placeholder_name: str) -> "SigmaString":
        """
        Replace all occurrences of string part matching regular expression with placeholder.

        :param regex: regular expression that should be matched.
        :type regex: Pattern
        :param placeholder_name: name of placeholder that should be inserted.
        :type placeholder_name: str
        :return: Returns a string with the replacement placeholders.
        :rtype: SigmaString
        """
        result = []
        for e in self.s:
            if isinstance(e, str):
                matched = False
                i = 0
                for m in regex.finditer(e):
                    matched = True
                    s = e[i : m.start()]
                    if s != "":
                        result.append(s)
                    result.append(Placeholder(placeholder_name))
                    i = m.end()

                if matched:  # if matched, append remainder of string
                    s = e[i:]
                    if s != "":
                        result.append(s)
                else:  # no matches: append original string
                    result.append(e)
            else:
                result.append(e)

        s = self.__class__()
        s.s = tuple(result)
        return s

    def _merge_strs(self) -> "SigmaString":
        """Merge consecutive plain strings in self.s."""
        src = list(reversed(self.s))
        res = []
        while src:
            item = src.pop()
            try:
                if isinstance(res[-1], str) and isinstance(
                    item, str
                ):  # append current item to last result element if both are strings
                    res[-1] += item
                else:
                    res.append(item)
            except IndexError:  # first element
                res.append(item)

        self.s = tuple(res)
        return self

    def __add__(self, other: Union["SigmaString", str, SpecialChars, Placeholder]) -> "SigmaString":
        s = self.__class__()
        if isinstance(other, self.__class__):
            s.s = self.s + other.s
        elif isinstance(other, (str, SpecialChars, Placeholder)):
            s.s = self.s + (other,)
        else:
            return NotImplemented
        return s._merge_strs()

    def __radd__(self, other: Union[str, SpecialChars, Placeholder]) -> "SigmaString":
        if isinstance(other, (str, SpecialChars, Placeholder)):
            s = self.__class__()
            s.s = (other,) + self.s
            return s._merge_strs()
        else:
            return NotImplemented

    def __eq__(self, other: Union["SigmaString", str]) -> bool:
        if isinstance(other, str):
            return self == self.__class__(other)
        elif isinstance(other, self.__class__):
            return self.s == other.s
        else:
            raise NotImplementedError(
                "SigmaString can only be compared with a string or another SigmaString"
            )

    def __str__(self) -> str:
        rs = ""
        for s in self.s:
            if isinstance(s, str):
                rs += s
            elif isinstance(s, SpecialChars):
                rs += special_char_mapping[s]
            elif isinstance(s, Placeholder):
                rs += f"%{s.name}%"
            else:
                raise TypeError(
                    "SigmaString can only consist of plain strings and instances of SpecialChars or Placeholder objects."
                )
        return rs

    def __repr__(self) -> str:
        return str(f"SigmaString({self.s})")

    def to_plain(self):
        """Return plain string representation of SigmaString, equivalent to converting it with str()."""
        return str(self)

    def __bytes__(self) -> bytes:
        return str(self).encode()

    def __len__(self) -> int:
        return sum(
            (
                (
                    len(e)
                    if isinstance(e, str)  # count string parts with number of characters
                    else 1
                )  # everything else is counted as single character
                for e in self.s
            )
        )

    def startswith(self, val: Union[str, SpecialChars]) -> bool:
        """Check if string starts with a given string or special character."""
        if len(self.s) == 0:
            return False
        c = self.s[0]
        if not isinstance(val, type(c)):  # can't match if types differ
            return False
        elif isinstance(c, str):  # pass startswith invocation to string objects
            return c.startswith(val)
        else:  # direct comparison of SpecialChars
            return c == val

    def endswith(self, val: Union[str, SpecialChars]) -> bool:
        """Check if string ends with a given string or special character."""
        if len(self.s) == 0:
            return False
        c = self.s[-1]
        if not isinstance(val, type(c)):  # can't match if types differ
            return False
        elif isinstance(c, str):  # pass endswith invocation to string objects
            return c.endswith(val)
        else:  # direct comparison of SpecialChars
            return c == val

    def contains_special(self) -> bool:
        """Check if string contains special characters."""
        return any([isinstance(item, SpecialChars) for item in self.s])

    def contains_placeholder(
        self, include: Optional[List[str]] = None, exclude: Optional[List[str]] = None
    ) -> bool:
        """
        Check if string contains placeholders and if any placeholder name is

        * contained on the include list (if there is one)
        * not contained on the include list (if there is one)

        It is sufficient that one placeholder matches these conditions. The purpose of this method is to
        determine if there are placeholders for further processing.
        """
        return any(
            (
                isinstance(item, Placeholder)
                and (include is None or item.name in include)
                and (exclude is None or item.name not in exclude)
                for item in self.s
            )
        )

    def replace_placeholders(
        self,
        callback: Callable[[Placeholder], Iterator[Union[str, SpecialChars, Placeholder]]],
    ) -> List["SigmaString"]:
        """
        Iterate over all placeholders and call the callback for each one. The callback is called with the placeholder instance
        as argument and yields replacement values (plain strings or SpecialChars instances). Each yielded replacement value
        is concatenated to the SigmaString prefix before the placeholder and the method is called recursively with the suffix
        after the placeholder. All placeholder replacements are combined with all returned SigmaString suffixes. Therefore,
        the callback could be called multiple times with the same placeholder instance and should return the same results to ensure
        a consistent result.

        The callback can return a plain string, a SpecialChars instance (for insertion of wildcards) or a Placeholder (e.g. to keep
        the placeholder for later processing pipeline items).
        """
        if (
            not self.contains_placeholder()
        ):  # return unchanged string in a list if it doesn't contain placeholders
            return [self]

        s = self.s
        for i in range(len(s)):
            if isinstance(s[i], Placeholder):  # Placeholder instance at index, do replacement
                prefix = SigmaString()
                prefix.s = s[:i]
                placeholder = s[i]
                suffix = SigmaString()
                suffix.s = s[i + 1 :]
                return [
                    prefix + replacement + result_suffix
                    for replacement in callback(
                        placeholder
                    )  # iterate over all callback result values
                    for result_suffix in suffix.replace_placeholders(
                        callback
                    )  # iterate over all result values of calling this method with the SigmaString remainder
                ]

    def __iter__(self) -> Iterable[Union[str, SpecialChars]]:
        for item in self.s:
            if isinstance(item, str):  # yield single characters of string parts
                for char in item:
                    yield char
            else:
                yield item

    def iter_parts(self) -> Iterable[Union[str, SpecialChars]]:
        for item in self.s:
            yield item

    def map_parts(
        self,
        func: Callable[[Union[str, SpecialChars]], Optional[Union[str, SpecialChars]]],
        filter_func: Callable[[Union[str, SpecialChars]], bool] = lambda x: True,
    ) -> "SigmaString":
        s = self.__class__()
        s.s = tuple(
            filter(
                lambda x: x is not None,  # filter out None results
                (func(item) if filter_func(item) else item for item in self.iter_parts()),
            )
        )
        return s

    def convert(
        self,
        escape_char: Optional[str] = "\\",
        wildcard_multi: Optional[str] = "*",
        wildcard_single: Optional[str] = "?",
        add_escaped: str = "",
        filter_chars: str = "",
    ) -> str:
        """
        Convert SigmaString into a query string or pattern. The following parameters allow to change the behavior:

        * escape_char: the character used to escape special characters. By default these are only the wildcard characters.
        * wildcard_multi and wildcard_single: strings that should be output as wildcards for multiple and single characters.
        * add_escaped: characters which are escaped in addition to the wildcards
        * filter_chars: characters that are filtered out.

        Setting one of the wildcard or multiple parameters to None indicates that this feature is not supported. Appearance
        of these characters in a string will raise a SigmaValueError.
        """
        s = ""
        escaped_chars = frozenset((wildcard_multi or "") + (wildcard_single or "") + add_escaped)

        for c in self:
            if isinstance(c, str):  # c is plain character
                if c in filter_chars:  # Skip filtered characters
                    continue
                if c in escaped_chars:
                    s += escape_char
                s += c
            elif isinstance(c, SpecialChars):  # special handling for special characters
                if c == SpecialChars.WILDCARD_MULTI:
                    if wildcard_multi is not None:
                        s += wildcard_multi
                    else:
                        raise SigmaValueError(
                            "Multi-character wildcard not specified for conversion"
                        )
                elif c == SpecialChars.WILDCARD_SINGLE:
                    if wildcard_single is not None:
                        s += wildcard_single
                    else:
                        raise SigmaValueError(
                            "Single-character wildcard not specified for conversion"
                        )
            elif isinstance(c, Placeholder):
                raise SigmaPlaceholderError(
                    f"Attempt to convert unhandled placeholder '{c.name}' into query."
                )
            else:
                raise SigmaValueError(
                    f"Trying to convert SigmaString containing part of type '{type(c).__name__}'"
                )
        return s


class SigmaCasedString(SigmaString):
    """Case-sensitive string matching."""

    @classmethod
    def from_sigma_string(cls, s: SigmaString) -> "SigmaCasedString":
        cs = cls(s.original)
        cs.s = s.s
        return cs


@dataclass
class SigmaNumber(SigmaType):
    """Numeric value type"""

    number: Union[int, float]

    def __post_init__(self):
        try:  # Only use float number if it can't be represented as int.
            i = int(self.number)
            f = float(self.number)
            if i == f:
                self.number = i
            else:
                self.number = f
        except ValueError as e:
            raise SigmaValueError("Invalid number") from e

    def __str__(self):
        return str(self.number)

    def __eq__(self, other: Union["SigmaNumber", int]) -> bool:
        if isinstance(other, int):
            return self.number == other
        else:
            return self.number == other.number


@dataclass
class SigmaBool(SigmaType):
    """Boolean value type"""

    boolean: bool

    def __post_init__(self):
        if not isinstance(self.boolean, bool):
            raise SigmaTypeError("SigmaBool must be a boolean")

    def __str__(self):
        return str(self.boolean)

    def __bool__(self):
        return self.boolean


class SigmaRegularExpressionFlag(Enum):
    IGNORECASE = auto()
    MULTILINE = auto()
    DOTALL = auto()


@dataclass
class SigmaRegularExpression(SigmaType):
    """Regular expression type"""

    regexp: str
    flags: Set[SigmaRegularExpressionFlag] = field(default_factory=set)
    sigma_to_python_flags: ClassVar[Dict[SigmaRegularExpressionFlag, re.RegexFlag]] = {
        SigmaRegularExpressionFlag.IGNORECASE: re.IGNORECASE,
        SigmaRegularExpressionFlag.MULTILINE: re.MULTILINE,
        SigmaRegularExpressionFlag.DOTALL: re.DOTALL,
    }
    sigma_to_re_flag: ClassVar[Dict[SigmaRegularExpressionFlag, str]] = {
        SigmaRegularExpressionFlag.IGNORECASE: "i",
        SigmaRegularExpressionFlag.MULTILINE: "m",
        SigmaRegularExpressionFlag.DOTALL: "s",
    }

    def __post_init__(self):
        self.compile()

    def add_flag(self, flag: SigmaRegularExpressionFlag):
        self.flags.add(flag)

    def compile(self):
        """Verify if regular expression is valid by compiling it"""
        try:
            flags = 0
            for flag in self.flags:
                flags |= self.sigma_to_python_flags[flag]
            re.compile(self.regexp, flags)
        except re.error as e:
            raise SigmaRegularExpressionError(
                f"Regular expression '{self.regexp}' is invalid: {str(e)}"
            ) from e

    def escape(
        self,
        escaped: Tuple[str] = (),
        escape_char: str = "\\",
        escape_escape_char: bool = True,
        flag_prefix: bool = True,
    ) -> str:
        """Escape strings from escaped tuple as well as escape_char itself (can be disabled with
        escape_escape_char) with escape_char. Prepends a (?...) expression with set flags (i, m and
        s) if flag_prefix is set."""
        r = "|".join(
            [  # Generate regular expressions from sequences that should be escaped and the escape char itself
                re.escape(e)
                for e in [*escaped, escape_char if escape_escape_char else None]
                if e is not None
            ]
        )
        pos = (
            [  # determine positions of matches in regular expression
                m.start() for m in re.finditer(r, self.regexp)
            ]
            if r != ""
            else []
        )
        ranges = zip([None, *pos], [*pos, None])  # string chunk ranges with escapes in between
        ranges = list(ranges)

        if flag_prefix and self.flags:
            prefix = (
                "(?" + "".join(sorted((self.sigma_to_re_flag[flag] for flag in self.flags))) + ")"
            )
        else:
            prefix = ""

        return prefix + escape_char.join([self.regexp[i:j] for i, j in ranges])


@dataclass
class SigmaCIDRExpression(NoPlainConversionMixin, SigmaType):
    """CIDR IP address range expression type"""

    cidr: str
    source: Optional[SigmaRuleLocation] = None
    network: Union[IPv4Network, IPv6Network] = field(init=False, compare=False)

    def __post_init__(self):
        """Verify if cidr is valid by re"""
        try:
            self.network = ip_network(self.cidr)
        except ValueError as e:
            raise SigmaTypeError("Invalid CIDR expression: " + str(e), source=self.source)

    def expand(
        self,
        wildcard: str = "*",
    ) -> List[str]:
        """
        Convert CIDR range into a list of wildcard patterns or plain CIDR notation. The following parameters allow to change the behavior:

        * wildcard: string that should be output as wildcard. Usually not required because this is
          passed to SigmaString that generates a wildcard pecial character from '*' that is
          converted into possible individual wildcard characters.

        Setting wildcard to None indicates that this feature is not need and the query language handles CIDR notation properly.
        """
        patterns = []
        if isinstance(
            self.network, IPv4Network
        ):  # IPv4, algorithm: each group of an IPv4 address represents 8 bit. Therefore, we align to 8 bit boundaries, iterate over the remaining bits and put a wildcard at the end (if not /32)
            prefix_rem8 = (
                self.network.prefixlen % 8
            )  # This variable stores the number of bits exceeding the previous 8 bit boundary
            prefix_diff = (
                8 - prefix_rem8
            ) % 8  # We want the next 8 bit boundary to expand into smaller subnets, therefore the other side of the remainder is used.
            for subnet in self.network.subnets(
                prefix_diff
            ):  # Generate all the subnetworks where the prefix ends at the next 8 bit boundary
                wildcard_group = (
                    subnet.prefixlen // 8
                )  # Determine group that has to be replaced with wildcard: 8 bit boundary before prefix
                subnet_groups = str(subnet.network_address).split(".")
                if wildcard_group == 0:  # Not all groups are static, add wildcard
                    patterns.append(wildcard)
                elif wildcard_group < 4:  # Not all groups are static, add wildcard
                    patterns.append(".".join(subnet_groups[:wildcard_group]) + "." + wildcard)
                else:  # /32 - no wildcard is set
                    patterns.append(
                        str(subnet.network_address)
                    )  # Return single address subnet without wildcard
        else:  # IPv6, algorithm: each hex digit of an IPv6 address represents 4 bit. Therefore, we align to 4 bit boundaries and iterate over the remaining bits.
            prefix_rem4 = (
                self.network.prefixlen % 4
            )  # This variable stores the number of bits exceeding the previous 4 bit boundary
            prefix_diff = (
                4 - prefix_rem4
            ) % 4  # We want the next 4 bit boundary to expand into smaller subnets, therefore the other side of the remainder is used.
            for subnet in self.network.subnets(
                prefix_diff
            ):  # Generate all the subnetworks where the prefix ends at the next 4 bit boundary
                first_addr = str(subnet.network_address)
                last_addr = str(subnet.broadcast_address)
                wildcard_required = False  # There's the possibility that no wildcard is required at all if the prefix is /128 (e.g. localhost)
                for i in range(
                    len(first_addr)
                ):  # Determine the first char that differs between the first and last network address of the network. This is the location where the wildcard has to be placed.
                    if first_addr[i] != last_addr[i]:
                        wildcard_required = True
                        break  # location found
                if wildcard_required:
                    patterns.append(
                        str(subnet)[:i] + wildcard
                    )  # Generate pattern by cutting of at first difference
                else:  # The /128 case - no differences
                    patterns.append(str(subnet))  # Return the single address
        return patterns


@dataclass
class SigmaCompareExpression(NoPlainConversionMixin, SigmaType):
    """Type for numeric comparison."""

    class CompareOperators(Enum):
        LT = auto()  # <
        LTE = auto()  # <=
        GT = auto()  # >
        GTE = auto()  # >=

    number: SigmaNumber
    op: CompareOperators
    source: Optional[SigmaRuleLocation] = None

    def __post_init__(self):
        if not isinstance(self.number, SigmaNumber):
            raise SigmaTypeError("Compare operator expects number", source=self.source)


@dataclass
class SigmaFieldReference(NoPlainConversionMixin, SigmaType):
    """Type for referencing to other fields for comparison between them."""

    field: str


@dataclass
class SigmaQueryExpression(NoPlainConversionMixin, SigmaType):
    """
    Special purpose type for passing a query part (e.g. list lookups in placeholders) directly into the generated
    query. The query string may contain a {field} placeholder, which is replaced with the field name contained in
    the detection item containing the query expression. This is done by the finalize method.

    Because this is very specific to the target language, it has to be used in late stages of the conversion
    process by backend-specific processing pipelines or the backend itself.
    """

    expr: str
    id: str

    def __post_init__(self):
        if not isinstance(self.expr, str):
            raise SigmaTypeError("SigmaQueryExpression expression must be a string")
        if not isinstance(self.id, str):
            raise SigmaTypeError("SigmaQueryExpression placeholder identifier must be a string")

    def __str__(self):
        return self.expr

    def has_field_placeholder(self) -> bool:
        return "{field}" in self.expr

    def finalize(self, field: Optional[str] = None) -> str:
        if field is None and self.has_field_placeholder():
            raise SigmaValueError(
                f"Query expression '{ self.expr }' has a field placeholder but no field was given in finalization"
            )
        return self.expr.format(field=field, id=self.id)


@dataclass
class SigmaExpansion(NoPlainConversionMixin, SigmaType):
    """
    Special purpose type for correct logic linking of values expanded by modifiers. In the usual
    cases the writer of a Sigma rule expects the values expanded by modifiers like base64offset or
    windash are OR-linked, even if the value list containing the original values is linked with AND
    by modifying it with 'all'. A SigmaExpansion is emitted by such modifiers, contains the
    expanded values and is converted as follows:

    1. the whole expansion is handled as group which is enclosed in parentheses.
    2. the values contained in the expansion are linked with OR, independent from the linking of the
       context that encloses the expansion.
    """

    values: List[SigmaType]


type_map = {
    bool: SigmaBool,
    int: SigmaNumber,
    float: SigmaNumber,
    str: SigmaString,
    type(None): SigmaNull,
}


def sigma_type(v: Optional[Union[int, float, str]]):
    """Return Sigma type from Python value"""
    for t, st in type_map.items():
        if isinstance(v, t):
            return st(v)
