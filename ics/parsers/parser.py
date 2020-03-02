from typing import Callable, Dict, List, Optional, Tuple
from collections import namedtuple

from ics.grammar.parse import ContentLine


ParserOption = namedtuple("ParserOption", ["required", "multiple", "default"])
ParserOption.__new__.__defaults__ = (False, False, None)


class Parser:
    @classmethod
    def get_parsers(cls) -> Dict[str, Tuple[Callable, ParserOption]]:
        methods = [
            (method_name, getattr(cls, method_name))
            for method_name in dir(cls)
            if callable(getattr(cls, method_name))
        ]
        parsers = [
            (method_name, method_callable)
            for (method_name, method_callable) in methods
            if method_name.startswith("parse_")
        ]
        return {
            method_name.split("_", 1)[1]
            .upper()
            .replace("_", "-"): (
                method_callable,
                getattr(method_callable, "options", ParserOption()),
            )
            for (method_name, method_callable) in parsers
        }


def option(
    required: bool = False,
    multiple: bool = False,
    default: Optional[List[ContentLine]] = None,
) -> Callable:
    def decorator(fn):
        fn.options = ParserOption(required, multiple, default)
        return fn

    return decorator
