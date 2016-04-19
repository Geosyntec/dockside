import os
from six.moves.urllib.request import urlopen

import pandas as pd

def _make_params(paramlist):

    param_dict = {
        'flow': 'cb_00060=on&',
        'temp': 'cb_00010=on&',
    }

    params = ''
    for p in paramlist:
        params += param_dict[p]

    return '?' + params

def _make_url(site, params, start, end):
    urlstr = (r'http://nwis.waterdata.usgs.gov/usa/nwis/uv/{}'
              r'format=rdb&site_no={}&period=&begin_date={}&end_date={}')

    paramlist = _make_params(params)

    url = urlstr.format(paramlist, site, start, end)
    return url

def get_raw_txt(site, params, start, end, path):

    if not os.path.exists(path):
        os.makedirs(path)

    filename = '_'.join([site, *params, start, end]) + '.txt'
    full_path = os.path.join(path, filename)
    url = _make_url(site, params, start, end)

    if not os.path.exists(full_path):
        with open(full_path, 'wb') as openfile:
            response = urlopen(url)
            content = response.read()
            openfile.write(content)

    return full_path

def read_nwis(site, params, start, end, skiprows, path='data'):
    path = get_raw_txt(site, params, start, end, path)

    df = pd.read_csv(path, sep='\t', skiprows=skiprows)

    return df