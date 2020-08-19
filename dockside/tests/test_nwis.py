from pathlib import Path
from pkg_resources import resource_filename
from textwrap import dedent
from tempfile import TemporaryDirectory

import pandas

from unittest.mock import patch
import pytest

from dockside import nwis


class FakeResponse:
    def json(self):
        return "fake json response"


@pytest.fixture
def station():
    with TemporaryDirectory() as datadir:
        yield nwis.Station(14211500, "2018-10-01", "2018-10-30", savepath=datadir)


@pytest.mark.parametrize(
    ("daily", "expected"),
    [
        (True, "14211500_20181001_thru_20181030_daily.csv"),
        (False, "14211500_20181001_thru_20181030_insta.csv"),
    ],
)
def test_station__make_fpath(station, daily, expected):
    assert station._make_fpath(daily) == station.savepath / expected


@patch.object(nwis, "fetch_nwis", return_value=FakeResponse())
def test_daily_json(fetch, station):
    # call once, use cached property, check .json() was used, assert only 1 call
    data = station.daily_json
    data2 = station.daily_json

    assert data == data2 == "fake json response"
    fetch.assert_called_once_with(station.site, station.start, station.end, daily=True)


@patch.object(nwis, "fetch_nwis", return_value=FakeResponse())
def test_insta_json(fetch, station):
    # call once, use cached property, check .json() was used, assert only 1 call
    data = station.insta_json
    data2 = station.insta_json

    assert data == data2 == "fake json response"
    fetch.assert_called_once_with(station.site, station.start, station.end, daily=False)


@patch.object(nwis, "read_nwis", return_value="fake data")
@patch.object(nwis, "fetch_nwis", return_value=FakeResponse())
def test_daily_data(fetch, read, station):
    # call once, use cached property, check .data() was used, assert only 1 call
    data = station.daily_data
    data2 = station.daily_data

    assert data == data2 == "fake data"
    fetch.assert_called_once_with(station.site, station.start, station.end, daily=True)
    read.assert_called_once_with("fake json response", daily=True)


@patch.object(nwis, "read_nwis", return_value="fake data")
@patch.object(nwis, "fetch_nwis", return_value=FakeResponse())
def test_insta_data(fetch, read, station):
    # call once, use cached property, check .data() was used, assert only 1 call
    data = station.insta_data
    data2 = station.insta_data

    assert data == data2 == "fake data"
    fetch.assert_called_once_with(station.site, station.start, station.end, daily=False)
    read.assert_called_once_with("fake json response", daily=False)


@pytest.mark.parametrize(
    ("daily", "fname"),
    [
        (True, "14211500_20181001_thru_20181030_daily.csv"),
        (False, "14211500_20181001_thru_20181030_insta.csv"),
    ],
)
@pytest.mark.parametrize("save", [True, False])
@pytest.mark.parametrize("force", [True, False])
@pytest.mark.parametrize("exists", [True, False])
@patch.object(nwis, "read_cache", return_value="fake data")
@patch.object(nwis, "read_nwis", return_value=pandas.DataFrame())
def test_station_get_data(
    nwis_reader, cache_reader, station, daily, fname, save, force, exists
):
    fpath = station.savepath / fname
    with patch("pathlib.Path.exists", return_value=exists):
        with patch("pandas.DataFrame.to_csv", return_value=None) as to_csv:
            data = station.get_data(daily=daily, save=save, force=force)
            if not exists or force:
                nwis_reader.assert_called_once_with(
                    station.site, station.start, station.end, daily=daily
                )
                if save:
                    to_csv.assert_called_once_with(fpath, encoding="utf-8")
            else:
                cache_reader.assert_called_once_with(fpath, daily=daily)
