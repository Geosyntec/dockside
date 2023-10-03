from datetime import datetime

import numpy
import pandas
from pandas import Timestamp

from unittest import mock
import pytest
import pandas.testing as pdtest

from dockside import io


@pytest.fixture
def insta_ts_1():
    return {
        "variable": {
            "variableName": "Streamflow, ft&#179;/s",
            "unit": {"unitCode": "ft3/s"},
        },
        "values": [
            {
                "value": [
                    {
                        "value": "1.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:00:00.000-05:00",
                    },
                    {
                        "value": "1.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:15:00.000-05:00",
                    },
                    {
                        "value": "1.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:30:00.000-05:00",
                    },
                    {
                        "value": "1.82",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:45:00.000-05:00",
                    },
                    {
                        "value": "1.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T01:00:00.000-05:00",
                    },
                    {
                        "value": "1.81",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T01:15:00.000-05:00",
                    },
                ]
            }
        ],
    }


@pytest.fixture
def insta_ts_2():
    return {
        "variable": {"variableName": "Stage Elevation, ft", "unit": {"unitCode": "ft"}},
        "values": [
            {
                "value": [
                    {
                        "value": "54.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:00:00.000-05:00",
                    },
                    {
                        "value": "54.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:15:00.000-05:00",
                    },
                    {
                        "value": "54.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:30:00.000-05:00",
                    },
                    {
                        "value": "54.82",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:45:00.000-05:00",
                    },
                    {
                        "value": "54.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T01:00:00.000-05:00",
                    },
                    {
                        "value": "54.81",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T01:15:00.000-05:00",
                    },
                ]
            }
        ],
    }


@pytest.fixture
def daily_ts_1():
    return {
        "variable": {
            "variableName": "Streamflow, ft&#179;/s",
            "options": {
                "option": [
                    {"value": "Maximum", "name": "Statistic", "optionCode": "00001"}
                ]
            },
        },
        "values": [
            {
                "value": [
                    {
                        "value": "1.79",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:00:00.000",
                    },
                    {
                        "value": "1.12",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-02T00:00:00.000",
                    },
                    {
                        "value": "0.74",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-03T00:00:00.000",
                    },
                    {
                        "value": "0.67",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-04T00:00:00.000",
                    },
                    {
                        "value": "1.56",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-05T00:00:00.000",
                    },
                ]
            }
        ],
    }


@pytest.fixture
def daily_ts_2():
    return {
        "variable": {
            "variableName": "Streamflow, ft&#179;/s",
            "options": {
                "option": [
                    {"value": "Average", "name": "Statistic", "optionCode": "00002"}
                ]
            },
        },
        "values": [
            {
                "value": [
                    {
                        "value": "1.65",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-01T00:00:00.000",
                    },
                    {
                        "value": "1.04",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-02T00:00:00.000",
                    },
                    {
                        "value": "0.68",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-03T00:00:00.000",
                    },
                    {
                        "value": "0.65",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-04T00:00:00.000",
                    },
                    {
                        "value": "1.41",
                        "qualifiers": ["A"],
                        "dateTime": "2012-10-05T00:00:00.000",
                    },
                ]
            }
        ],
    }


@pytest.mark.parametrize(
    ("daily", "url"),
    [
        (
            True,
            "https://nwis.waterservices.usgs.gov/nwis/dv?format=json&sites=08071280&startDT=2012-10-01&endDT=2012-12-01",
        ),
        (
            False,
            "https://nwis.waterservices.usgs.gov/nwis/iv?format=json&sites=08071280&startDT=2012-10-01&endDT=2012-12-01",
        ),
    ],
)
def test_fetch_nwis(daily, url):
    site = "08071280"
    start = datetime(2012, 10, 1)
    end = "2012-12-01"
    r = io.fetch_nwis(site, start, end, daily=daily)
    assert r.url == url
    assert hasattr(r, "json")


def test__expand_columns():
    x = numpy.arange(12).reshape(3, 4)
    df = pandas.DataFrame(x, columns=("A_a", "A_b", "B_a", "B_c"))

    res_cols = pandas.MultiIndex(
        levels=[["A", "B"], ["a", "b", "c"]],
        codes=[[0, 0, 1, 1], [0, 1, 0, 2]],
        names=["top", "bottom"],
    )
    expected = pandas.DataFrame(x, columns=res_cols)
    result = io._expand_columns(df, ["top", "bottom"])
    pdtest.assert_frame_equal(result, expected)


def test__parse_ts_insta(insta_ts_1):
    expected = pandas.DataFrame(
        {
            ("Streamflow, ft&#179;/s", "qual"): {
                Timestamp("2012-10-01 05:00:00"): "A",
                Timestamp("2012-10-01 05:15:00"): "A",
                Timestamp("2012-10-01 05:30:00"): "A",
                Timestamp("2012-10-01 05:45:00"): "A",
                Timestamp("2012-10-01 06:00:00"): "A",
                Timestamp("2012-10-01 06:15:00"): "A",
            },
            ("Streamflow, ft&#179;/s", "value"): {
                Timestamp("2012-10-01 05:00:00"): 1.79,
                Timestamp("2012-10-01 05:15:00"): 1.79,
                Timestamp("2012-10-01 05:30:00"): 1.79,
                Timestamp("2012-10-01 05:45:00"): 1.82,
                Timestamp("2012-10-01 06:00:00"): 1.79,
                Timestamp("2012-10-01 06:15:00"): 1.81,
            },
        }
    )
    result = io._parse_ts(insta_ts_1, daily=False)
    pdtest.assert_frame_equal(
        result, expected, check_names=False, check_index_type=False
    )


def test__parse_ts_daily(daily_ts_1):
    expected = pandas.DataFrame(
        {
            ("Streamflow, ft&#179;/s", "Maximum", "qual"): {
                Timestamp("2012-10-01"): "A",
                Timestamp("2012-10-02"): "A",
                Timestamp("2012-10-03"): "A",
                Timestamp("2012-10-04"): "A",
                Timestamp("2012-10-05"): "A",
            },
            ("Streamflow, ft&#179;/s", "Maximum", "value"): {
                Timestamp("2012-10-01"): 1.79,
                Timestamp("2012-10-02"): 1.12,
                Timestamp("2012-10-03"): 0.74,
                Timestamp("2012-10-04"): 0.67,
                Timestamp("2012-10-05"): 1.56,
            },
        }
    )
    result = io._parse_ts(daily_ts_1, daily=True)
    pdtest.assert_frame_equal(result, expected, check_names=False)


def test_read_nwis_insta(insta_ts_1, insta_ts_2):
    expected = pandas.DataFrame(
        {
            ("Streamflow, ft&#179;/s", "qual"): {
                Timestamp("2012-10-01 05:00:00"): "A",
                Timestamp("2012-10-01 05:15:00"): "A",
                Timestamp("2012-10-01 05:30:00"): "A",
                Timestamp("2012-10-01 05:45:00"): "A",
                Timestamp("2012-10-01 06:00:00"): "A",
                Timestamp("2012-10-01 06:15:00"): "A",
            },
            ("Streamflow, ft&#179;/s", "value"): {
                Timestamp("2012-10-01 05:00:00"): 1.79,
                Timestamp("2012-10-01 05:15:00"): 1.79,
                Timestamp("2012-10-01 05:30:00"): 1.79,
                Timestamp("2012-10-01 05:45:00"): 1.82,
                Timestamp("2012-10-01 06:00:00"): 1.79,
                Timestamp("2012-10-01 06:15:00"): 1.81,
            },
            ("Stage Elevation, ft", "qual"): {
                Timestamp("2012-10-01 05:00:00"): "A",
                Timestamp("2012-10-01 05:15:00"): "A",
                Timestamp("2012-10-01 05:30:00"): "A",
                Timestamp("2012-10-01 05:45:00"): "A",
                Timestamp("2012-10-01 06:00:00"): "A",
                Timestamp("2012-10-01 06:15:00"): "A",
            },
            ("Stage Elevation, ft", "value"): {
                Timestamp("2012-10-01 05:00:00"): 54.79,
                Timestamp("2012-10-01 05:15:00"): 54.79,
                Timestamp("2012-10-01 05:30:00"): 54.79,
                Timestamp("2012-10-01 05:45:00"): 54.82,
                Timestamp("2012-10-01 06:00:00"): 54.79,
                Timestamp("2012-10-01 06:15:00"): 54.81,
            },
        }
    )
    site_json = {"value": {"timeSeries": [insta_ts_1, insta_ts_2]}}
    result = io.read_nwis(site_json, daily=False)
    pdtest.assert_frame_equal(
        result, expected, check_names=False, check_index_type=False
    )


def test_read_nwis_daily(daily_ts_1, daily_ts_2):
    expected = pandas.DataFrame(
        {
            ("Streamflow, ft&#179;/s", "Maximum", "qual"): {
                Timestamp("2012-10-01"): "A",
                Timestamp("2012-10-02"): "A",
                Timestamp("2012-10-03"): "A",
                Timestamp("2012-10-04"): "A",
                Timestamp("2012-10-05"): "A",
            },
            ("Streamflow, ft&#179;/s", "Maximum", "value"): {
                Timestamp("2012-10-01"): 1.79,
                Timestamp("2012-10-02"): 1.12,
                Timestamp("2012-10-03"): 0.74,
                Timestamp("2012-10-04"): 0.67,
                Timestamp("2012-10-05"): 1.56,
            },
            ("Streamflow, ft&#179;/s", "Average", "qual"): {
                Timestamp("2012-10-01"): "A",
                Timestamp("2012-10-02"): "A",
                Timestamp("2012-10-03"): "A",
                Timestamp("2012-10-04"): "A",
                Timestamp("2012-10-05"): "A",
            },
            ("Streamflow, ft&#179;/s", "Average", "value"): {
                Timestamp("2012-10-01"): 1.65,
                Timestamp("2012-10-02"): 1.04,
                Timestamp("2012-10-03"): 0.68,
                Timestamp("2012-10-04"): 0.65,
                Timestamp("2012-10-05"): 1.41,
            },
        }
    )
    site_json = {"value": {"timeSeries": [daily_ts_1, daily_ts_2]}}
    result = io.read_nwis(site_json, daily=True)
    pdtest.assert_frame_equal(result, expected, check_names=False)


@pytest.mark.parametrize(("daily", "header"), [(True, [0, 1, 2]), (False, [0, 1])])
def test_read_cache(daily, header):
    path = "path/to/csv.csv"
    datecol = [0]
    with mock.patch.object(pandas, "read_csv") as reader:
        io.read_cache(path, daily=daily)
        reader.assert_called_once_with(
            path, parse_dates=datecol, header=header, index_col=datecol
        )
