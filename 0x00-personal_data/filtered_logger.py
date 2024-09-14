#!/usr/bin/env python3
"""Basic Regex-ing"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in the log message.

    Args:
    fields (list): A list of strings representing all fields to obfuscate.
    redaction (str): A string representing what to obfuscate the field with.
    message (str): The log line to be filtered.
    separator (str): The separator between fields in the log line.

    Returns:
    str: The obfuscated log message.
    """
    return re.sub(f"({'|'.join(fields)})=.*?{separator}",
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)
