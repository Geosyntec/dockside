# dockside
Download NWIS data without too much fuss

## Installation

```
pip install git+https://github.com/Geosyntec/dockside.git
```

## Example

```python
import dockside

gauge = '08075500'
output_folder = '01-raw-data'
sta = dockside.Station(gauge, ['flow', 'stage'], '2018-01-01', '2018-11-24', '01-raw-data')
sta.clean_data.plot()
```
