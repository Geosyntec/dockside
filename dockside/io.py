from pathlib import Path

import requests
import pandas as pd


def fetch_nwis(site, start, end, daily=False, **kwargs):
    dtfmt = '%Y-%m-%d'
    url_base = "https://nwis.waterservices.usgs.gov/nwis/{}".format('dv' if daily else 'iv')
    url_params = {
        "format": kwargs.pop('format', 'json'),
        "sites": site,
        "startDT": pd.Timestamp(start).strftime(dtfmt),
        "endDT": pd.Timestamp(end).strftime(dtfmt),
        **kwargs
    }

    return requests.get(url_base, params=url_params)


def _expand_columns(df, names, sep='_'):
    newcols = df.columns.str.split(sep, expand=True)
    return (
        df.set_axis(newcols, axis='columns', inplace=False)
          .rename_axis(names, axis='columns')
    )


def _parse_ts(ts, daily):
    param = ts['variable']['variableName']
    if daily:
        stat = ts['variable']['options']['option'][0]['value']
    else:
        stat = None

    col_levels = {
        False: ['param', 'var'],
        True: ['param', 'stat', 'var']
    }
    sep = 'xxxxx'

    return (
        pd.DataFrame(ts['values'][0]['value'])
            .rename(columns=lambda c: '_orig_' + c)
            .assign(datetime=lambda df: pd.to_datetime(df['_orig_dateTime']))
            .assign(qual=lambda df: df['_orig_qualifiers'].map(lambda x: ','.join(x)))
            .assign(value=lambda df: df['_orig_value'].astype(float))
            .loc[:, lambda df: df.columns.map(lambda c: not c.startswith('_orig'))]
            .set_index('datetime')
            .rename(columns=lambda c: sep.join(filter(lambda x: bool(x), [param, stat, c])))
            .rename_axis('var', axis='columns')
            .pipe(_expand_columns, col_levels[daily], sep=sep)
    )


def read_nwis(site_json, daily=False):
    all_ts = site_json['value']['timeSeries']
    if len(all_ts) > 0:
        df = pd.concat([
            _parse_ts(ts, daily=daily)
            for ts in all_ts
        ], axis='columns')

        return df


def read_cache(fpath, daily=False):
    header = [0, 1]
    if daily:
        header.append(2)
    return pd.read_csv(fpath, parse_dates=[0], header=header, index_col=[0])
