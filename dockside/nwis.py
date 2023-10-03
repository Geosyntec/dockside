from pathlib import Path

from pandas import Timestamp

from .io import fetch_nwis, read_nwis, read_cache


class Station(object):
    """USGS Station and download helpers

    Parameters
    ----------
    site : int, string, or sequence
        Site ID number from NWIS. E.g, site = 14211500 or site = '14211500' for
        Johnson Creek in Portland, OR. This can also be a list-like object for
        multiple sites (experimental).
    start, end : string or date-like
        Start and end dates for the period of interest.
    savepath : path-like
        Path to where data would be saved when using the `get_data` method.

    """

    def __init__(self, site, start, end, savepath="data"):
        self.site = site
        self.start = Timestamp(start)
        self.end = Timestamp(end)
        self.savepath = Path("." or savepath)

        self._daily_json = None
        self._insta_json = None
        self._daily_data = None
        self._insta_data = None

    def _make_fpath(self, daily):
        datefmt = "%Y%m%d"
        suffix = "daily" if daily else "insta"
        fname = "_".join(
            [
                f"{self.site}",
                self.start.strftime(datefmt),
                "thru",
                self.end.strftime(datefmt),
                suffix,
            ]
        )
        return self.savepath / (fname + ".csv")

    @property
    def daily_json(self):
        if self._daily_json is None:
            self._daily_json = fetch_nwis(
                self.site, self.start, self.end, daily=True
            ).json()
        return self._daily_json

    @property
    def insta_json(self):
        if self._insta_json is None:
            self._insta_json = fetch_nwis(
                self.site, self.start, self.end, daily=False
            ).json()
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
        """
        Fetch and save data for the site.

        Parameters
        ----------
        daily : bool (default False)
            Toggles fetching either instaneous (False) or daily values (True).
        save : bool (defaut False)
            Toggles saving the downloaded data to `site.savepath`
        force : bool (defaut False)
            If True and the data has already been downloaded and save, this
            will force the redownloading of the data.

        Returns
        -------
        pandas.DataFrame

        Note
        ----
        Unless readying from a cache, this method *always* redownloads the data,
        even with multiple calls, instead of relying on the `daily_data` and
        `insta_data` properties of the class.

        """

        fpath = self._make_fpath(daily=daily)

        if not fpath.exists() or force:
            df = read_nwis(self.site, self.start, self.end, daily=daily)
            if save:
                df.to_csv(fpath, encoding="utf-8")
        else:
            df = read_cache(fpath, daily=daily)
        return df
