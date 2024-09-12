#!/usr/bin/python3
"""Basic Regex-ing"""
import re

def filter_datum(fields, redaction, message, separator):
  """Filters a log message by obfuscating specified fields."""
  pattern = rf"(?:{separator})({'|'.join(fields)})=([^;]+)"
  return re.sub(pattern, rf"\1={redaction}", message)
