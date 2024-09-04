# esdateutil

Provides utilities for handling dates like how Elasticsearch does.

In particular:
 - Datemath parsing and evaluation
 - ES-like datetime string format parsing

The goals of this project are:
 - Be as close to Elasticsearch behaviour as Python makes sensible.
 - No runtime dependencies.
 - Customizability; most functionality should be parameterizable.

This project will be version 1.0 when it provides:
 - Full datemath parsing
 - ES & java-style date string format parsing (https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html)
 - Robust tests for weird stuff like datemath rounding on DST boundaries

## Building

Requires pyenv and pyenv-virtualenv to be installed on your machine.
Requires pyenv-init (pyenv and pyenv-virtualenv) to be run for pyenv local to work w/ virtualenv

## Hitchhiker's Guide to Python Datetimes

One of the consequences of using Python's built-in datetime objects and
functions by default is that they can behave very differently from version to
version and from Elasticsearch defaults. Below are some of the most important
differences in functionality to be aware of.

 - The default date parsing format in Elasticsearch is
   [strict_date_optional_time||epoch_millis](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html).
   The default parse function of DateMath in this library is
   datetime.datetime.fromisoformat, but it can be customized with
   `DateMath(date_fn=custom_date_parsing_function)`. The dateformat module
   approximates the ES functionality, but is not correct yet. If you are
   parsing datemath strings containing absolute datetime values, this means:
   - By default, ES supports millisecond epochs as a datetime format, by default we do not.
   - datetime.datetime.fromisoformat only [parses from ISO format properly in 3.11+](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat).
     It is recommended to use a different date_fn if you are using a version
     below 3.11, such as python-dateutil's
     [parser.parse](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) and [parser.isoparse](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse) or the [iso8601](https://pypi.org/project/iso8601/) library.
   - ES strict_date_optional_time allows 2024 or 2024-08 as dates, but Python's
     fromisoformat does not even in 3.11+. python-dateutil
     [parser.isoparse](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse)
     and [iso8601](https://pypi.org/project/iso8601/) support this, or you can
     set a custom date_fn using the dateformat module of this library or the
     built-in strptime if you need this functionality.
 - The default time resolution in Elasticsearch is milliseconds, whereas in
   Python datetime it is microseconds. This shouldn't be important unless you
   are using the optional UNITS_ROUND_UP or another custom round
   implementation. UNITS_ROUND_UP_MILLIS is provided as an alternative.
