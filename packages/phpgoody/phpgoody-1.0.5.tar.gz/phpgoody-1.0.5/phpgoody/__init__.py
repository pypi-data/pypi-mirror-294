"""
Implement php functions in python
"""

import datetime
from typing import Any

import dateutil
import dateutil.relativedelta


def time():
    """
    Return current unix timestamp
    """
    return int(datetime.datetime.now().timestamp())


def date(format: str, timestamp: int = None):
    """
    Format a local time/date
    """
    if timestamp is None:
        return datetime.datetime.now().strftime(format)

    return datetime.datetime.fromtimestamp(timestamp).strftime(format)


def date_default_timezone_set(timezone: str):
    """
    Sets the default timezone used by all date/time functions in a script
    """
    import os

    os.environ["TZ"] = timezone
    os.tzset()


def is_file(filename: str) -> bool:
    """
    Checks whether a file or directory exists
    """
    import os

    return os.path.isfile(filename)


def file_exists(filename: str) -> bool:
    """
    Checks whether a file or directory exists.
    """
    import os

    return os.path.exists(filename)


def each(array: list | dict):
    """
    Return the current key and value pair from an array and advance the array cursor
    """
    for key, value in enumerate(array) if isinstance(array, list) else array.items():
        yield key, value


def json_decode(json_string: str):
    """
    Decodes a JSON string
    """
    import json

    return json.loads(json_string)


def json_encode(data) -> str:
    """
    Returns the JSON representation of a value
    """
    import json
    from collections.abc import Mapping, Iterable
    from decimal import Decimal

    class DecimalEncoder(json.JSONEncoder):
        def encode(self, obj):
            if isinstance(obj, Mapping):
                return (
                        "{"
                        + ", ".join(
                    f"{self.encode(k)}: {self.encode(v)}" for (k, v) in obj.items()
                )
                        + "}"
                )
            if isinstance(obj, Iterable) and (not isinstance(obj, str)):
                return "[" + ", ".join(map(self.encode, obj)) + "]"
            if isinstance(obj, Decimal):
                return f"{obj.normalize():f}"  # using normalize() gets rid of trailing 0s, using ':f' prevents scientific notation
            return super().encode(obj)

    return json.dumps(data, cls=DecimalEncoder, default=str)


def file_put_contents(filename: str, data: str):
    """
    Write data to a file
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

    return len(data)


def array_map(callback, array: list):
    """
    Applies the callback to the elements of the given arrays
    """
    return [callback(value) for value in array]


def file_get_contents(filename: str):
    """
    Reads entire file into a string
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def preg_match(pattern: str, subject: str):
    """
    Perform a regular expression match
    """
    import re

    match = re.search(pattern, subject)

    return match.groups() if match else None


def strtotime(datetime_: str, baseTimestamp: int = None) -> int:
    """
    Parse about any English textual datetime description into a Unix timestamp
    """
    if baseTimestamp is None:
        baseTimestamp = time()

    base = datetime.datetime.fromtimestamp(baseTimestamp)

    if datetime_ == "now":
        return baseTimestamp

    if datetime_ == "tomorrow":
        return (base + datetime.timedelta(days=1)).timestamp()

    if datetime_ == "yesterday":
        return base - datetime.timedelta(days=1).timestamp()

    matches = preg_match(r"^(-?\d+)\s(days|day|year|years)?$", datetime_)
    matches = list(matches)
    if matches:
        if matches[1] == "year":
            matches[1] = "years"
        if matches[1] == "day":
            matches[1] = "days"

        return (
                base + dateutil.relativedelta.relativedelta(**{matches[1]: int(matches[0])})
        ).timestamp()

    return False


def str_ends_with(haystack: str, needle: str) -> bool:
    """
    Check if a string ends with a specific string
    """
    return haystack.endswith(needle)


def str_starts_with(haystack: str, needle: str) -> bool:
    """
    Check if a string starts with a specific string
    """
    return haystack.startswith(needle)


def array_merge(*arrays: list | dict) -> list | dict:
    """
    Merge one or more arrays
    """
    if isinstance(arrays[0], dict):
        result = {}
        for array in arrays:
            result = {**result, **array}

        return result

    result = []
    for array in arrays:
        result.extend(array)

    return result


def array_values(array: dict) -> list:
    """
    Return all the values of an array
    """
    return list(array.values())


def array_keys(array: dict) -> list:
    """
    Return all the keys of an array
    """
    return list(array.keys())


def array_column(array: list, column: str) -> list:
    """
    Return the values from a single column in the input array
    """
    return [row[column] for row in array]


def ksort(array: dict) -> dict:
    """
    Sort an array by key
    """
    return dict(sorted(array.items()))


def date_diff(date1: str, date2: str):
    """
    Returns the difference between two DateTime objects
    """
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

    return date2 - date1


def sleep(seconds: int):
    """
    Delay execution
    """
    import time

    time.sleep(seconds)


def array_sum(array: list) -> int:
    """
    Calculate the sum of values in an array
    """
    return sum(array)


def array_slice(array: list | dict, offset: int, length: int = None) -> dict[Any, Any] | list:
    """
    Extract a slice of the array
    """
    if isinstance(array, dict):
        array = list(array.items())
        return dict(array[offset: offset + length])

    return array[offset: offset + length]


def array_reverse(array: list) -> list:
    """
    Return an array with elements in reverse order
    """
    return array[::-1]


def arsort(array: dict) -> dict:
    """
    Sort an array in reverse order and maintain index association
    """
    return dict(sorted(array.items(), key=lambda x: x[1], reverse=True))


def preg_replace(pattern: str, replacement: str, subject: str) -> str:
    """
    Perform a regular expression search and replace
    """
    import re

    return re.sub(pattern, replacement, subject)


def md5(string: str) -> str:
    """
    Calculate the md5 hash of a string
    """
    import hashlib

    return hashlib.md5(string.encode()).hexdigest()
