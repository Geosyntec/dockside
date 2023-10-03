from pathlib import Path

import requests
import pandas as pd


def fetch_nwis(site, start, end, daily=False, **kwargs):
    """Fetch JSON data from NWIS

    Parameters
    ----------
    site : int, string, or sequence
        Site ID number from NWIS. E.g, site = 14211500 or site = '14211500' for
        Johnson Creek in Portland, OR. This can also be a list-like object for
        multiple sites (experimental).
    start, end : string or date-like
        Some form of date representation for the start and end of the NWIS
        observations you'd like to download
    daily : bool (default is False)
        Toggles downloading daily (True) or instanteous values (False, default)

    Additional Parameters
    ---------------------
    All additional keyword arguments are passed directly to the NWIS API.

    Returns
    -------
    request
        A request object representing the API call to fetch the data.

    Examples
    --------
    >>> import json
    >>> from tempfile import TemporaryDirectory
    >>> from pathlib import Path
    >>> from dockside.io import fetch_nwis, read_nwis
    >>> r = fetch_nwis(14211500, '2018-01-01', '2018-06-30', daily=False)
    >>> with TemporaryDirectory() as td:
    ...     fpath = Path(td) / 'JCreek_flow.json'
    ...     with fpath.open('w') as fp:
    ...         json.dump(r.json(), fp)

    """

    dtfmt = "%Y-%m-%d"
    url_base = "https://nwis.waterservices.usgs.gov/nwis/{}".format(
        "dv" if daily else "iv"
    )
    url_params = {
        "format": kwargs.pop("format", "json"),
        "sites": site,
        "startDT": pd.Timestamp(start).strftime(dtfmt),
        "endDT": pd.Timestamp(end).strftime(dtfmt),
        **kwargs,
    }

    return requests.get(url_base, params=url_params)


def _expand_columns(df, names, sep="_"):
    """
    Splits string column labels into tuples
    """

    newcols = df.columns.str.split(sep, expand=True)
    return df.set_axis(newcols, axis="columns").rename_axis(names, axis="columns")


def _parse_ts(ts, daily):
    """
    Parses a single `timeSeries` object in an NWIS JSON response in a dataframe
    """

    param = ts["variable"]["variableName"]
    if daily:
        stat = ts["variable"]["options"]["option"][0]["value"]
    else:
        stat = None

    col_levels = {False: ["param", "var"], True: ["param", "stat", "var"]}
    sep = "xxxxx"

    return (
        pd.DataFrame(ts["values"][0]["value"])
        .rename(columns=lambda c: "_orig_" + c)
        .assign(datetime=lambda df: pd.to_datetime(df["_orig_dateTime"]))
        .assign(qual=lambda df: df["_orig_qualifiers"].map(lambda x: ",".join(x)))
        .assign(value=lambda df: df["_orig_value"].astype(float))
        .loc[:, lambda df: df.columns.map(lambda c: not c.startswith("_orig"))]
        .set_index("datetime")
        .rename(columns=lambda c: sep.join(filter(lambda x: bool(x), [param, stat, c])))
        .rename_axis("var", axis="columns")
        .pipe(_expand_columns, col_levels[daily], sep=sep)
    )


def read_nwis(site_json, daily=False):
    """Read an NWIS JSON response to a pandas Dataframe

    Parameters
    ----------
    site_json : json-like
        JSON response from an API call to NWIS
    daily : bool (default is False)
        Set to True if you're parsing daily values or False (default) if they
        they are instanteous values.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> from dockside.io import fetch_nwis, read_nwis
    >>> r = fetch_nwis(14211500, '2018-01-01', '2018-06-30', daily=True)
    >>> df = read_nwis(r.json(), daily=True)

    """

    all_ts = site_json["value"]["timeSeries"]
    if len(all_ts) > 0:
        df = pd.concat([_parse_ts(ts, daily=daily) for ts in all_ts], axis="columns")

        return df


def read_cache(fpath, daily=False):
    """Reads a previouly cached dataframe created with `read_nwis`

    Parameters
    ----------
    fpath : path-like
        File path to the cached data
    daily : bool (default is False)
        Set to True if you're parsing daily values or False (default) if they
        they are instanteous values.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> from tempfile import TemporaryDirectory
    >>> from pathlib import Path
    >>> from dockside.io import fetch_nwis, read_nwis, read_cache
    >>> r = fetch_nwis(14211500, '2018-01-01', '2018-06-30', daily=True)
    >>> with TemporaryDirectory() as td:
    ...     fpath = Path(td) / 'cached_flow.csv'
    ...     df1 = read_nwis(r.json(), daily=True)
    ...     df1.to_csv(fpath)
    ...     df2 = read_cache(fpath, daily=True)
    """

    header = [0, 1]
    if daily:
        header.append(2)
    return pd.read_csv(fpath, parse_dates=[0], header=header, index_col=[0])
