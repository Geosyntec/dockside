# dockside

[![Build Status](https://travis-ci.org/Geosyntec/dockside.svg?branch=master)](https://travis-ci.org/Geosyntec/dockside)
[![codecov](https://codecov.io/gh/Geosyntec/dockside/branch/master/graph/badge.svg)](https://codecov.io/gh/Geosyntec/dockside)

Download NWIS data without too much fuss

## Installation

```bash
pip install git+https://github.com/Geosyntec/dockside.git
```

## Example

```python
import dockside
gauge = '08075500'
output_folder = '01-raw-data'
sta = dockside.Station(gauge, '2018-01-01', '2018-11-24', '01-raw-data')
sta.insta_data.plot()
```
