"""
    API for Era5 dataset from Copernicus Climate Datastore.

    Note: Initial release data (ERA5T) are available about 5 days behind real time.

    Dataset summary:
        https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview

    Detailed information about the dataset:
        https://confluence.ecmwf.int/display/CKB/ERA5

    API documentation:
        https://cds.climate.copernicus.eu/toolbox/doc/api.html
"""

import os
import logging
import configparser
import warnings
import platform
from os.path import isfile, dirname
from glob import glob
from datetime import datetime, timedelta
import cdsapi
import numpy as np

if platform.machine() == 'arm64':
    warnings.warn(
        "ERA5 module requires the pygrib package which is not available for this platform"
    )
else:
    import pygrib

from kadlu import index
from kadlu.geospatial.data_sources.data_util import (
    database_cfg,
    dt_2_epoch,
    logmsg,
    logmsg_nodata,
    storage_cfg,
    str_def,
)

"""
    Names of the tables that will be created in the kadlu geospatial.db database for storing ERA5.

    OBS: Table names must match the variable names used by ERA5 
"""
era5_tables = [
    'significant_height_of_combined_wind_waves_and_swell',
    'mean_wave_direction',
    'mean_wave_period',
    'u_component_of_wind',
    'v_component_of_wind',
    'convective_precipitation',
    'convective_snowfall',
    'normalized_energy_flux_into_ocean',
    'normalized_energy_flux_into_waves',
    'normalized_stress_into_ocean',
    'precipitation_type',
    'surface_solar_radiation_downwards',  #https://codes.ecmwf.int/grib/param-db/169
]


logging.getLogger('cdsapi').setLevel(logging.WARNING)


def initdb():
    """ Create tables in kadlu's geospatial.db database for storing ERA5 data"""
    conn, db = database_cfg()
    for var in era5_tables:
        db.execute(f'CREATE TABLE IF NOT EXISTS {var}'
                   '( val     REAL    NOT NULL, '
                   '  lat     REAL    NOT NULL, '
                   '  lon     REAL    NOT NULL, '
                   '  time    INT     NOT NULL, '
                   '  source  TEXT    NOT NULL) ')
        db.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS '
                   f'idx_{var} on {var}(time, lon, lat, val, source)')
    conn.close()


def era5_cfg(key=None, url=None):
    """ Configure URL and Key for accessing ERA5 data via the CDS API.
    
        Args:
            key: str 
                API access key. If not specified, the default Kadlu key will be used
            url: str
                URL address. If not specified, will be set to https://cds.climate.copernicus.eu/api/v2
    """
    cfg = configparser.ConfigParser()  # read .ini into dictionary object
    cfgfile = os.path.join(dirname(dirname(dirname(dirname(__file__)))), "config.ini")
    cfg.read(cfgfile)

    if 'cdsapi' not in cfg.sections():
        cfg.add_section('cdsapi')

    if key is not None:
        cfg.set('cdsapi', 'key', key)
        with open(cfgfile, 'w') as f:
            cfg.write(f)
    else:
        cfg.set('cdsapi', 'key', '20822:2d1c1841-7d27-4f72-bb8a-9680a073b4c3')
        with open(cfgfile, 'w') as f:
            cfg.write(f)

    if url is not None:
        cfg.set('cdsapi', 'url', url)
        with open(cfgfile, 'w') as f:
            cfg.write(f)
    else:
        cfg.set('cdsapi', 'url', 'https://cds.climate.copernicus.eu/api/v2')
        with open(cfgfile, 'w') as f:
            cfg.write(f)
    
    return


def clear_cache_era5():
    """ Removes all files with the filename pattern ERA5_*.grb2 in the Kadlu storage directory"""
    logger = logging.getLogger("kadlu")

    # path to folder where Kadlu stores data
    dir_path = storage_cfg()

    if not os.path.exists(dir_path):
        warn_msg = f"Failed to clear ERA5 cache. Kadlu data storage directory not found at {dir_path}."
        logger.warning(warn_msg)
        return
    
    # find all ERA5 grib files
    paths = glob(os.path.join(dir_path, "ERA5_*.grb2"))    

    if len(paths) == 0:
        info_msg = f"ERA5 cache is empty."
        logger.info(info_msg)
        return

    # get their size and remove them
    bytes = 0
    for path in paths:
        bytes += os.path.getsize(path)
        os.remove(path)

    info_msg = f"Emptied ERA5 cache (deleted {len(paths)} files, {bytes/1E6:.1f} MB)"
    logger.info(info_msg)


def fetch_era5(var, *, west, east, south, north, start, **_):
    """ Fetch global ERA5 data for specified variable, geographic region, and time range.

        Downloads 24-hours of global data on the specified day, and saves these data to 
        a *.grb2 file in the kadlu data storage directory, using the recommended spatial 
        resolution of 0.25 x 0.25 degrees.

        The *.grb2 file can be deleted manually by calling the `clear_cache_era5` function 
        to save disk space, if necessary.

        Only data within the specified geographic boundaries (`west`, `east`, `south`, `north`) 
        are inserted into the kadlu geospatial.db database.

        args:
            var: string
                The variable short name of desired wave parameter according to ERA5 docs. 
                The complete list can be found here (table 7 for wave params):
                https://confluence.ecmwf.int/display/CKB/ERA5+data+documentation#ERA5datadocumentation-Temporalfrequency
            west,east,south,north: float
                Geographic boundaries of the data request
            start: datetime.datetime
                UTC date of the data request. 24-hours of data will be fetched.
                
        return:
            True if new data was fetched, else False
    """
    logger = logging.getLogger("kadlu")

    # cleaner stack trace by raising error outside of try/except
    err = False

    # configure access to CDS API
    era5_cfg()
    cfg = configparser.ConfigParser()  # read .ini into dictionary object
    cfgfile = os.path.join(dirname(dirname(dirname(dirname(__file__)))),
                           "config.ini")
    cfg.read(cfgfile)

    # attempt connecting to the CDS API
    try:
        client = cdsapi.Client(url=cfg['cdsapi']['url'], key=cfg['cdsapi']['key'])
    except KeyError:
        try:
            client = cdsapi.Client()
        except Exception:
            err = True

    # if attempt fails, raise an error
    if err:
        raise KeyError('CDS API has not been configured for the ERA5 module. '
                       'obtain an API token from the following URL and run '
                       'kadlu.era5_cfg(url="URL_HERE", key="TOKEN_HERE"). '
                       'https://cds.climate.copernicus.eu/api-how-to')

    # form request
    # note: we use the recommended spatial resolution of 0.25 x 0.25 degrees
    # https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference

    t = datetime(start.year, start.month, start.day)
    times = [datetime(t.year, t.month, t.day, h).strftime('%H:00') for h in range(24)]

    request = {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': var,
        'year': t.strftime("%Y"),
        'month': t.strftime("%m"),
        'day': t.strftime("%d"),
        'time': times,
        'grid': [0.25, 0.25], 
    }

    # download the data and save as *.grb2 file
    fname = f'ERA5_reanalysis_{var}_{t.strftime("%Y-%m-%d")}.grb2'
    fpath = f'{storage_cfg()}{fname}'
    if not isfile(fpath):
        logger.info(f'fetching {fpath}...')
        client.retrieve(
            'reanalysis-era5-single-levels', 
            request, 
            fpath
        )

    # load the data from the *.grb2 file and insert it into the database
    assert isfile(fpath)
    grb = pygrib.open(fpath)
    data = np.array([[], [], [], [], []])
    table = var[4:] if var[0:4] == '10m_' else var

    # process data 'messages' 
    for msg in grb:
        # timestamp
        dt = msg.validDate

        # for forecasts, 'validDate' represents the start time of the forecast (06:00 UTC or 18:00 UTC)
        # so we must add the appropriate number of hourly steps
        # https://confluence.ecmwf.int/pages/viewpage.action?pageId=85402030
        #  
        # for accumulated quantities we should subtracting 1/2 hour to get the time at the center of the 
        # forecast bin; however, since our database stores times as INTs (hours since 2000-01-01), we 
        # instead subtract 1/2 hour when the data is loaded from the database
        
        step = msg.step
        ###if msg.stepType == "accum":
        ###    step -= 0.5

        dt += timedelta(seconds = step * 3600)

        debug_msg = f"[ERA5] Processing message with timestamp {dt} (step={step}) ..."
        logger.debug(debug_msg)

        # read grib data (value, lat, lon)
        z, y, x = msg.data()
        if np.ma.is_masked(z):
            z2 = z[~z.mask].data
            y2 = y[~z.mask]
            x2 = x[~z.mask]
        else:  # wind data has no mask
            z2 = z.reshape(-1)
            y2 = y.reshape(-1)
            x2 = x.reshape(-1)

        # ERA5 uses longitude values in the range [0;360] referenced to the Greenwich Prime Meridian
        # convert to longitude to [-180;180]
        x3 = ((x2 + 180) % 360) - 180

        # index coordinates, select query range subset
        xix = np.logical_and(x3 >= west, x3 <= east)
        yix = np.logical_and(y2 >= south, y2 <= north)
        idx = np.logical_and(xix, yix)

        # collect data in a list (values, lats, lons, times, source)
        msg_data = [
            z2[idx], y2[idx], x3[idx], dt_2_epoch([dt for i in z2[idx]]), ['era5' for i in z2[idx]]
        ]

        # aggregate data
        data = np.hstack((data, msg_data))

    # perform the insertion into the database
    initdb()
    conn, db = database_cfg()
    n1 = db.execute(f"SELECT COUNT(*) FROM {table}").fetchall()[0][0]
    db.executemany(
        f"INSERT OR IGNORE INTO {table} "
        f"VALUES (?,?,?,CAST(? AS INT),?)", data.T)
    n2 = db.execute(f"SELECT COUNT(*) FROM {table}").fetchall()[0][0]
    db.execute("COMMIT")
    conn.commit()
    conn.close()

    # log message
    kwargs = dict(
        south = south,
        west = west,
        north = north,
        east = east,
        start = t,
        end = t + timedelta(hours=24)     
    )
    logmsg('era5', var, (n1, n2), **kwargs)
    
    return True


def load_era5(var, *, west, east, south, north, start, end, **_):
    """ Load ERA5 data from local geospatial.db database

        Args:
            var: str
                Variable to be fetched
            west,east,south,north: float
                Geographic boundaries of the data request
            start: datetime.datetime
                UTC start time for the data request.
            end: datetime.datetime
                UTC end time for the data request.

        Returns:
            values:
                values of the fetched var
            lat:
                y grid coordinates
            lon:
                x grid coordinates
            epoch:
                timestamps in epoch hours since jan 1 2000
    """
    # Check local database for data.
    # Fetch data from CDS API, if missing.
    with index(storagedir=storage_cfg(),
               west=west,
               east=east,
               south=south,
               north=north,
               start=start,
               end=end) as fetchmap:
        fetchmap(callback=fetch_era5, var=var)

    # query local database for data
    table = var[4:] if var[0:4] == '10m_' else var  # table name can't start with int
    sql_query_list = [f"SELECT * FROM {table} WHERE lat >= ?", 'lat <= ?', 'lon >= ?', 'lon <= ?', 'time >= ?', 'time <= ?']
    sql_query = ' AND '.join(sql_query_list) + ' ORDER BY time, lat, lon ASC'
    sql_values = tuple(
        map(str, [south, north, west, east, dt_2_epoch(start), dt_2_epoch(end)])
    )
    conn, db = database_cfg()
    db.execute(sql_query, sql_values)
    rowdata = np.array(db.fetchall(), dtype=object).T
    conn.close()

    # if no data was found, return empty arrays and log info
    if len(rowdata) == 0:
        logmsg_nodata(
            'era5', var,
            west=west, east=east, south=south, north=north,
            start=start, end=end
        )
        return np.array([[], [], [], []])

    val, lat, lon, epoch, source = rowdata
    return np.array((val, lat, lon, epoch), dtype=float)


class Era5():
    """ Collection of module functions for fetching and loading.
    
        The functions return (values, lat, lon, epoch) numpy arrays with 
        shape (num_points, 4) where epoch is the number of hours since 2000-01-01.
    """

    def load_windwaveswellheight(self, **kwargs):
        return load_era5('significant_height_of_combined_wind_waves_and_swell',
                         **kwargs)

    def load_wavedirection(self, **kwargs):
        return load_era5('mean_wave_direction', **kwargs)

    def load_waveperiod(self, **kwargs):
        return load_era5('mean_wave_period', **kwargs)

    def load_precipitation(self, **kwargs):
        return load_era5('convective_precipitation', **kwargs)

    def load_snowfall(self, **kwargs):
        return load_era5('convective_snowfall', **kwargs)

    def load_flux_ocean(self, **kwargs):
        return load_era5('normalized_energy_flux_into_ocean', **kwargs)

    def load_flux_waves(self, **kwargs):
        return load_era5('normalized_energy_flux_into_waves', **kwargs)

    def load_stress_ocean(self, **kwargs):
        return load_era5('normalized_stress_into_ocean', **kwargs)

    def load_precip_type(self, **kwargs):
        return load_era5('precipitation_type', **kwargs)

    def load_wind_u(self, **kwargs):
        return load_era5('10m_u_component_of_wind', **kwargs)

    def load_wind_v(self, **kwargs):
        return load_era5('10m_v_component_of_wind', **kwargs)
    
    def load_insolation(self, **kwargs):
        data = load_era5('surface_solar_radiation_downwards', **kwargs)
        # for accumulated quantities, we subtract 1/2 hour to get the time at the center of the forecast bin
        data[3] -= 0.5
        return data

    def load_irradiance(self, **kwargs):
        data = self.load_insolation(**kwargs)
        data[0] /= 3600
        return data

    def load_wind_uv(self, **kwargs):
        """ Loads wind speed computed as sqrt(wind_u^2 + wind_v^2)"""
        # Check local database for data.
        # Fetch data from CDS API, if missing.
        with index(storagedir=storage_cfg(),
                   west=kwargs['west'],
                   east=kwargs['east'],
                   south=kwargs['south'],
                   north=kwargs['north'],
                   start=kwargs['start'],
                   end=kwargs['end']) as fetchmap:
            fetchmap(callback=fetch_era5, var='10m_u_component_of_wind')
            fetchmap(callback=fetch_era5, var='10m_v_component_of_wind')

        # form SQL query
        sql = ' AND '.join(['SELECT u_component_of_wind.val, u_component_of_wind.lat, u_component_of_wind.lon, u_component_of_wind.time, v_component_of_wind.val FROM u_component_of_wind '\
                'INNER JOIN v_component_of_wind '\
                'ON u_component_of_wind.lat == v_component_of_wind.lat',
                            'u_component_of_wind.lon == v_component_of_wind.lon',
                            'u_component_of_wind.time == v_component_of_wind.time '\
                                    'WHERE u_component_of_wind.lat >= ?',
                            'u_component_of_wind.lat <= ?',
                            'u_component_of_wind.lon >= ?',
                            'u_component_of_wind.lon <= ?',
                            'u_component_of_wind.time >= ?',
                            'u_component_of_wind.time <= ?']) + ' ORDER BY u_component_of_wind.time, u_component_of_wind.lat, u_component_of_wind.lon ASC'
        
        # establish connection to the geospatial.db database
        conn, db = database_cfg()
        
        # perform the query
        db.execute(
            sql,
            tuple(
                map(str, [
                    kwargs['south'], kwargs['north'], kwargs['west'],
                    kwargs['east'],
                    dt_2_epoch(kwargs['start']),
                    dt_2_epoch(kwargs['end'])
                ])))

        wind_u, lat, lon, epoch, wind_v = np.array(db.fetchall()).T

        # compute speed
        val = np.sqrt(np.square(wind_u) + np.square(wind_v))

        conn.close()

        return np.array((val, lat, lon, epoch)).astype(float)

    def __str__(self):
        info = '\n'.join([
            "Era5 Global Dataset from Copernicus Climate Datastore.",
            "Combines model data with observations from across",
            "the world into a globally complete and consistent dataset",
            "\thttps://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels"
        ])
        args = "(south, north, west, east, start, end)"
        return str_def(self, info, args)
