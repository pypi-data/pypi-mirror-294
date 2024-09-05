import os, sys
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import CRS
import pytest

from no3gwt.gis_attribute_utils import *

@pytest.fixture(scope="module")
def archive_data(test_data_path):
    archive_file = os.path.join(test_data_path, 'green_archive_wells.csv')
    archive_df = pd.read_csv(archive_file)
    archive_data = gpd.GeoDataFrame(archive_df, crs=CRS("epsg:4269"),
                                geometry=gpd.points_from_xy(archive_df.long,
                                archive_df.lat))
    archive_data = archive_data.to_crs(epsg=3070)
    return archive_data

@pytest.fixture(scope="module")
def test_points(archive_data):
    test_points = archive_data[['site_no', 'sample_dt', 'geometry']].copy()
    test_points['well_num'] = [i+1 for i in np.arange(0, test_points.shape[0])]
    return test_points

def test_mean_buffer_value(test_data_path, test_points, archive_data):
    input_raster = os.path.join(test_data_path, 'sden_b1km')
    test_points['stream_den'] = mean_buffer_value(input_raster, test_points)
    assert np.allclose(archive_data['stream_den'],
                       test_points['stream_den'],
                       1e-6)
    assert np.abs(np.mean(archive_data['stream_den'] - test_points['stream_den'])) < 1e-6
    

def test_raster_point_value(test_data_path, test_points, archive_data):
    input_raster = os.path.join(test_data_path, 'afe5k')
    test_points['A_Fe'] = raster_point_value(input_raster, test_points)
    assert np.allclose(archive_data['A_Fe'],
                       test_points['A_Fe'],
                       1e-6)
    assert np.abs(np.mean(archive_data['A_Fe']-test_points['A_Fe'])) < 1e-6

def test_landuse_catergory_value(test_data_path, test_points, archive_data):
    input_raster = os.path.join(test_data_path, 'lu82_b1k_test.tif')
    test_points['LU1982_crops'] = landuse_catergory_value(input_raster, 
                                                          test_points, 43)
    assert np.allclose(archive_data['LU1982_crops'],
                       test_points['LU1982_crops'],
                       0.1)
    assert np.abs(np.mean(archive_data['LU1982_crops']-test_points['LU1982_crops'])) < 0.3
    
def test_weighted_drainage_index(test_data_path, test_points, archive_data):
    input_raster = os.path.join(test_data_path, 'mur_90m2_b1km_clip.tif')
    drainageclass_file = os.path.join(test_data_path, 'WI_DrainageClass.csv')
    test_points['weighted_drainage_index'] = weighted_drainage_index(
                                                        input_raster, 
                                                        test_points, 
                                                        drainageclass_file)
    assert np.allclose(archive_data['weighted_drainage_index'],
                       test_points['weighted_drainage_index'],
                       0.1)
    assert np.abs(np.mean(archive_data['weighted_drainage_index']-test_points['weighted_drainage_index'])) < 0.05

def test_soller_geology_pct_buffer_area(test_data_path, test_points):
    '''
    May improve test in the future by incoroporating Smith (2021) archive data 
    to verify output. 
    '''
    geo_shp = os.path.join(test_data_path, 'Soller_stack_map_test.shp')
    geo_class = 'Coarse-grained stratified sediment'
    overlap_dict = soller_geology_pct_buffer_area(test_points, geo_shp, geo_class)
    test_points['pct_buffer_soller_coarse_gr_strat_sed'] = [overlap_dict.get(i, 0.) for i in test_points.index]
    assert test_points['pct_buffer_soller_coarse_gr_strat_sed'].notnull().any()


def test_redox_raster_stats(test_data_path):
    input_raster = os.path.join(test_data_path, 'wi_anox_do_and_fe.asc')
    mean, mdn, sd, mx, mn = redox_raster_stats(input_raster)
    assert mean == 3.080894708633423
    assert mdn == 1.
    assert sd == 3.5035674571990967
    assert mx == 10.
    assert mn == 0.


def test_bedrock_overlay(test_data_path, test_points):
    '''
    May improve test in the future by incoroporating Smith (2021) archive data 
    to verify output. 
    '''
    test_points['BedrockOverlay'] = bedrock_overlay(test_points, test_data_path,
                                                    test_points)
    assert test_points['BedrockOverlay'].notnull().any()
    expected = ['RestState', 'Coarse']
    assert test_points['BedrockOverlay'].unique().tolist() == expected
