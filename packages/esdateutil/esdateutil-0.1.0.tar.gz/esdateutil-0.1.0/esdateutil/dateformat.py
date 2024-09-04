#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for handling Elasticsearch date strings and date math in Python.

Copyright (c) 2024, Matthew Murr
License: MIT (see LICENSE for details)
https://git.sr.ht/~murr/esdateutil
"""

# ES Implementation:
# - https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/common/time/DateFormatter.java
# - https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/common/time/DateFormatters.java
# ES Tests: https://github.com/elastic/elasticsearch/blob/main/server/src/test/java/org/elasticsearch/common/time/DateFormattersTests.java

from datetime import datetime

DATE_FORMATS = {}
def date_format_fn(fn):
    DATE_FORMATS[fn.__name__] = fn
    return fn

def date_formatter(fmts):
    fmt_fns = [DATE_FORMATS[fmt] for fmt in fmts]
    # TODO This very much prevents pickling, prefer a partial or returning an object or something
    def fn(s, tz=None):
        for fmt_fn in fmt_fns:
            try:
                return fmt_fn(s, tz)
            except ValueError:
                continue
    return fn

def date_formatter_str(fmt_str="", separator="||"):
    return date_formatter(fmt_str.split(separator))

@date_format_fn
def epoch_millis(s, tz=None):
    return datetime.fromtimestamp(int(s)/1000, tz=tz)

@date_format_fn
def epoch_second(s, tz=None):
    return datetime.fromtimestamp(int(s), tz=tz)

@date_format_fn
def strict_date_optional_time_nanos(s, tz=None):
    try:
        # TODO This is not a strict date optional time, you bastard.
        # I'm doing this for now because it's way faster than iterating over
        # way too many strptime calls, but it has false positives so it's
        # functionally incorrect.
        d = datetime.fromisoformat(s)
        if not d.tzinfo:
            d = d.replace(tzinfo=tz)
        return d
        #return datetime.striptime(s, "%Y-%m-%dT%H:%M:%S.%fZ", tz=UTC)
    except ValueError:
        pass

    # We ascend in size as later times overlap with what datetime.fromisoformat accepts.
    for fmt in "%Y", "%Y-%m", "%Y-%m-%d", "%Y-%m-%dT%H", "%Y-%m-%dT%H:%M","%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S,%f":
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=tz)
        except ValueError:
            continue

    # No format matched.
    raise ValueError(f"Used strict_date_optional_time or strict_date_optional_time_nanos but string {s} does not match format")

@date_format_fn
def strict_date_optional_time(s, tz=None):
    d = strict_date_optional_time_nanos(s, tz)
    if d.microsecond % 1000:
        raise ValueError(f"Used strict_date_optional_time but fractional seconds of {s} are not milliseconds")
    return d

# TODO :)
def date_optional_time(s, tz=None):
    raise NotImplementedError("date_optional_time")

def basic_date(s, tz=None):
    raise NotImplementedError("basic_date")

def basic_date_time(s, tz=None):
    raise NotImplementedError("basic_date_time")

def basic_date_time_no_millis(s, tz=None):
    raise NotImplementedError("basic_date_time_no_millis")

def basic_ordinal_date(s, tz=None):
    raise NotImplementedError("basic_ordinal_date")

def basic_ordinal_date_time(s, tz=None):
    raise NotImplementedError("basic_ordinal_date_time")

def basic_ordinal_date_time_no_millis(s, tz=None):
    raise NotImplementedError("basic_ordinal_date_time_no_millis")

def basic_time(s, tz=None):
    raise NotImplementedError("basic_time")

def basic_time_no_millis(s, tz=None):
    raise NotImplementedError("basic_time_no_millis")

def basic_t_time(s, tz=None):
    raise NotImplementedError("basic_t_time")

def basic_t_time_no_millis(s, tz=None):
    raise NotImplementedError("basic_t_time_no_millis")

def basic_week_date(s, tz=None):
    raise NotImplementedError("basic_week_date")

def strict_basic_week_date(s, tz=None):
    raise NotImplementedError("strict_basic_week_date")

def basic_week_date_time(s, tz=None):
    raise NotImplementedError("basic_week_date_time")

def strict_basic_week_date_time(s, tz=None):
    raise NotImplementedError("strict_basic_week_date_time")

def basic_week_date_time_no_millis(s, tz=None):
    raise NotImplementedError("basic_week_date_time_no_millis")

def strict_basic_week_date_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_basic_week_date_time_no_millis")

def date(s, tz=None):
    raise NotImplementedError("date")

def strict_date(s, tz=None):
    raise NotImplementedError("strict_date")

def date_hour(s, tz=None):
    raise NotImplementedError("date_hour")

def strict_date_hour(s, tz=None):
    raise NotImplementedError("strict_date_hour")

def date_hour_minute(s, tz=None):
    raise NotImplementedError("date_hour_minute")

def strict_date_hour_minute(s, tz=None):
    raise NotImplementedError("strict_date_hour_minute")

def date_hour_minute_second(s, tz=None):
    raise NotImplementedError("date_hour_minute_second")

def strict_date_hour_minute_second(s, tz=None):
    raise NotImplementedError("strict_date_hour_minute_second")

def date_hour_minute_second_fraction(s, tz=None):
    raise NotImplementedError("date_hour_minute_second_fraction")

def strict_date_hour_minute_second_fraction(s, tz=None):
    raise NotImplementedError("strict_date_hour_minute_second_fraction")

def date_hour_minute_second_millis(s, tz=None):
    raise NotImplementedError("date_hour_minute_second_millis")

def strict_date_hour_minute_second_millis(s, tz=None):
    raise NotImplementedError("strict_date_hour_minute_second_millis")

def date_time(s, tz=None):
    raise NotImplementedError("date_time")

def strict_date_time(s, tz=None):
    raise NotImplementedError("strict_date_time")

def date_time_no_millis(s, tz=None):
    raise NotImplementedError("date_time_no_millis")

def strict_date_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_date_time_no_millis")

def hour(s, tz=None):
    raise NotImplementedError("hour")

def strict_hour(s, tz=None):
    raise NotImplementedError("strict_hour")

def hour_minute(s, tz=None):
    raise NotImplementedError("hour_minute")

def strict_hour_minute(s, tz=None):
    raise NotImplementedError("strict_hour_minute")

def hour_minute_second(s, tz=None):
    raise NotImplementedError("hour_minute_second")

def strict_hour_minute_second(s, tz=None):
    raise NotImplementedError("strict_hour_minute_second")

def hour_minute_second_fraction(s, tz=None):
    raise NotImplementedError("hour_minute_second_fraction")

def strict_hour_minute_second_fraction(s, tz=None):
    raise NotImplementedError("strict_hour_minute_second_fraction")

def hour_minute_second_millis(s, tz=None):
    raise NotImplementedError("hour_minute_second_millis")

def strict_hour_minute_second_millis(s, tz=None):
    raise NotImplementedError("strict_hour_minute_second_millis")

def ordinal_date(s, tz=None):
    raise NotImplementedError("ordinal_date")

def strict_ordinal_date(s, tz=None):
    raise NotImplementedError("strict_ordinal_date")

def ordinal_date_time(s, tz=None):
    raise NotImplementedError("ordinal_date_time")

def strict_ordinal_date_time(s, tz=None):
    raise NotImplementedError("strict_ordinal_date_time")

def ordinal_date_time_no_millis(s, tz=None):
    raise NotImplementedError("ordinal_date_time_no_millis")

def strict_ordinal_date_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_ordinal_date_time_no_millis")

def time(s, tz=None):
    raise NotImplementedError("time")

def strict_time(s, tz=None):
    raise NotImplementedError("strict_time")

def time_no_millis(s, tz=None):
    raise NotImplementedError("time_no_millis")

def strict_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_time_no_millis")

def t_time(s, tz=None):
    raise NotImplementedError("t_time")

def strict_t_time(s, tz=None):
    raise NotImplementedError("strict_t_time")

def t_time_no_millis(s, tz=None):
    raise NotImplementedError("t_time_no_millis")

def strict_t_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_t_time_no_millis")

def week_date(s, tz=None):
    raise NotImplementedError("week_date")

def strict_week_date(s, tz=None):
    raise NotImplementedError("strict_week_date")

def week_date_time(s, tz=None):
    raise NotImplementedError("week_date_time")

def strict_week_date_time(s, tz=None):
    raise NotImplementedError("strict_week_date_time")

def week_date_time_no_millis(s, tz=None):
    raise NotImplementedError("week_date_time_no_millis")

def strict_week_date_time_no_millis(s, tz=None):
    raise NotImplementedError("strict_week_date_time_no_millis")

def weekyear(s, tz=None):
    raise NotImplementedError("weekyear")

def strict_weekyear(s, tz=None):
    raise NotImplementedError("strict_weekyear")

def weekyear_week(s, tz=None):
    raise NotImplementedError("weekyear_week")

def strict_weekyear_week(s, tz=None):
    raise NotImplementedError("strict_weekyear_week")

def weekyear_week_day(s, tz=None):
    raise NotImplementedError("weekyear_week_day")

def strict_weekyear_week_day(s, tz=None):
    raise NotImplementedError("strict_weekyear_week_day")

def year(s, tz=None):
    raise NotImplementedError("year")

def strict_year(s, tz=None):
    raise NotImplementedError("strict_year")

def year_month(s, tz=None):
    raise NotImplementedError("year_month")

def strict_year_month(s, tz=None):
    raise NotImplementedError("strict_year_month")

def year_month_day(s, tz=None):
    raise NotImplementedError("year_month_day")

def strict_year_month_day(s, tz=None):
    raise NotImplementedError("strict_year_month_day")


if __name__ == "__main__":
    print(DATE_FORMATS.keys())
    date_parser = date_formatter_str("strict_date_optional_time||epoch_millis")
    print(date_parser)
    print(date_parser("2922789948123"))
    print(date_parser("2024"))
    print(date_parser("2024-04"))
    print(date_parser("2024-04-11T14:00:01"))
