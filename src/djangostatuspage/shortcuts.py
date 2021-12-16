"""Various useful function."""

import datetime
import itertools
import re


def camel_case_split(s: str):
    """Split camel (and pascal) case string into words."""
    start_idx = [0] + [i for i, e in enumerate(s) if e.isupper() and i > 0]
    start_idx.append(len(s))

    return [s[x:y] for x, y in zip(start_idx, start_idx[1:])]


def get_enum_choices(enum):
    """Get list of choices suitable for Django Model from enum class."""
    return [(choice.value, make_verbose_name(choice.name)) for choice in enum]


def make_verbose_name(name: str, glue: str = " "):
    """Glue words from camelCase, snake_case etc. and capitalize first letter."""
    name = glue.join(multi_case_split(name.lower())).capitalize()
    return name


def multi_case_split(s: str, split_pattern: str = "[_-]"):
    """Split a string into words: camelCase, PascalCase, snake_case, kebap-case, etc."""
    camel_split = camel_case_split(s)
    splits = itertools.chain(*[re.split(split_pattern, s) for s in camel_split])
    non_blank_splits = list(filter(len, splits))
    return non_blank_splits if len(non_blank_splits) > 0 else [""]


def utc_now():
    """Get current UTC time with timezone info."""
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
