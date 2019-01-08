from pathlib import Path

from pandas import Timestamp

from .io import fetch_nwis, read_nwis, read_cache


class Station(object):
    def __init__(self, site, start, end, savepath='data'):
        self.site = site
        self.start = Timestamp(start)
        self.end = Timestamp(end)
        self.savepath = Path('.' or savepath)

        self._daily_json = None
        self._insta_json = None
        self._daily_data = None
        self._insta_data = None

    def make_fpath(self, daily):
        datefmt = '%Y%m%d'
        suffix = 'daily' if daily else 'insta'
        fname = "_".join([
            f"{self.site}",
            self.start.strftime(datefmt),
            'thru',
            self.end.strftime(datefmt),
            suffix,
        ])
        return self.savepath / (fname + '.csv')

    @property
    def daily_json(self):
        if self._daily_json is None:
            self._daily_json = fetch_nwis(self.site, self.start, self.end,
                                          daily=True).json()
        return self._daily_json

    @property
    def insta_json(self):
        if self._insta_json is None:
            self._insta_json = fetch_nwis(self.site, self.start, self.end,
                                          daily=False).json()
        return self._insta_json

    @property
    def daily_data(self):
        if self._daily_data is None:
            self._daily_data = read_nwis(self.daily_json, daily=True)
        return self._daily_data

    @property
    def insta_data(self):
        if self._insta_data is None:
            self._insta_data = read_nwis(self.insta_json, daily=False)
        return self._insta_data

    def get_data(self, daily=False, save=False, force=False):
        fpath = self.make_fpath(daily=daily)
        if not fpath.exists() or force:
            df = read_nwis(self.site, self.start, self.end, daily=daily)
            if save:
                df.to_csv(fpath, encoding='utf-8')
        else:
            df = read_cache(fpath, daily=daily)
        return df
