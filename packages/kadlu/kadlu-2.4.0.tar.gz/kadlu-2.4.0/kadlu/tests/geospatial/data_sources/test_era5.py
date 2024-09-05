import kadlu
import numpy as np
from datetime import datetime, timedelta
from kadlu.geospatial.data_sources.data_util import reshape_4D
from kadlu.geospatial.data_sources.era5 import clear_cache_era5

# notes:
#  * with default settings, kadlu fetches data in lat/lon bins of 2 degrees and temporal bins of 1 day (24 hours)
#  * ERA5 HRES atmospheric data has a spatial resolution of 0.28125 degrees (31km while wave data have a resolution of 0.36 degrees
#  * ERA4 HRES temporal resolution is 1h


# test region: 1x1 degree area in middle of the north Atlantic; 3-hour time window
kwargs = dict(
    south=36.1,
    west=-39.2,
    north=37.1,
    east=-38.2,
    start=datetime(2024, 7, 1, 8, 0, 0),
    end=datetime(2024, 7, 1, 10, 0, 0),
    top=0,
    bottom=5000,
)


# clear any cached ERA5 data files
clear_cache_era5()


def test_era5_load_wave():
    """ Check that we can fetch and load wave data for the test region """
    val, lat, lon, time = kadlu.load(source='era5', var='waveheight', **kwargs)
    assert (len(val) == len(lat) == len(lon))
    assert len(np.unique(time)) == 3 #3 hours
    assert np.all(np.unique(lat) == [36.25, 36.50, 36.75, 37.00])
    assert np.all(np.unique(lon) == [-39.00, -38.75, -38.50, -38.25])
    assert np.all(np.logical_and(val >= 0, val <= 100))


def test_era5_load_irradiance():
    """ Check that we can fetch and load irradiance data for the test region """
    val, lat, lon, time = kadlu.load(source='era5', var='irradiance', **kwargs)
    assert (len(val) == len(lat) == len(lon))
    assert len(np.unique(time)) == 3 #3 hours
    assert np.all(np.unique(time) == [214759.5, 214760.5, 214761.5])
    assert np.all(np.unique(lat) == [36.25, 36.50, 36.75, 37.00])
    assert np.all(np.unique(lon) == [-39.00, -38.75, -38.50, -38.25])
    assert np.all(np.logical_and(val >= 0, val <= 1000))


def test_era5_irradiance_is_nonzero_during_daylight():
    """ Check that irradiance data is non-zero during day-light hours for a particular 
        location (Victoria, BC) and date (2024-07-19)
    """
    lat = 48.421
    lon = -123.383
    dt = datetime(2024, 7, 19, 0, 0, 0)
    kwargs = dict(
        south=lat-0.6,
        north=lat+0.6,
        west=lon-0.6,
        east=lon+0.6,
        start=dt,
        end=dt + timedelta(days=1),
    )
    data = kadlu.load(source='era5', var='irradiance', **kwargs)
    time = data[3]
    assert len(np.unique(time)) == 24 #hours
    n = len(np.unique(data[1]))
    m = len(np.unique(data[2]))
    k = len(np.unique(data[3]))
    v = np.reshape(data[0], newshape=(n,m,k), order="F")
    # last axis has UTC hours in increasing order 00, 01, ..., 23
    # Victoria BC is 7 hours behind UTC
    # day-light hours on July 19 are 5:33 AM to 9:05 PM local time
    # so we would expect the following UTC hour bins to have non-zero 
    # solar irradiance values: 0-4, 13-23
    assert np.all(v[0,0,:5] > 0) 
    assert np.all(v[0,0,5:13] == 0.) 
    assert np.all(v[0,0,13:] > 0) 


def test_era5_load_wind():
    """ Check that we can fetch and load wind data for the test region """
    val, lat, lon, time = kadlu.load(source='era5', var='wind_uv', **kwargs)
    assert (len(val) == len(lat) == len(lon))
    assert len(np.unique(time)) == 3 #3 hours
    assert np.all(np.unique(lat) == [36.25, 36.50, 36.75, 37.00])
    assert np.all(np.unique(lon) == [-39.00, -38.75, -38.50, -38.25])
    assert np.all(np.logical_and(val >= 0, val <= 100))


