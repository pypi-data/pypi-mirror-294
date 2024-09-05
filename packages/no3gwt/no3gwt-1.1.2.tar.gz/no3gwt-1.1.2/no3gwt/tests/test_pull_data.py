import os, sys
import pandas as pd
import numpy as np
import geopandas as gpd
from pyproj import CRS
import pytest
from datetime import datetime

import no3gwt.well_setup as ws

@pytest.fixture(scope="function")
def user_input_file(project_root_path):
    return(os.path.join(project_root_path, 
                        'data_in', 
                        'example2.xlsx')
                        )

# @pytest.fixture(scope="function")
# def processed_file(project_root_path):
#     return(os.path.join(project_root_path, 
#                         'data_in', 
#                         'example_input.csv')
#                         )

@pytest.fixture(scope="function")
def septic_file(project_root_path):
    return os.path.join(project_root_path, 'data_mid', 'septic_all7.nc') 


@pytest.fixture(scope="module")
def well_data(user_data):
    well_data = gpd.GeoDataFrame(user_data,
                       crs=CRS("epsg:4269"), 
                       geometry=gpd.points_from_xy(user_data.longitude_deg,
                                                   user_data.latitude_deg)
                       )
    return well_data

# nitrate netcdf
@pytest.fixture(scope="function")
def no3_file(project_root_path):
    return os.path.join(project_root_path, 'data_mid', 'ibis_21_int_clipped.nc')

# flux netcdf
@pytest.fixture(scope="function")
def flux_file(project_root_path):
    return os.path.join(project_root_path, 'data_mid', 'flux_21_int_clipped.nc')
#

def test_pull_user_input(user_input_file):
    ws_class = ws.WellInfo(user_input_file)
    user_data = ws_class.pull_user_input()
    assert user_data.shape == (9,28)
    no3_list = user_data['NO3_obs'].tolist()
    assert len(no3_list) == 9
    assert np.nanmean(no3_list) == 15.625

def test_pull_septic_new(well_data, septic_file, tmpdir):
    ws_class = ws.WellInfo(user_input_file)
    out_file = os.path.join(tmpdir, 'Septic_leach_data.csv')
    ws_class.sep_out_file = out_file
    ws_class.pull_septic_new(well_data, septic_file)
    septic_data = pd.read_csv(out_file)
    this_year = datetime.today().year
    assert septic_data.Year.max() == this_year
    assert septic_data.shape[0] == len(np.arange(1850, this_year+1))
    assert septic_data.Sep_leach_1.notnull().any()

def test_pull_IBIS(user_data, no3_file, flux_file, tmpdir):

    ws_class = ws.WellInfo(user_input_file)
    out_file = os.path.join(tmpdir, 'NO3_leach_data.csv')
    ws_class.N_out_file = out_file
    ws_class.pull_IBIS(user_data, no3_file=no3_file, 
              flux_file=flux_file)
    ibis_data = pd.read_csv(out_file)
    assert ibis_data.shape[0] == 116
    assert ibis_data.NO3_Leaching_1.notnull().any()
    assert ibis_data.Drainage_Flux_1.notnull().any()

