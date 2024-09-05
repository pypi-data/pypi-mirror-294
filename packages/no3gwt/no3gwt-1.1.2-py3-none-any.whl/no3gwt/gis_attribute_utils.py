"""
This file contains numerous utility functions for processing and 
summarizing GIS files.  Many of these functions generate output for the
well of interest for use in the machine learning support models. 
"""

import csv
import numpy as np
import os
import pandas as pd
import shutil
import matplotlib.pyplot as plt

import geopandas as gpd
from pyproj import CRS
import rasterio

import no3gwt.ZonalAnalysis as za
from no3gwt.config import *

import pyproj
pyproj.network.set_network_enabled(False)

def mean_buffer_value(input_raster, gdf, buff_radius=500):
    """
    This function takes a list of points or wells in a pandas geodataframe, 
    creates circular buffer polygons around the points/wells with a specified 
    radius, then computes the mean raster value withing the buffer polygon. 
    
    NDST Method #1 - Mean raster value within 500-m buffer of well coordniates
    
    Parameters
    ------------------------------
    input_raster: str, 
                path to categorical landuse raster file for analysis 
    gdf: geopandas geodataframe, 
                geodataframe that contains of geometry of wells/points
    buff_radius = int, default 500,
                radius of circular buffer area around well. Units dependant
                on input_raster units.
    
    """
    #  make temporary directory to save files - will delete from directory 
    #  at the end of the function
    temp_dir = 'temp_files/'
    if os.path.exists(temp_dir):
        pass
    else:
        os.mkdir(temp_dir)
    
    with rasterio.open(input_raster) as src:
        raster_crs = src.crs
        wkt_out = raster_crs.to_wkt()
    
    gdf = gdf.to_crs(raster_crs)
    
    wkt_in = (gdf.crs).to_wkt()
    well_shapefile = os.path.join(temp_dir, 'user_gdf.shp')
    gdf.to_file(well_shapefile)  

    
    outpath = temp_dir + 'zonal_stats'
    za.zonal_stats(
        well_shapefile,
        input_raster,
        fldname='well_num',
        buffDist=buff_radius,
        projIn=wkt_in,  
        projOut=wkt_out, 
        fact=30,
        filenm=outpath,
        csvout=True
    )
    
    #  Remove nodata values (less than zero), and extract mean values
    zonal_df = pd.read_csv(outpath + '.csv')
    zonal_df.loc[zonal_df['mean'] < 0, 'mean'] = np.nan
    buff_mean = zonal_df['mean'].tolist()
    shutil.rmtree(temp_dir)
    
    return buff_mean

def raster_point_value(input_raster, gdf):
    """
    This function extracts the raster pixel value from the well/point 
    locations listed in a geodataframe.

    NDST Method #2 - Mean raster value within 500-m buffer of well 
    coordniates

    Properties
    ------------------------------
    input_raster: str,
                path to categorical landuse raster file for analysis
    gdf: geopandas geodataframe,
                geodataframe that contains of geometry of wells/points

    """

    with rasterio.open(input_raster) as src:
        raster_crs = src.crs
    gdf_reproj = gdf.to_crs(raster_crs)

    #  get a list of coordinate tuples for each row in a geopandas dataframe 
    #  that contains well point
    x_coords = gdf_reproj['geometry'].x.to_list()
    y_coords = gdf_reproj['geometry'].y.to_list()
    coords = list(zip(x_coords, y_coords))

    #  extract raster cell values at well/point coordinates
    with rasterio.open(input_raster) as src:
        point_values = list(np.concatenate([v for v in src.sample(coords)], axis=0))

    #  remove any nodata (negative) values
    point_values = [np.nan if i < 0 else i for i in point_values]
    
    return point_values

def landuse_catergory_value(input_raster, gdf, lu_class, 
                            buff_radius=500, verbose=True):
    """
    This function computes the percent categories of raster cells within 
    buffer zone

    NDST Method #3 - Percentage area of a specific raster class (or 
    classes) within 500-m buffer area

    Properties
    ------------------------------
    input_raster: str,
                path to categorical landuse raster file for analysis
    gdf: geopandas geodataframe,
                geodataframe that contains of geometry of wells/points
    lu_class: int or list of ints,
                landuse class(es) of interest. Must be passed to function as 
                an integer or list of integers that represent the landuse 
                class(es)
    buff_radius = int, default 500,
                radius of circular buffer area around well. Units dependant 
                on input_raster units.
    verbose : bool, default True
              if True, print all function progress messages.

    """

    temp_dir = 'temp_files/'
    if os.path.exists(temp_dir):
        pass
    else:
        os.mkdir(temp_dir)
    
    gdf = gdf.to_crs('epsg:5070')
    gdf.to_file(temp_dir + 'user_gdf.shp')
    well_shapefile = temp_dir + 'user_gdf.shp'
    outpath = temp_dir + 'zonal_catergory'
    
    za.zonal_category(
        gdb=well_shapefile,
        ras=input_raster,
        fldname='well_num',
        buffDist=buff_radius, 
        fact=30,
        filenm=outpath,
        csvout=True
    )
    
    zonal_df = pd.read_csv(outpath + '.csv')
    cols = zonal_df.columns.to_list()
    
    if verbose is True:
        print('lu_class: {}'.format(lu_class))

    if type(lu_class) == list and len(lu_class) > 1:
        str_vars = list(map(str, lu_class))
        both_list = list(set(str_vars).intersection(cols))
        both_df = zonal_df.loc[:, both_list]
        both_df['sum'] = both_df.sum(axis=1)
        lu_percent = both_df['sum'].to_list()
        
    if type(lu_class) == int or len(lu_class) == 1:
        str_var = str(lu_class)
        if str_var in zonal_df.columns:
            lu_percent = zonal_df[str_var].to_list()
        if str_var not in zonal_df.columns:
            lu_percent = np.zeros(zonal_df.shape[0]).tolist()

    shutil.rmtree(temp_dir)        
            
    return lu_percent

def weighted_drainage_index(input_raster, gdf, dc_dbf, buff_radius=500):
    """
    This function computes the weighted drainage index within a circular buffer 
    area around wells/points in a geopandas geodatabase given a SSURGO mukey 
    raster and DrainageClass.dbf

    NDST Method #4 - Weighted drainage index calculation

    Properties
    ------------------------------
    input_raster: str,
                path to SSURGO mukey grid raster file
    gdf: geopandas geodataframe,
                geodataframe that contains of geometry of wells/points
    dc_dbf: str,
                path to WI_DrainageClass.csv or DrainageClass.dbf with 
                corresponding input_raster mukey attributes
    buff_radius = int, default 500,
                radius of circular buffer area around well. Units 
                dependant on input_raster units.

    """

    temp_dir = 'temp_files/'
    if os.path.exists(temp_dir):
        pass
    else:
        os.mkdir(temp_dir)

    gdf = gdf.to_crs('epsg:5070')
    gdf.to_file(temp_dir + 'user_gdf.shp')
    well_shapefile = temp_dir + 'user_gdf.shp'
    outpath = temp_dir + 'weighted_drainage_index'

    za.zonal_category(
        gdb=well_shapefile,
        ras=input_raster,
        fldname='well_num',
        buffDist=buff_radius, 
        fact=30,
        filenm=outpath,
        csvout=True
    )

    if dc_dbf.endswith('.dbf'):
        drainage = gpd.read_file(dc_dbf)
        drainage['mukey'] = np.int64(drainage['mukey'])    
    else:
        drainage = pd.read_csv(dc_dbf)
        drainage['mukey'] = np.int64(drainage['mukey'])    

    zonal_df = pd.read_csv(outpath + '.csv')
    well_nums = zonal_df.well_num.to_list()    

    columns = ['DC1', 'DC2', 'DC4', 'DC5', 'DC6', 'DC8', 'DC9']
    weighted_drainage_index = []

    for wn in well_nums:
        well_df = zonal_df.loc[zonal_df.well_num == wn]
        well_df = well_df.loc[:, (well_df != 0).any(axis=0)]
        well_df.set_index('well_num', inplace=True)  
        mukeys = [np.int64(i) for i in well_df.columns.to_list()]

        well_df_T = well_df.transpose()
        well_df_T.reset_index(inplace=True)
        well_df_T.rename(columns={wn: "mukey_pct_area", 'index': 'mukey'}, inplace=True)
        well_df_T['mukey'] = np.int64(well_df_T['mukey'])
        well_df_T['mukey_pct_area']=well_df_T['mukey_pct_area'] / 100

        wdi_df = drainage.loc[drainage['mukey'].isin(mukeys)]
        wdi_df = wdi_df.reindex(columns=wdi_df.columns.tolist() + columns)
        wdi_df = wdi_df.merge(well_df_T, on='mukey')

        wdi_df.loc[:, 'DC1'] = wdi_df.DrnClass_1 * wdi_df.mukey_pct_area * 7 / 100 
        wdi_df.loc[:, 'DC2'] = wdi_df.DrnClass_2 * wdi_df.mukey_pct_area * 4 / 100
        wdi_df.loc[:, 'DC4'] = wdi_df.DrnClass_4 * wdi_df.mukey_pct_area * 2 / 100
        wdi_df.loc[:, 'DC5'] = wdi_df.DrnClass_5 * wdi_df.mukey_pct_area * 6 / 100
        wdi_df.loc[:, 'DC6'] = wdi_df.DrnClass_6 * wdi_df.mukey_pct_area * 3 / 100
        wdi_df.loc[:, 'DC8'] = wdi_df.DrnClass_8 * wdi_df.mukey_pct_area * 1 / 100
        wdi_df.loc[:, 'DC9'] = wdi_df.DrnClass_9 * wdi_df.mukey_pct_area * 5 / 100

        xa1 = wdi_df['DC1'].sum()
        xa2 = wdi_df['DC2'].sum()
        xa4 = wdi_df['DC4'].sum()
        xa5 = wdi_df['DC5'].sum()
        xa6 = wdi_df['DC6'].sum()
        xa8 = wdi_df['DC8'].sum()
        xa9 = wdi_df['DC9'].sum()

        wdi = xa1 + xa2 + xa4 + xa5 + xa6 + xa8 + xa9

        weighted_drainage_index.append(wdi)
        
    shutil.rmtree(temp_dir)

    return weighted_drainage_index

def shapefile_point_value(shapefile, gdf, attribute='Quaternary'):
    """
    This function computes the percent categories of raster cells within 
    buffer zone

    NDST Method #5 - Shapefile polygon value extraction to point

    Properties
    ------------------------------
    shapefile: str,
                path to ploygon shapefile with attribute of interest
    gdf: geopandas geodataframe,
                geodataframe that contains of geometry of wells/points
    attribute = str, default "Quaternary",
                title of polygon shapefile attribute to extract into a list

    """

    polygon_shapefile = gpd.read_file(shapefile)

    #  check that the new shapefile has a valid CRS
    try:
        CRS(polygon_shapefile.crs)
    #  if not, transform to a valid CRS. NAD83 works - epsg:5070.
    except:
        polygon_shapefile.crs = 'epsg:5070'
    #  create a well CRS object
    well_crs = CRS(gdf.crs)
    polygon_shapefile = polygon_shapefile.to_crs(well_crs)
    sjoin_gdf = gpd.sjoin(gdf, polygon_shapefile, how='left', 
                            predicate='within')
    polygon_attributes = list(sjoin_gdf[attribute])

    return polygon_attributes

def ssurgo_dbf_buffer_value(input_raster, gdf, db_file, 
                            column_name, buff_radius=500):
    """
   This function computes the mean raster value within a circular buffer area 
   around wells/points in a geopandas geodatabase given a SSURGO 90-m mukey 
   raster and Wiezorek 2014 .dbf file

   NDST Method #6 - SSURGO dbf file mean raster value within buffer area

   Properties
   ------------------------------
   input_raster: str,
               path to SSURGO mukey grid raster file
   gdf: geopandas geodataframe,
               geodataframe that contains of geometry of wells/points
   db_file: str,
               path to Wezorek databases (either WI-sized .csv files or 
               USA-sized .dbf files) with corresponding input_raster mukey 
               attributes
   column_name: str,
               name of the column of interest to for buffer mean value
   buff_radius = int, default 500,
               radius of circular buffer area around well. Units dependant on 
               input_raster units.

   """

    temp_dir = 'temp_files/'
    if os.path.exists(temp_dir):
        pass
    else:
        os.mkdir(temp_dir)

    gdf = gdf.to_crs('epsg:5070')
    gdf.to_file(temp_dir + 'user_gdf.shp')
    well_shapefile = temp_dir + 'user_gdf.shp'
    outpath = temp_dir + 'ssurgo_buffer'
    
    # Run zonal category to extract percent area of each mukey
    # inside each well buffer.
    za.zonal_category(
        gdb=well_shapefile,
        ras=input_raster,
        fldname='well_num',
        buffDist=buff_radius, 
        fact=30,
        filenm=outpath,
        csvout=True
    )

    # Read in zonal category results and dbf/csv file.
    zonal_df = pd.read_csv(outpath + '.csv', index_col='well_num')
    
    if db_file.endswith('.dbf'):
        dbf = gpd.read_file(db_file)
        dbf['mukey'] = np.int64(dbf['mukey'])    
    else:
        dbf = pd.read_csv(db_file)
        dbf['mukey'] = np.int64(dbf['mukey'])    

    well_nums = zonal_df.index.to_list()   
    ssurgo_mean = []

    # Loop through user wells and calculate the mean ssurgo value in buffer.
    # Loop is used for PEST calibration; single well for NDST application.
    for wn in well_nums:
        well_df = zonal_df.loc[[wn]]
        well_df = well_df.loc[:, (well_df != 0).any(axis=0)]
        mukeys = well_df.columns.to_list() 
        mukeys = [np.int64(i) for i in well_df.columns.to_list()]
        well_df_T = well_df.transpose()
        well_df_T.reset_index(inplace=True)
        well_df_T.rename(
            columns={wn: "mukey_pct_area", 'index': 'mukey'}, inplace=True
            )
        well_df_T['mukey'] = np.int64(well_df_T['mukey'])
        well_df_T['mukey_pct_area']=well_df_T['mukey_pct_area'] / 100

        dbf_mean = dbf.loc[dbf['mukey'].isin(mukeys)]
        dbf_mean = dbf_mean.reindex(columns=dbf_mean.columns.tolist() + \
                                                            ['ssurgo_mean'])
        dbf_mean.rename(columns={'{}'.format(column_name): 
                                        "column_of_interest"}, inplace=True)
        dbf_mean['column_of_interest'].replace(-9999., np.nan, inplace=True)
        dbf_mean = dbf_mean.merge(well_df_T, on='mukey')
        dbf_mean.loc[:, 'ssurgo_mean'] = dbf_mean.column_of_interest * \
                                                dbf_mean.mukey_pct_area
        value = dbf_mean['ssurgo_mean'].sum()
        ssurgo_mean.append(value)
    
    #  No HYDCLASS data in ALL of Adams County. If column_name is HYDCLASS 
    #  replace nodata (negative) values with state-wide average HYDCLASS 
    #  value = 18.72268281902348
    if column_name == 'HYDCLASS':
        ssurgo_mean = [18.72268281902348 if i < 0 else i for i in ssurgo_mean]
    
    #  Remove any other nodata (negative) values 
    ssurgo_mean = [np.nan if i < 0 else i for i in ssurgo_mean]
    shutil.rmtree(temp_dir)

    return ssurgo_mean

def soller_geology_pct_buffer_area(gdf, geo_shp, geo_class, 
                                   well_id=None, buff_radius=500):
    '''
    gdf : geopandas geodataframe, 
                geodataframe that contains of geometry of wells/points
    geo_shp : string, path to shapefile, 
                Soller_stack_map.shp, from Soller et al., 2012
    geo_class : string, geology class. Options are: 
                    'Till',
                    'Fine-grained stratified sediment',
                    'Coarse-grained stratified sediment',
                    'Exposed bedrock',
                    'Organic-rich sediment'
    well_id : string
                uniqe well identifier to create results dictionary, uses 
                index by defualt
    buff_radius = int, default 500,
                radius of circular buffer area around well. Units dependant
                on input_raster units.
            
    '''

    geo_gdf = gpd.read_file(geo_shp)
    buff_gdf = gdf.copy()
    buff_gdf = buff_gdf.to_crs(geo_gdf.crs)
    
    assert buff_gdf.crs.axis_info[0].unit_name == 'metre'
    buff_gdf['geometry'] = buff_gdf.geometry.buffer(buff_radius)
    
    #  slice out geo class of interest
    class_gdf = geo_gdf.loc[geo_gdf.GEOL_UNIT.str.startswith(geo_class)]
    dis_gdf = class_gdf.dissolve(by='SOURCE')
    #  drop wells/buffers that do not intersect the GEOL_UNIT.
    res_union = gpd.overlay(buff_gdf, dis_gdf, how='intersection')
    res_union['area'] = res_union.geometry.area
    #  calculate the percent overlap - the ratio of intersect area to total 
    # buffer area expressed as a %, round to nearest whole number
    res_union['pct_overlap'] = [np.round((i / (np.pi*(buff_radius**2)))*100, 
                                          decimals=0) for i in res_union.area]
    
    if well_id is None:
        overlap_dict = dict(zip(res_union.index, res_union.pct_overlap))
    else:
        overlap_dict = dict(zip(res_union[f'{well_id}'], 
                                                    res_union.pct_overlap))

    return overlap_dict

def redox_raster_stats(input_raster, plot=False):
    '''
    Simple utility to extract basic raster stats (mean, median, max, min, & 
    sd) to support Chris Green's redox modeling. 
    '''
    with rasterio.open(input_raster) as src:
        data = src.read(1)
        nodata = src.meta['nodata']
        dtype = src.meta['dtype']
       
    if np.issubdtype(dtype, np.integer) is True:
        data = data.astype(np.float32)
    data[data==nodata]=np.nan

    if not nodata==data[0,0]: 
        other_nodata=data[0,0]
    data[data==other_nodata]=np.nan
    
    mean = np.nanmean(data)
    mdn = np.nanmedian(data)
    sd = np.nanstd(data)
    mx = np.nanmax(data)
    mn = np.nanmin(data)
    
    if plot is True:  
        plt.imshow(data)
        plt.colorbar()
        plt.show()
    
    return mean, mdn, sd, mx, mn

def bedrock_overlay(gdf, shapepath, working_df, verbose=True):
    '''
    Function to recreate "BedrockOverlay" field for the depth-to-water
    support model input dataset. The function uses well locations for
    assessing whether the well is in one of three zones ("Cu", "BR_patchy",
    "Coarse") or the "rest of the state".

    '''
    shapefiles = [
        'BR_patchy_Area.shp',
        'CoarseGT200_Area.shp',
        'Cu_Area.shp'
    ]
    bo_list =[]
    
    #  Get list (for PEST; single well for users' application) of wells in 
    #  each of the three zones.
    for shp in shapefiles:
        temp_gdf = gdf.copy()
        if verbose is True:
            print(f'  processing shapefile: {shp}')
        shp = gpd.read_file(os.path.join(shapepath, shp))
        temp_gdf = temp_gdf.to_crs(shp.crs)
        clip = gpd.clip(temp_gdf, shp)
        if verbose is True:
            print(f'  number of wells in zone: {clip.shape[0]}')
        bo_list.append(clip.well_num.tolist())

    #  check to make sure there's no overlap between lists of wells
    assert(set(bo_list[0]).intersection(bo_list[1])==set())
    assert(set(bo_list[0]).intersection(bo_list[2])==set())
    assert(set(bo_list[1]).intersection(bo_list[2])==set())

    working_df['BedrockOverlay'] = 'RestState'
    bo_values = ['BR_patchy', 'Coarse', 'Cu']

    #  This step makes a new column and returns it as a list (which 
    #  can then be added, outside of this function, as a new column)
    for val, wells in zip(bo_values, bo_list):
        working_df.loc[working_df.well_num.isin(wells), 'BedrockOverlay'] = val
    
    return working_df.BedrockOverlay.tolist()

def calc_O2_rate(user_df_all, well, O2_coeffs):
    '''
    This function computes the oxygen reduction rate for a well based on the
    multivariate regession equation developed by Juckem and Green (2023), and
    published as a data release as part of the WI-NDST project.    
    '''

    variables = ['mean_twi', 
    'stream_den', 
    'mean_subsurf_contime' , 
    'Rech_eff_myr_Reitz_mean' , 
    'Rech_mmyr_SWBNawqa_mean' , 
    'pet_inyr' , 
    'LP1' , 
    'LP2' , 
    'rech48grd_wolock' , 
    'alt_ft_NAVD88' , 
    'DSD4' , 
    'DSD3' , 
    'LP8' , 
    'A_Fe' , 
    'C_C_Inorg' , 
    'LU1982_pasture' , 
    'LU1982_lowuse' , 
    'LU1982_developed' , 
    'weighted_drainage_index' , 
    'SSURGO_HYDCLASS_mean', 
    'SSURGO_AVG_NO10_mean' , 
    'SSURGO_hydgrp_B_mean' , 
    'SSURGO_wtdep_min_mean' , 
    'SSURGO_avg_silt_mean' , 
    'SSURGO_avg_bd_mean',
    'z_W',
    'uz_thick',
    'pct_buffer_soller_coarse_gr_strat_sed', 
    'C_C_Org',                                
    'LU1982_wetlands' ,                      
    'wi_anox_do_and_fe']

    df = user_df_all[variables]
    df_well = df.loc[well]
    df_well = df_well.fillna(0)
    coeff_dict = dict(zip(O2_coeffs.Variable.values, O2_coeffs.coefficient.values))
    coeffs_df = O2_coeffs.copy().set_index('Variable')

    O2_rate = O2_rate_intercept # from config file
    min_rate = O2_min_rate # from config file
    max_rate = O2_max_rate # from config file
    for i in variables:
        GIS_val = df_well[i]
        val_norm  = (GIS_val - coeffs_df.loc[i]['avg'])/coeffs_df.loc[i]['std']
        sum_to_add = val_norm*coeff_dict[i]
        O2_rate = O2_rate + sum_to_add
    if O2_rate < min_rate:
        O2_rate = min_rate
    if O2_rate > max_rate:
        O2_rate = max_rate

    return O2_rate