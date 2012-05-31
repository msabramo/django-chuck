# -*- encoding: utf-8 -*-
THOUSAND_SEPARATOR = "'"
DECIMAL_SEPARATOR = '.'
DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M:%S',    # '25.10.2006 14:30:59'
    '%d.%m.%Y %H:%M',       # '25.10.2006 14:30'
    '%d.%m.%Y',             # '25.10.2006'
    '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
    '%Y-%m-%d',             # '2006-10-25'
)