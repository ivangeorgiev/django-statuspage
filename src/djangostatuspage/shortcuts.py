import datetime
import itertools
import re

def camel_case_split(s: str):
    """Split camel (and pascal) case string into words"""
    start_idx = [0] + \
                [i for i, e in enumerate(s)
                   if e.isupper() and i>0 ]
    start_idx.append(len(s))

    return [s[x: y] for x, y in zip(start_idx, start_idx[1:])]

def multi_case_split(s: str, split_pattern='[_-]'):
    camel_split = camel_case_split(s)
    splits = itertools.chain(*map(lambda s: re.split(split_pattern, s), camel_split))
    non_blank_splits = list(filter(len, splits))
    return list(non_blank_splits) if len(non_blank_splits) > 0 else ['']


def utc_now():
    """Get current UTC time with timezone info"""
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

