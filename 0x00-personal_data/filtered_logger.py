#!/usr/bin/env python3
"""Regex-ing an input"""
import re

def filter_datum(fields, redaction, message, separator):
    """function that returns the log message obfuscated"""
    return re.sub(r'({})=[^{}]*'.format('|'.join(fields), separator), r'\1={}'.format(redaction), message)
