from __future__ import absolute_import

# import - third-party packages
import requests
import warnings
import pandas as pd
from six import string_types
import os
import collections
import numbers
from datetime import datetime

# module import
from janus.config.app import AppConfig
from janus.util import Entity
from janus.util.color import Color
from janus.util.base import TYPE_ERROR_STRING

class Ticker(Entity):
    def __init__(self, ticker, start=None, end=None):
        envvar = AppConfig.ENVIRONMENT_VARIABLE['tiingo_api_key']
        config = {}
        if not _check_environment_variable_set(envvar):
            message = Color.warn("Environment variable {envvar} for Tiingo not configure correctly ")

            warnings.warn(message)
        else:
            self.tiingo_token = os.getenv(envvar)
        self.ticker = ticker
        self.fetch_tiingo_data(start=start, end=end)
    def update(self, start=None, end=None):
        self.data = self.fetch_tiingo_data(self.ticker, start, end)
        self.length  =  len(self.data)
        self.attrs   = list(self.data.columns)

    def fetch_tiingo_data(self, ticker, d_start, d_end):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.tiingo_token
        }
        url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + d_start + "&endDate=" + d_end

        # print url
        requestResponse = requests.get(url, headers=headers)
        json_result = requestResponse.json()

        df = pd.DataFrame.from_records(json_result)

        if not 'adjClose' in df.columns:
            if 'close' in df.columns:
                df['adjClose'] = df['close']
            else:
                print("Error: No Close information")
                return

        # Convert ISO date format to Pandas DateTime
        df['date'] = pd.to_datetime(df['date'])
        # Align Column Names to previous DataReader names
        df = df.rename(
            columns={'date': 'Date', 'open': 'Open', 'adjClose': 'Adj Close', 'volume': 'Volume', 'high': 'High',
                     'low': 'Low', 'close': 'Close'})
        financial_data = df.set_index(['Date'])
        return financial_data

def _raise_type_error(expected_type_name, recieved_type_name):
    raise TypeError(TYPE_ERROR_STRING.format(
        expected_type_name = expected_type_name,
        recieved_type_name = recieved_type_name
    ))

def _get_type_name(o):
    type_ = type(o)
    name  = type_.__name__

    return name

def _get_datetime_str(dt, format_):
    if _check_type(dt, pd.Timestamp):
        dt = dt.to_pydatetime()

    _check_type(dt, type_ = datetime, raise_err = True, expected_type_name = 'datetime.datetime')

    string = dt.strftime(format_)

    return string

def _check_type(o, type_, raise_err = False, expected_type_name = None):
    if not isinstance(o, type_):
        if raise_err:
            _raise_type_error(
                expected_type_name = expected_type_name,
                recieved_type_name = _get_type_name(o)
            )
        else:
            return False
    else:
        return True

def _check_str(o, raise_err = False):
    return _check_type(o, string_types, raise_err = raise_err, expected_type_name = 'str')

def _check_int(o, raise_err = False):
    return _check_type(o, numbers.Integral, raise_err = raise_err, expected_type_name = 'int')

def _check_real(o, raise_err = False):
    return _check_type(o, numbers.Real, raise_err = raise_err, expected_type_name = '(int, float)')

def _check_pandas_series(data, raise_err = False):
    return _check_type(data, pd.Series, raise_err = raise_err, expected_type_name = 'pandas.Series')

def _check_pandas_dataframe(data, raise_err = False):
    return _check_type(data, pd.DataFrame, raise_err = raise_err, expected_type_name = 'pandas.DataFrame')

def _check_iterable(o, raise_err = False):
    return _check_type(o, collections.Iterable, raise_err = raise_err, expected_type_name = '(str, list, tuple)')

def _check_sequence(o, string = True, raise_err = False):
    return _check_type(o, collections.Sequence, raise_err = raise_err, expected_type_name = '(list, tuple)')

def _check_environment_variable_set(variable, raise_err = False):
    _check_str(variable, raise_err = raise_err)

    try:
        os.environ[variable]
    except KeyError:
        if raise_err:
            raise ValueError('Environment variable {variable} not set.')
        else:
            return False

    return True

def _validate_in_range(value, low, high, raise_err = False):
    if not low <= value <= high:
        if raise_err:
            raise ValueError('{value} out of bounds, must be in range [{low}, {high}].'.format(
                value = value,
                low   = low,
                high  = high
            ))
        else:
            return False
    else:
        return True

def _validate_date(value, format_ = '%Y-%m-%d', raise_err = False):
    _check_str(value, raise_err = raise_err)

    try:
        datetime.strptime(value, format_)
    except ValueError:
        if raise_err:
            raise ValueError('Expected {format_} format, got {value} instead.'.format(
                format_ = format_,
                value   = value
            ))
        else:
            return False

    return True

def _assign_if_none(a, b):
    return b if a is None else a

def _is_sequence_all(seq):
    _check_sequence(seq, raise_err = True)

    length = len(seq)
    is_seq = True if length != 0 and seq.count(seq[0]) == length else False

    return is_seq