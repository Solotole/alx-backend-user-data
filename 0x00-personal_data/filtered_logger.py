#!/usr/bin/env python3
"""Basic Regex-ing"""
import re
import logging
from typing import List, Optional, Tuple


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """Filters a log message by obfuscating specified fields."""
    pattern: str = rf"(?:{separator})({'|'.join(fields)})=([^;]+)"
    return re.sub(pattern, rf"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """formating method"""
        filter_string: str = filter_datum(
                                        self.fields,
                                        self.REDACTION,
                                        record.getMessage(),
                                        self.SEPARATOR
                                        )
        record.msg: str = filter_string
        return super().format(record)
