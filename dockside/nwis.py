import pandas as pd

from .io import get_raw_txt, read_nwis, _make_url


class Station(object):
    def __init__(self, site, params, start, end, savepath='data'):
        self.site = site
        self.params = params
        self.start = start
        self.end = end
        self.savepath = savepath

        self.url = _make_url(site, params, start, end)
        self.path = get_raw_txt(site, params, start, end, savepath)

        self._skiprows = None
        self._rawdata = None
        self._clean_data = None
        self._header = None
        self.__parse_header = None

    @property
    def _parse_header(self):
        if self.__parse_header is None:
            with open(self.path, 'r') as openfile:
                header = ''
                for n, line in enumerate(openfile):
                    header += line
                    if '#' not in line:
                        break
            self.__parse_header = (header, n)
        return self.__parse_header

    @property
    def header(self):
        if self._header is None:
            self._header = self._parse_header[0]
        return self._header

    @property
    def skiprows(self):
        if self._skiprows is None:
            self._skiprows = self._parse_header[1]
        return self._skiprows

    def _columns(self, start='# Data provided for site',
        end='# Data-value qualification codes included'):

        cols = []
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
        if self._rawdata is None:
            data = read_nwis(self.site, self.params, self.start,
                self.end, self.skiprows, path=self.savepath)
            self._rawdata = data
        return self._rawdata

    @property
    def clean_data(self):
        if self._clean_data is None:
            data = (self.rawdata.rename(columns=self._columns())
                                .drop([0], axis=0)
                                .assign(site_name=lambda df: str(df.agency_cd +) str(df.site_no))
                                .drop(['agency_cd', 'site_no'], axis=1)
                                .set_index(['site_name', 'datetime', 'tz_cd'])
            )

        return data