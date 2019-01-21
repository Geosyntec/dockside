from pathlib import Path
from six.moves.urllib.request import urlopen

import pandas as pd

def _make_params(paramlist):

    if not isinstance(paramlist, list):
        paramlist = [paramlist]
    param_dict = {
        'flow': 'cb_00060=on&',
        'temp': 'cb_00010=on&',
        'stage': 'cb_00065=on&',
        'precip': 'cb_00045=on&'
    }

    params = ''
    for p in paramlist:
        params += param_dict[p]

    return '?' + params

def _make_url(site, params, start, end):
    urlstr = (r'https://nwis.waterdata.usgs.gov/nwis/uv/{}'
              r'format=rdb&site_no={}&period=&begin_date={}&end_date={}')

    paramlist = _make_params(params)

    url = urlstr.format(paramlist, site, start, end)
    return url

def get_raw_txt(site, params, start, end, path):

    folder = Path(path)
    if not folder.exists():
        folder.mkdir(exist_ok=True, parents=True)

    full_path = folder / ('_'.join([site, *params, start, end]) + '.txt')
    url = _make_url(site, params, start, end)

    if not full_path.exists():
        with full_path.open('wb') as openfile:
            response = urlopen(url)
            content = response.read()
            openfile.write(content)

    return full_path

def read_nwis(site, params, start, end, skiprows, path='data'):
    path = get_raw_txt(site, params, start, end, path)
    df = pd.read_csv(path, sep='\t', skiprows=skiprows, parse_dates=[2])

    return df
