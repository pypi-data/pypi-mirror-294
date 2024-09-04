#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for handling Elasticsearch date strings and date math in Python.

Copyright (c) 2024, Matthew Murr
License: MIT (see LICENSE for details)
https://git.sr.ht/~murr/esdateutil
"""

# ES Ref: https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math

import logging

from datetime import datetime, timedelta
from calendar import monthrange


LOG = logging.getLogger(__name__)

def units_delta_months_add(d: datetime, n: int) -> datetime:
    month = d.month + n
    year = d.year + (month-1) // 12
    month = (month % 12) or 12
    return d.replace(year=year, month=month)

UNITS_DELTA_DEFAULT = {
    'y': lambda d, n: d.replace(year=d.year+n),
    'M': lambda d, n: units_delta_months_add(d, n),
    'w': lambda d, n: d + timedelta(days=n*7),
    'd': lambda d, n: d + timedelta(days=n),
    'h': lambda d, n: d + timedelta(hours=n),
    'H': lambda d, n: d + timedelta(hours=n),
    'm': lambda d, n: d + timedelta(minutes=n),
    's': lambda d, n: d + timedelta(seconds=n)
}

UNITS_ROUND_DOWN = {
    'y': lambda d: d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0),
    'M': lambda d: d.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
    'w': lambda d: (d - timedelta(days=d.weekday())).replace(hour=0, minute=0, second=0, microsecond=0),
    'd': lambda d: d.replace(hour=0, minute=0, second=0, microsecond=0),
    'h': lambda d: d.replace(minute=0, second=0, microsecond=0),
    'H': lambda d: d.replace(minute=0, second=0, microsecond=0),
    'm': lambda d: d.replace(second=0, microsecond=0),
    's': lambda d: d.replace(microsecond=0),
}
UNITS_ROUND_DEFAULT = UNITS_ROUND_DOWN

UNITS_ROUND_UP = {
    'y': lambda d: d.replace(month=12, day=monthrange(d.year, 12)[1], hour=23, minute=59, second=59, microsecond=999999),
    'M': lambda d: d.replace(day=monthrange(d.year, d.month)[1], hour=23, minute=59, second=59, microsecond=999999),
    'w': lambda d: (d + timedelta(days=6-d.weekday())).replace(hour=23, minute=59, second=59, microsecond=999999),
    'd': lambda d: d.replace(hour=23, minute=59, second=59, microsecond=999999),
    'h': lambda d: d.replace(minute=59, second=59, microsecond=999999),
    'H': lambda d: d.replace(minute=59, second=59, microsecond=999999),
    'm': lambda d: d.replace(second=59, microsecond=999999),
    's': lambda d: d.replace(microsecond=999999),
}
UNITS_ROUND_UP_MILLIS = {
    'y': lambda d: d.replace(month=12, day=monthrange(d.year, 12)[1], hour=23, minute=59, second=59, microsecond=999000),
    'M': lambda d: d.replace(day=monthrange(d.year, d.month)[1], hour=23, minute=59, second=59, microsecond=999000),
    'w': lambda d: (d + timedelta(days=6-d.weekday())).replace(hour=23, minute=59, second=59, microsecond=999000),
    'd': lambda d: d.replace(hour=23, minute=59, second=59, microsecond=999000),
    'h': lambda d: d.replace(minute=59, second=59, microsecond=999000),
    'H': lambda d: d.replace(minute=59, second=59, microsecond=999000),
    'm': lambda d: d.replace(second=59, microsecond=999000),
    's': lambda d: d.replace(microsecond=999000),
}

class DateMath():

    def __init__(self, timezone=None, separator="||", now_str="now", now_fn=lambda tz: datetime.now(tz), date_fn=datetime.fromisoformat, units_delta: dict=None, units_round: dict=None):
        LOG.debug("Initialising new DateMath instance: timezone=%s, separator=\"%s\", now_fn=%s, date_fn=%s, units_delta=%s, units_round=%s", timezone, separator, now_fn, date_fn, units_delta, units_round)

        self.idx = None
        self.len = None
        self.timezone = timezone

        if not separator:
            raise ValueError("separator is empty or none")
        self.separator = separator

        self.now_str = now_str

        self.now_fn = now_fn
        self.date_fn = date_fn


        if units_delta is not None:
            self.units_delta = units_delta.copy()
        else:
            self.units_delta = UNITS_DELTA_DEFAULT

        if units_round is not None:
            self.units_round = units_round.copy()
        else:
            self.units_round = UNITS_ROUND_DEFAULT

    def next(self, s):
        try:
            c = s[self.idx]
        except IndexError:
            raise ValueError("truncated input - expected character at position {} in {}, instead reached end of string".format(self,idx, s))
        self.idx += 1
        #LOG.debug("next({s}) = {c}, {self.idx}")
        return c

    def _parse_anchor(self, s):
        start = self.idx

        if self.now_str:
            now_len = len(self.now_str)
            if self.len - start >= now_len and s[start:now_len] == self.now_str:
                self.idx += now_len
                LOG.debug("_parse_anchor(%s) : now anchor tok [%i,%i)", s, start, self.idx)
                date = self.now_fn(self.timezone)
                return date

        idx = s.find(self.separator, start, self.len)
        if idx == -1:
            sep_offset = 0
            self.idx = self.len
            LOG.debug("_parse_anchor(%s) : no separator string %s", s, self.separator)
        else:
            sep_offset = len(self.separator)
            self.idx = idx + sep_offset
            LOG.debug("_parse_anchor(%s) : separator tok %s from [%i,%i)", s, self.separator, idx, sep_offset)

        end = self.idx - sep_offset
        LOG.debug("_parse_anchor(%s) : date anchor tok [%i,%i)", s, start, end)

        date = self.date_fn(s[start:end])

        if date.tzinfo is None and not self.timezone is None:
            LOG.debug("_parse_anchor(%s) : adding missing tzinfo to %s with %s", s, date, self.timezone)
            date = date.replace(tzinfo=self.timezone)

        return date

    def _parse_num(self, s):
        start = self.idx
        try:
            while s[self.idx] >= '0' and s[self.idx] <= '9':
                self.idx += 1
        except IndexError:
            raise ValueError("truncated input whilst parsing number - expected character at position {} in {}, instead reached end of string".format(self.idx, s))
        LOG.debug("_parse_num(%s) : num tok [%i,%i)", s, start, self.idx)
        return s[start:self.idx]

    def _parse_math(self, s):
        LOG.debug("_parse_math(%s : parsing math from [%i,%i)", s, self.idx, self.len)
        while self.idx < self.len:
            start = self.idx
            op = self.next(s)
            if op == '+' or op == '-':
                sign = -1 if op == '-' else 1

                num_s = self._parse_num(s)
                try:
                    num = int(num_s)
                except ValueError:
                    # It is valid to drop the number from arithmetic operations, e.g. +y instead of +1y.
                    # If the unit identifier is invalid, we will throw later in the code.
                    num = 1

                unit = self.next(s)
                try:
                    delta_fn = self.units_delta[unit]
                except KeyError:
                    valid_units = ', '.join(self.units_delta.keys())
                    raise ValueError("unit {} at position {} in {} not supported in arithmetic operation. valid units: {}".format(unit, self.idx-1, s, valid_units))

                #print(op, sign, num, delta)
                LOG.debug("_parse_math(%s) : delta expr [%i,%i)", s, start, self.idx)
                yield lambda d: delta_fn(d, sign * num)
            elif op == '/':
                unit = self.next(s)
                try:
                    round_fn = self.units_round[unit]
                except KeyError:
                    valid_units = ', '.join(self.units_round.keys())
                    raise ValueError("unit {} at position {} in {} not supported in rounding operation. valid units: {}".format(unit, self.idx-1, s, valid_units))
                #print(op, delta)
                LOG.debug("_parse_math(%s) : round expr [%i,%i)", s, start, self.idx)
                yield round_fn
            else:
                raise ValueError("operator {} at position {} in {} not supported. valid operators: +, -, /".format(op, self.idx-1, s))


    def parse_math(self, s, start=0):
        #LOG.debug("parse_math(%s) : called", s)
        self.idx = start
        self.len = len(s)

        # Consume until math.
        idx = s.find(self.separator)
        if idx == -1:
            LOG.debug("parse_math(%s) : consumed string, no separator %s", s, self.separator)
        else:
            LOG.debug("parse_math(%s) : consumed string, separator %s from [%i,%i)", s, self.separator, idx, sep_offset)
            self.idx = idx + len(self.separator)

        try:
            while not s[self.idx] in {'+', '-', '/'}:
                self.idx += 1
        except IndexError:
            # There is no math to math...
            LOG.debug("parse_math(%s) : consumed string with no math found", s)
            return

        math_fns = self._parse_math(s)
        yield from math_fns

    def eval_math(self, s, start=0):
        #LOG.debug("eval_math(%s) : called", s)
        it = self.parse_math(s, start)
        delta = timedelta(0)
        for fn in it:
            delta = fn(delta) # TODO Round does not work with deltas. Ignore or handle except
        return delta

    def parse(self, s, start=0): # NOTE Parse would be more accurately called "deserialize" or "loads"
        #LOG.debug("parse(%s) : called", s)
        self.idx = start
        self.len = len(s)

        anchor_date = self._parse_anchor(s)
        yield anchor_date

        if self.idx < self.len:
            math_fns = self._parse_math(s)
            yield from math_fns

    def eval(self, s, start=0):
        LOG.debug("eval(%s) : called", s)
        it = self.parse(s, start)
        date = next(it)
        for fn in it:
            date = fn(date)

        return date

if __name__ == "__main__":
    from datetime import timezone
    logging.basicConfig(level=logging.DEBUG)
    dm = DateMath(timezone=timezone(timedelta(hours=1)))
    for s in ("2014-11-18||/m+y", "2011-11-04||+1m/d",  "2011-11-04T00:01:11||/d+7d", "2011-11-04"):
        toks = dm.parse(s)
        print(s, next(toks), dm.eval(s))
