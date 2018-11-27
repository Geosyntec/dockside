from matplotlib import pyplot
import pandas as pd

from .io import get_raw_txt, read_nwis, _make_url


class Station(object):
    def __init__(self, site, params, start, end, savepath='data'):
        self.site = site

        if not isinstance(params, list):
            self.params = [params]
        else:
            self.params = params
        self.start = start
        self.end = end
        self.savepath = savepath

        self.url = _make_url(site, self.params, start, end)
        self.path = get_raw_txt(site, self.params, start, end, savepath)

        self._skiprows = None
        self._rawdata = None
        self._clean_data = None
        self._header = None
        self.__parse_header = None

    @property
    def has_data(self):
        return self.path.exists() and (self.path.stat().st_size > 0)

    @property
    def _parse_header(self):
        if self.has_data and self.__parse_header is None:
            with self.path.open('r') as openfile:
                header = ''
                for n, line in enumerate(openfile):
                    header += line
                    if '#' not in line:
                        break
                self.__parse_header = (header, n)
        return self.__parse_header

    @property
    def header(self):
        if self._parse_header and self._header is None:
            self._header = self._parse_header[0]
        return self._header

    @property
    def skiprows(self):
        if self._parse_header and self._skiprows is None:
            self._skiprows = self._parse_header[1]
        return self._skiprows

    def _columns(self, start='# Data provided for site',
                 end='# Data-value qualification codes included'):

        cols = []
        if self.has_data:
            append = False
            for n, line in enumerate(self.header.split('\n')):
                if start in line:
                    append = True
                if end in line:
                    append = False

                if append:
                    cols.append(line)

            cols = cols[2:-1]
            cols = [[__ for __ in _.strip('#').split(' ') if __ != ''] for _ in cols]
            cols = {'_'.join(_[:2]):' '.join(_[2:]) for _ in cols}
            cols.update({a + '_cd': 'Qual ' + b for a, b in cols.items()})
        return cols

    @property
    def rawdata(self):
        if self.has_data and self._rawdata is None:
            data = read_nwis(self.site, self.params, self.start,
                self.end, self.skiprows, path=self.savepath)
            self._rawdata = data
        return self._rawdata

    @property
    def clean_data(self):
        if self.rawdata is not None:
            data = (self.rawdata.rename(columns=self._columns())
                                .drop([0], axis=0)
                                .assign(site_name=lambda df: df.agency_cd.astype(str) + df.site_no.astype(str))
                                .assign(datetime=lambda df: df.datetime.apply(lambda dt: pd.Timestamp(dt)))
                                .drop(['agency_cd', 'site_no'], axis=1)
                                .set_index(['site_name', 'datetime', 'tz_cd'])
            )

            for numeric in [a for a in self._columns().values() if 'Qual' not in a]:
                data[numeric] = pd.to_numeric(data[numeric])

        return data