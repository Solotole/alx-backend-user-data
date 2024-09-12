#!/usr/bin/env python3
"""Basic Regex-ing"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Filters a log message by obfuscating specified fields."""
    pattern: str = rf"(?:{separator})({'|'.join(fields)})=([^;]+)"
    return re.sub(pattern, rf"\1={redaction}", message)
