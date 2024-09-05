"""
This utility file supports the WI-NDST code base.  Included functions are
used to read-in the user file, processes and format the data, and prepare
dataframes of the user's well data for use by subsequent scenario functions.
Other functions assist with pulling in data from various support models or
running the support models. Additional functions assist with processing and
manipulating calibration parameters and associated Monte Carlo realizations.  
"""

import csv
import os, sys
import time
from datetime import datetime
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import CRS
import pyproj
import no3gwt.gis_attribute_utils as gisutils
import gzip
import rasterio
import xarray as xr
from scipy.interpolate import interp1d
from no3gwt.config import *
from joblib import dump, load
import warnings
from shapely.geometry import Point, shape, MultiPolygon
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
pyproj.network.set_network_enabled(False)

debug = False
def check_location(user_df):
    # epsg:4326 is latitude/longitude_deg:          User input data
    # epsg:3071 is Wisc Transverse Mercator, HARN:  WI_outline  
    # epsg:26916 is UTM zone 16N, NAD83:            WORKING CRS

    well_df = gpd.GeoDataFrame(user_df,
                               crs = "EPSG:4326",
                               geometry=gpd.points_from_xy(user_df.longitude_deg,
                                                           user_df.latitude_deg))
    well_df.to_crs(epsg=26916, inplace=True)  # transform to UTM83Z16N
    
    # reads *.prj file so wi_shp is already in epsg=3071 CRS
    wi_shp = gpd.read_file(os.path.join(gisdir, 'ibis_outline.shp'))
    wi_shp.to_crs(epsg=26916, inplace=True)  # transform to UTM83Z16N
    
    crystaline_shp = gpd.read_file(os.path.join(gisdir, 'BR_patchy_crystaline.shp'))
    crystaline_shp.to_crs(epsg=26916, inplace=True)  # transform to UTM83Z16N
   
    cu_shp = gpd.read_file(os.path.join(gisdir,'Cu.shp'))
    cu_shp.to_crs(epsg=26916, inplace=True)  # transform to UTM83Z16N
    
    carbonate_shp = gpd.read_file(os.path.join(gisdir, 'Wis_CarbDepAr_Wgnhs_2009_1m.shp'))
    carbonate_shp.to_crs(epsg=26916, inplace=True)  # transform to UTM83Z16N

    shp_dict = {'exposed_bedrock' : cu_shp, 'crystaline_bedrock' : crystaline_shp, 
                'carbonate_bedrock' : carbonate_shp}

    bedrock_excluded = False
    
    shp_list = list(wi_shp.geometry)
    wi_geom = MultiPolygon(shp_list)

    if well_df.within(wi_geom)[0]:
        print('This well is within the area of Wisconin for which the GW-NDST \n'\
              'tool has nitrate loading information.')
    else:
        print('This well is outside the area of Wisconin for which the GW-NDST \n'\
              'tool has nitrate loading information.')
        sys.exit('Stopping tool.')
    
    for name, shp in shp_dict.items():
        
        if shp.contains(well_df.geometry[0])[0]:
            
            print1 = f'\n---------------------------------------------------'\
                     '--------------------\n'\
                     'NOTICE: This well is within an area where groundwater is '\
                     'likely to \nflow through fractured bedrock. While the '\
                     'GW-NDST will still function, \nit is important to note '\
                     'that the tool was not designed to simulate \n'\
                     'preferential flow conditions, such as flow through '\
                     'fractures, \nkarst, etc.  Results of the GW-NDST for '\
                     'this location may be unreliable.' 
            print(print1)
            model_shp = shp
            bedrock_excluded = True
            ax = shp.plot(label = 'Geologic Boundary', facecolor='grey', 
                          alpha = 0.25, edgecolor='grey', legend = True, 
                          figsize = (5,5))
            well_df.plot(ax=ax, label = 'Well Location', marker = '.',
                         color = 'red', legend = True)
            wi_shp.plot(ax=ax, facecolor = 'None', edgecolor = 'black', 
                        label = 'Wisconsin', legend = True)
            ax.get_legend_handles_labels()
            ax.set_title('Fractured Bedrock Areas of Wisconsin')
            ax.legend()
            ax.set_xlim((1000, 540000))
            ax.set_ylim((4680000, 5250000))
            plt.show()
            print2 = '----------------------------------------------------'\
                     '--------------------\n'
            print(print2)
    
def get_well_params(well, user_df):
    
    params_update = dict()
    params_update.update({'disp_ratio': (user_df.loc[well, 'disp_ratio']),
                         'uz_mobile' : (user_df.loc[well, 'uz_mobile'] ),
                         'k_no3' : (user_df.loc[well, 'k_o2'] * 
                                    user_df.loc[well,'k_o2_to_k_no3_mult']),
                         'k_o2_mult' : (user_df.loc[well, 'k_o2_mult']),
                         'age_mult' : (user_df.loc[well, 'age_mult']),
                         'is_end_mult' : (user_df.loc[well, 'is_end_mult']),
                         'is_start_mult' : (user_df.loc[well, 
                                                        'is_start_mult']),
                         'uz_thick' : (user_df.loc[well, 'uz_thick']),
                         'k_o2' : (user_df.loc[well, 'k_o2']),
                         'ibis_mult' : (user_df.loc[well, 'ibis_mult']),
                         'flux_mult' : (user_df.loc[well, 'flux_mult'])
                         })
    return params_update

def user_update_params(params, user_params_mults = 'default'):
    ''' This function takes the well, user_df, starting params, and 
    user defined parameter multipliers (user_params_mults), and updates 
    them into a new dictionary of parameters. If no user defined para-
    meter multipliers are provided, they are simply multiplied by 1 
    (unchanged).
    '''
    params_update = params.copy()
    if user_params_mults == 'default':
        user_params_mults =  {'mean_age_mult' : 1,
                      'age_dispersivity_mult': 1,
                      'uz_mobile_watercontent_mult' : 1,
                      'IBIS_mult' : 1,
                      'IBIS_start_mult' : 1,
                      'IBIS_end_mult' : 1,
                      'recharge_mult' : 1,
                      'septic_mult' : 1,
                      'k_O2_mult' : 1,
                      'O2_cut_mult' : 1,
                      'k_NO3_mult' : 1}

    params_update = {'disp_ratio': params['disp_ratio'] * 
                                   user_params_mults['age_dispersivity_mult'],
                     'uz_mobile' : params['uz_mobile'] * 
                                   user_params_mults['uz_mobile_watercontent_mult'],
                     'k_no3' : params['k_no3'] * 
                               user_params_mults['k_NO3_mult'],
                     'k_o2_mult' : params['k_o2_mult'],
                     'age_mult' : params['age_mult'] * 
                                  user_params_mults['mean_age_mult'],
                     'is_end_mult' : params['is_end_mult'] * 
                                     user_params_mults['IBIS_end_mult'],
                     'is_start_mult' : params['is_start_mult'] * 
                                       user_params_mults['IBIS_start_mult'],
                     'uz_thick' : params['uz_thick'],
                     'k_o2' : params['k_o2'] * user_params_mults['k_O2_mult'],
                     'ibis_mult' : params['ibis_mult'] * 
                                   user_params_mults['IBIS_mult'],
                     'flux_mult' : params['flux_mult'] * 
                                   user_params_mults['recharge_mult'],
                     'septic_mult' : params['septic_mult'] * 
                                     user_params_mults['septic_mult'],
                     'o2_cut' : params['o2_cut'] * 
                                user_params_mults['O2_cut_mult'],
                     'k_o2_to_k_no3_mult' : params['k_o2_to_k_no3_mult']
                     }
                     
    return params_update

class WellInfo:
  
    def __init__(self, user_file):
        self.user_file = user_file
        self.outfile_path = outfile_path
        self.sep_out_file = sep_out_file
        self.N_out_file = N_out_file
        
        if os.path.exists(output_path):
            pass
        else:
            os.mkdir(output_path)
  
    def pull_user_input(self):
        ''' This function reads in a user-specified XLSX file and processes 
        the data into a dataframe, and then passes the dataframe back 
        to the function that called it.
        '''
        
        df1 = pd.read_excel(self.user_file, index_col = None, header = 0)
        df1 = df1.head(7).T.head(3)
        df1 = df1.reset_index(drop = True)
        df1.columns = df1.loc[0]
        df1 = df1[2:]
        df1 = df1.rename(columns = {'Depth to bottom of screen' : 
                                    'scrndepbot_ft',
                                   'Depth to top of screen (depth of casing)' 
                                    : 'scrndeptop_ft',
                                   'Depth to top of screen' : 'scrndeptop_ft',
                                   'Latitude' : 'latitude_deg',
                                   'Longitude' : 'longitude_deg',
                                   'Altitude' : 'altitude',
                                   'Longterm avg. pumping rate (if available)' 
                                    : 'pump_Q'})
        df1 = df1.reset_index(drop = True)

        df2 = pd.read_excel(self.user_file, skiprows = 11)
        # All other columns retain pcode titles
        df2 = df2.rename(columns={'YYYY-MM-DD':'sample_dt', 
                                'p00618, 00620, 00631, or 00630':'NO3_obs',
                                'p00300':'O2_obs', 
                                'p00434':'pH',
                                'p01046': 'Fe_obs',
                                'p72019':'lev_va_merge_nwis_ft'})  
        if len(df2) == 0:  # Generate an empty DataFrame if no data in input
            nannp = np.empty(len(df2.columns))
            nannp[:] = np.nan
            colnames = list(df2.columns)
            nanrow = pd.Series(nannp, index=colnames)
            df2 = pd.concat([df2, nanrow.to_frame().T], ignore_index=True)
        # Trim away any additional columns that the user might add
        df2 = df2.iloc[:,0:20]  
                                
        pcodes = df2.columns.tolist()[4:-2]
        pcodes_new = [(i + '_imp') for i in pcodes]
        df2 = df2.rename(columns=dict(zip(pcodes, pcodes_new)))
        df2 = df2.reset_index(drop = True)
        
        # Here we add in a for loop to check for string entries.
        # Right now, the only method we have considers < and > string 
        # entries. The less than symbols (<) are taken as half the 
        # value. The greater than symbols (>) are taken as the value.
        cols = []
        for col in df2.columns[1:]:
            row_w_string = df2.loc[df2['{}'.format(col)].map(type) == 
                                   str].index.to_list()
            if len(row_w_string) > 0:
                cols.append(col)
        
        for i in range(0, len(cols)):
            tmp = []
            for j in df2[cols[i]].values:
                if type(j) == str:
                    if '<' in j:
                        val = j.split('<')[-1]
                        new_val = float(val)/2    
                    elif '>' in j:
                        val = j.split('>')[-1]
                        new_val = float(val)
                else:
                    new_val = j
                tmp.append(new_val)
            df2[cols[i]] = tmp
        user_df = df2.copy()
        for col in df1.columns:
            # Add header info to each column
            user_df[col] = df1[col].loc[0]  
        
        user_df['well_num'] = np.int16(1)

        return user_df
    
    def run_age_ml_py(self, input_data,
                      model_path, verbose=True):
                      
        X_test = pd.read_csv(input_data,sep='\t')
        age_ml_model = load(model_path)
        test_pred = age_ml_model.predict(X_test)
        X_test['preds'] = test_pred
        X_test['total_tt_years'] = np.exp(test_pred) * 1.153379
        X_test.to_csv(input_data.replace('.txt', '_age.txt'),sep='\t')
        if verbose is True:
            print('Results of ageML model printed to {}.'.format(
                    input_data.replace('.txt', '_age.txt')))
    
    def run_DTW_ML_py(self, input_data,
                      model_path, verbose=True):

        X_test = pd.read_csv(input_data, sep='\t')
        dtw_ml_model = load(model_path)
        test_pred = dtw_ml_model.predict(X_test)
        X_test['pred_DTW'] = test_pred
        X_test.to_csv(input_data.replace('_input.csv', '_dtw_preds.csv'), sep=',')
        if verbose is True:
            print('Results of ageML model printed to {}.'.format(
                   input_data.replace('_input.csv', '_dtw_preds.csv')))
   
    def find_grid_pars(self, gdf, user_df, params, pestdir = pestdir, 
                       gisdir = gisdir):

        #  1. List parameters to use in grid form    
        add_pars = ['disp_ratio', 'uz_mobile', 'age_mult', 'k_o2_mult',
                    'ibis_mult', 'is_start_mult', 'is_end_mult', 'flux_mult',
                    'septic_mult', 'o2_cut', 'k_o2_to_k_no3_mult'
                   ] 
                    
        #  2. Read in and georefrence grided parameter data
        with rasterio.open(os.path.join(gisdir,
                           'NationalGrid/natlGrid_WIbuff_block.tif')) as src:
            grid_crs = src.crs

        #  3a. Extract parameter values from geotiffs using 
        #      raster_point_value tool and add to user_df
        for par in add_pars:
            input_raster= os.path.join(pestdir, f'{par}.tif')
            gdf_reproj = gdf.to_crs(grid_crs)
            par_vals = gisutils.raster_point_value(input_raster, gdf_reproj)
            user_df[f'{par}'] = par_vals

        # 4. Update k_02 using k_o2_mult grid par
        user_df['k_o2'] = user_df['k_o2'] * user_df['k_o2_mult']

        # 5. Calc k_no3 from k_o2 in user data
        user_df['k_no3'] = user_df['k_o2_to_k_no3_mult'] * user_df['k_o2']

        # 6. Add user_df parameters to add_pars 
        user_df_pars = ['uz_thick', 'k_o2', 'k_no3']

        for user_df_par in user_df_pars:
            add_pars.append(user_df_par)

        return user_df
           
    def pull_septic_new(self, user_df, 
                        septic_file = septic_file):

        t = time.time()   
        septic_import = xr.open_dataarray(septic_file).load()

        # Rename latitude and longitude columns to have same name as 
        # IBIS output, makes searching easier later
        user_df = user_df.rename(columns = {'latitude_deg' : 'lat', 
                                            'longitude_deg' : 'lon'}
                                            )
        # Pull out the lat/long coordinates
        well_locs = user_df[['lat', 'lon']] 

        myList = user_df.lat.values.tolist()
        if all(x==myList[0] for x in myList):
            if user_df.sample_dt.isnull().values.all():
                well = user_df.head(1).index[0]
            else:
                well = user_df[user_df['sample_dt'] 
                               == user_df.sample_dt.max()].index[0]
            well_locs = well_locs.head(1)
            well_locs = well_locs.reset_index()
            well_locs.loc[0, 'well_num'] = well
            well_locs = well_locs.astype({'well_num': 'int32'})
            well_locs = well_locs.set_index('well_num')
            well_locs = well_locs[['lat', 'lon']]
        # Initialize list of dictionaries    
        well_dicts = [] 
        for idx in well_locs.index:
            well_dicts.append(well_locs.loc[idx].to_dict())

        # Find timeseries of that variable for a specific lat/long pair
        nanwell_list = []
        septic_dict = {}
        for well, locs in zip(well_locs.index, well_dicts):
            # Calc NO3 leaching for each well
            septic = septic_import.sel(locs, method = 'nearest') 
            septic_vals = np.array(septic)
            septic_times = np.arange(1850, 2020, 10)

            # These arrays are the same for each well, 
            # so only need one key.
            septic_dict['Time'] = septic_times 
            septic_dict[f'Septic_{well}'] = septic_vals

            if np.any(np.isnan(septic_vals)):
                nanwell_list.append(well)

        if len(nanwell_list) > 0:
            nan_well_out_path = os.path.dirname(self.sep_out_file)
            with open(os.path.join(nan_well_out_path, 
                                   'Septic_nanwell_list.txt'), 'w') as ofp:
                for item in nanwell_list:
                    ofp.write('{}\n'.format(item))
            print('Wrote list of NA wells to {}/Septic_nanwell_list.txt\
                  '.format(nan_well_out_path))

        df = pd.DataFrame.from_dict(septic_dict)
        this_year = datetime.today().year
        decades = ((this_year - 1850)//10)
        y = np.linspace(1850, (this_year//10)*10, ((this_year - 1850)//10)+1, 
                        endpoint=True, dtype = int) 

        y1 = y[0:decades]
        col_names = []
        for i in y1:
            col_names.append('sep_{}'.format(i))

        sep_df = df.copy()
        sep_df2 = sep_df.set_index([col_names])
        sep_df2 = sep_df2.drop(columns = 'Time')
        sep_df = sep_df2.T
        sep_df_idx = sep_df[col_names].fillna(0)

        start, end = y[0], this_year
        years_interp = np.linspace(start, end, num = end - start + 1, 
                                   endpoint=True, dtype = int)

        # Initialize results dictionary to build into single df after loop
        septic_dict = {'Year': years_interp} 

        for i in sep_df_idx.index:
            yr = i.split('_')[-1]
            slope_90 = (sep_df_idx.loc[i, 'sep_2000'] - 
                        sep_df_idx.loc[i, 'sep_1990'])/10
            slope_00 = (sep_df_idx.loc[i, 'sep_2010'] - 
                        sep_df_idx.loc[i, 'sep_2000'])/10
            slope_avg = np.mean([slope_90, slope_00])
            val_2020 = sep_df_idx.loc[i, 'sep_2010'] + 10*slope_avg
            sep_df_idx.loc[i, 'sep_2020'] = val_2020
            well_vals = sep_df_idx.loc[i].tolist()
            y_interp = interp1d(y, well_vals, bounds_error = False, 
                                fill_value = 'extrapolate')
            septic_interp = y_interp(years_interp)
            septic_dict[f'Sep_leach_{str(yr)}'] = septic_interp

        pd.DataFrame.from_dict(septic_dict).to_csv(self.sep_out_file, 
                                                   index=False)
        if debug:
            print('pull_septic completed in {0:.2f} seconds\
              '.format(time.time() - t))
        
        self.sep_input_df = pd.read_csv(self.sep_out_file)
        
    def pull_IBIS(self, user_df, 
                  no3_file = ag_input_path, 
                  flux_file = flux_file):
        '''
        user_df:    a geodataframe of well information supplied by the 
                    user, generated in `make_user_df_w_params`
        no3_file:   path to netCDF file of NO3 leaching (kg/ha) 
                    supplied by IBIS. This function assumes that nan 
                    values have been filled with interpolated values 
                    (via the `interpolate_IBIS` function)
        flux_file:  path to netCDF file of recharge (mm) supplied by 
                    IBIS. This function assumes that nan values have 
                    been filled with interpolated values (via the 
                    `interpolate_IBIS` function)
        out_file:   path to output/file - where csv files generated by 
                    this function will be saved
                   
        returns nothing, but writes-out NO3 leaching and flux values to 
        csv file in the specified out_path location for wells in 
        user_df.
        '''
        
        t = time.time()
        if no3_file.endswith('erfc.nc'):  
            # Special filter has been applied to this historical input.
            # Not currently used with GW-NDST.
            ds_no3 = xr.open_dataarray(no3_file).load() 
            ds_flux = xr.open_dataarray(flux_file).load()
            # Pass variable for conformity with Else statement
            no3leach = ds_no3 
            flux = ds_flux
        else:
            ds_no3 = xr.open_dataset(no3_file).load() 
            ds_flux = xr.open_dataset(flux_file).load()
            no3leach = ds_no3['urbno3leach']
            flux = ds_flux['drainage']
        
        # Rename latitude and longitude columns to have same name as 
        # IBIS output, makes searching easier later.
        user_df = user_df.rename(columns = {'latitude_deg' : 'latitude', 
                                            'longitude_deg' : 'longitude'}
                                            )
        # Pull out the lat/long coordinates
        well_locs = user_df[['latitude', 'longitude']] 
        
        myList = user_df.latitude.values.tolist()
        if all(x==myList[0] for x in myList):
            if user_df.sample_dt.isnull().values.all():
                well = user_df.head(1).index[0]
            else:
                well = user_df[user_df['sample_dt'] == 
                               user_df.sample_dt.max()].index[0]
            well_locs = well_locs.head(1)
            well_locs = well_locs.reset_index()
            well_locs.loc[0, 'well_num'] = well
            well_locs = well_locs.astype({'well_num': 'int32'})
            well_locs = well_locs.set_index('well_num')
            well_locs = well_locs[['latitude', 'longitude']]
        # Initialize list of dictionaries
        well_dicts = [] 
        for idx in well_locs.index:
            well_dicts.append(well_locs.loc[idx].to_dict())

        # Find timeseries of that variable for a specific lat/long pair
        nanwell_list = []
        ibis_dict = {}
        for well, locs in zip(well_locs.index, well_dicts):
            # Calc NO3 leaching for each well
            leaching = no3leach.sel(locs, method = 'nearest') 
            leach_vals = np.array(leaching)
            leach_times = np.array(leaching.time)
            
            # Calc flux drainage for each well
            drainage = flux.sel(locs, method = 'nearest')
            drain_flux = np.array(drainage)
            
            # These arrays are the same for each well so only need one key
            ibis_dict['Time'] = leach_times 
            ibis_dict[f'NO3_Leaching_{well}'] = leach_vals
            ibis_dict[f'Drainage_Flux_{well}'] = drain_flux
            
            if np.any(np.isnan(leach_vals)):
                print('NA vals in IBIS data at well_num: {0}; '
                      'location: {1}'.format(well, locs))
                nanwell_list.append(well)
                
        if len(nanwell_list) > 0:
            out_path = os.path.dirname(output_path)
            with open(os.path.join(out_path, 
                                   'IBIS_nanwell_list.txt'), 'w') as ofp:
                for item in nanwell_list:
                    ofp.write('{}\n'.format(item))
            print('Wrote list of NA wells to {}/IBIS_nanwell_list.txt\
                  '.format(out_path))
            
        pd.DataFrame.from_dict(ibis_dict).to_csv(self.N_out_file, index=False)
        if debug:
            print('pull_IBIS completed in {0:.2f} seconds\
              '.format(time.time() - t))
        else:
            print('-- Extracted septic and ag. leaching results --')
            print("\nFinished processing the well and running support models.")
            
        self.N_input_df = pd.read_csv(self.N_out_file)
        
        return self

    def process_chem_data(self, user_df, usermode):
    ## Process chemistry data into annual averages, log-transform
        
        chemlist = ['NO3_obs', 'O2_obs', 'Fe_obs', 'p00095_imp', 'p00405_imp',
                    'p00671_imp', 'p00915_imp', 'p00925_imp', 'p00930_imp', 
                    'p00935_imp', 'p00940_imp', 'p00945_imp', 'p00950_imp', 
                    'p00955_imp', 'p01056_imp', 'p00608_imp']
        
        if usermode is True:
            # Initialize; skip DTW_ML if user supplies DTW data.
            self.run_DTW_ML_flag = False  
            
            # re-sample all measurements into a single average value of the annual 
            # means for use with ageML and dtwML so get back one representative value.
            # keep track of well id
            well_id = user_df['Well ID or well name'].unique()[0]
            # fix groupby problem
            user_df2 = user_df.drop('Well ID or well name',axis=1)
            # Check to see that there is actually data in the DF and if not,
            # write a warning, don't average by year, and continue.
            if user_df2.sample_dt.notnull().any():
                # Re-sample all measurements into a single average value of
                # the annual means for use with ageML and dtwML so get back 
                # one representative value.
                user_df2['year']=user_df.sample_dt.dt.year
                annualave = user_df2.groupby(by='year').transform('mean')
                historicalave = annualave.mean()

                   # sample_dt is needed for
                   # backward compatability, but isn't used by ML models.
            else:  # In case there is no date-time entry.
                historicalave = user_df2.mean()
                
            historicalave = pd.DataFrame(historicalave).T
            historicalave['sample_dt'] = datetime.today()  
                                              
            # Check to see what type of sample data is available for 
            # this well.  Inform the user if age estimates for this well 
            # could be better informed by analyzing additional analytes.
            inorganics = [historicalave.O2_obs, historicalave.pH, 
                          historicalave.p00010_imp, historicalave.p00950_imp, 
                          historicalave.p00940_imp, historicalave.p00945_imp, 
                          historicalave.p00955_imp, historicalave.p00671_imp, 
                          historicalave.p00095_imp, historicalave.p00925_imp, 
                          historicalave.p00405_imp, historicalave.p00930_imp,
                          historicalave.p00608_imp, historicalave.p01056_imp, 
                          historicalave.p00915_imp, historicalave.p00935_imp, 
                          historicalave.Fe_obs]

            print('\n')
            if np.all(pd.isna(inorganics)):
                print('------------------------------------------------------'
                '----------------\n'
                'NOTICE: The input for this well lacks supplemental '
                'chemistry data. \n'
                'Future age distribution estimates could potentially be '
                'improved for \n'
                'this well by collecting supplemental chemistry samples '
                '(columns C \nthrough S in the Excel input file).'
                '\n----------------------------------------------------------'
                '------------\n')
            if np.any(historicalave.scrndepbot_ft > 500):
                print('------------------------------------------------------'
                '----------------\n'
                'Warning: This well is more than 500 feet (152 m) deep, '
                'which is beyond \n'
                'the depth of wells used to train and validate the age '
                'model. Age \nestimates for this well may be unreliable.'
                '\n----------------------------------------------------------'
                '------------\n')
            if np.any(pd.isna([historicalave.scrndepbot_ft, 
                      historicalave.scrndeptop_ft])):
                print('------------------------------------------------------'
                '----------------\n'
                'Warning: This well is missing well depth information (depth '
                'to bottom or \n'
                'top of screen). This is a critical input variable for '
                'estimating age. \n'
                'An age distribution will be computed, but age estimates for '
                'this well \nmay be unreliable.'
                '\n----------------------------------------------------------'
                '------------\n')
            if np.all(historicalave.lev_va_merge_nwis_ft.isna()):
                self.run_DTW_ML_flag = True
                print('------------------------------------------------------'
                '----------------\n'
                'NOTICE: No "depth to water" information (column S in the '
                'Excel input \n'
                'file) was provided for this well.  Future age distribution '
                'estimates \n'
                'could potentially be improved for this well by measuring '
                'the depth \nto water below the land surface.'
                '\n----------------------------------------------------------'
                '------------\n')
            else:  
               # Test for DTW > 200, but only if there's at least 1 
               # user input value, else a warning gets printed to the 
               # GUI (above).
                if np.nanmax(historicalave.lev_va_merge_nwis_ft) >= 200:
                    print('--------------------------------------------------'
                    '--------------------\n'
                    'NOTICE: The provided "depth to water" is greater than '
                    '200 feet, which is \n'
                    'suspicious.  An updated estimate has been provided '
                    'instead, which will be \n'
                    'used in the age Machine Learning model to estimate the '
                    'age of water in the \nwell.'
                    '\n------------------------------------------------------'
                    '----------------\n')
                    self.run_DTW_ML_flag = True

            # Convert chemistry to natural-log
            for chem in chemlist:
                # Handle reported chem values == 0 by making them 
                # really small for log transform
                historicalave[f'{chem}'] = [np.log(1e-6) if i == 0. 
                                            else np.log(i) 
                                            for i in historicalave[f'{chem}']]
                
            # Make sure sample_dt is string; shapefile export requrement
            historicalave['sample_dt'] = historicalave['sample_dt'].dt.\
                                         strftime('%Y-%m-%d')
            gdf = gpd.GeoDataFrame(historicalave,
                      crs=CRS("epsg:4269"), 
                      geometry=gpd.points_from_xy(historicalave.longitude_deg,
                                                  historicalave.latitude_deg)
                      )
                        
            self.gdf = gdf.to_crs(epsg=26916)
            self.gdf_crs = self.gdf.crs
            self.user_entries = self.gdf.shape[0]
            final_df = historicalave.copy()
            final_df['Well ID or well name'] = well_id
            return user_df, final_df

        # Alternative pathway for PEST
        elif usermode is False:
            # user_df = pd.read_csv(self.user_file)
            user_df['sample_dt'] = pd.to_datetime(user_df['sample_dt'])
            self.run_DTW_ML_flag = True

            # Convert chemistry to natural-log
            for chem in chemlist:
                # Handle reported chem values == 0 by making them 
                # really small for log transform
                user_df[f'{chem}'] = [np.log(1e-6) if i == 0. else np.log(i) 
                                      for i in user_df[f'{chem}']]

            # Make sure sample_dt is string; shapefile export requrement
            user_df['sample_dt'] = user_df['sample_dt'].dt.strftime('%Y-%m-%d')
            gdf = gpd.GeoDataFrame(user_df,
                      crs=CRS("epsg:4269"), 
                      geometry=gpd.points_from_xy(user_df.longitude_deg,
                                                  user_df.latitude_deg)
                      )
                           
            self.gdf = gdf.to_crs(epsg=26916)
            self.gdf_crs = self.gdf.crs
            self.user_entries = self.gdf.shape[0]
            final_df = user_df.copy()
            return user_df, final_df

        else:
            raise ValueError('usermode must be a boolean (`True` or `False`)')

    def setup_for_ML(self, final_df, usermode, verbose, 
                     data_in_dir = data_in_dir):
        
        ## Run county check ##
        shpdir = os.path.join(gisdir, 'WI_Buff1km/')
        ctydir =  os.path.join(gisdir, 'WI_County/')
        
        county_shp = os.path.join(ctydir, 'ctyppoly.shp')
        wi_counties = gpd.read_file(county_shp)
        wi_counties = wi_counties.to_crs(self.gdf_crs)

        cty_check_gdf = gpd.sjoin(self.gdf, 
                                  wi_counties[['CTY_NAME', 'geometry']], 
                                  how='inner', predicate='intersects',  
                                  rsuffix='county_shp')
        counties = cty_check_gdf['CTY_NAME'].unique().tolist()
        checked_entries = cty_check_gdf.shape[0]

        if checked_entries != self.user_entries:
            if usermode is True:
                print('*****************************************************'\
                      '*****************\n'\
                      '*****************************************************'\
                      '*****************\n'\
                      'The location of the well is not within Wisconsin.  '\
                      'Please review \nthe latitude and longitude values '\
                      'provided in your input Excel \nfile.  Note that '\
                      'longitude is negative in the western hemisphere.\n'\
                      '*****************************************************'\
                      '*****************\n'\
                      '*****************************************************'\
                      '*****************')
                raise ValueError('The supplied well is '\
                                  'located outside of Wisconsin.')
            else:
                raise ValueError('One or more of the supplied wells ' \
                                  'appear to be located outside of ' \
                                  'Wisconsin.')

        county_dict = {
            'Adams': 'Adams',
            'Ashland': 'Ashland',
            'Barron': 'Barron',
            'Bayfield': 'Bayfield',
            'Brown': 'Brown',
            'Buffalo': 'Buffalo',
            'Burnett': 'Burnett',
            'Calumet': 'Calumet',
            'Chippewa': 'Chippewa',
            'Clark': 'Clark',
            'Columbia': 'Columbia',
            'Crawford': 'Crawford',
            'Dane': 'Dane',
            'Dodge': 'Dodge',
            'Door': 'Door',
            'Douglas': 'Douglas',
            'Dunn': 'Dunn',
            'Eau Claire': 'EauClaire',
            'Florence': 'Florence',
            'Fond du Lac': 'Fonddulac',
            'Forest': 'Forest',
            'Grant': 'Grant',
            'Green': 'Green',
            'Green Lake': 'GreenLake',
            'Iowa': 'Iowa',
            'Iron': 'Iron',
            'Jackson': 'Jackson',
            'Jefferson': 'Jefferson',
            'Juneau': 'Juneau',
            'Kenosha': 'Kenosha',
            'Kewaunee': 'Kewaunee',
            'La Crosse': 'LaCrosse',
            'Lafayette': 'Lafayette',
            'Langlade': 'Langlade',
            'Lincoln': 'Lincoln',
            'Manitowoc': 'Manitowoc',
            'Marathon': 'Marathon',
            'Marinette': 'Marinette',
            'Marquette': 'Marquette',
            'Menominee': 'Menominee',
            'Milwaukee': 'Milwaukee',
            'Monroe': 'Monroe',
            'Oconto': 'Oconto',
            'Oneida': 'Oneida',
            'Outagamie': 'Outagamie',
            'Ozaukee': 'Ozaukee',
            'Pepin': 'Pepin',
            'Pierce': 'Pierce',
            'Polk': 'Polk',
            'Portage': 'Portage',
            'Price': 'Price',
            'Racine': 'Racine',
            'Richland': 'Richland',
            'Rock': 'Rock',
            'Rusk': 'Rusk',
            'Sauk': 'Sauk',
            'Sawyer': 'Sawyer',
            'Shawano': 'Shawano',
            'Sheboygan': 'Sheboygan',
            'St Croix': 'StCroix',
            'Taylor': 'Taylor',
            'Trempealeau': 'Tremp',
            'Vernon': 'Vernon',
            'Vilas': 'Vilas',
            'Walworth': 'Walworth',
            'Washington': 'Wash',
            'Washburn': 'Washburn',
            'Waukesha': 'Waukesha',
            'Waupaca': 'Waupaca',
            'Waushara': 'Waushara',
            'Winnebago': 'Winnebago',
            'Wood': 'Wood'
        }
        
        #################################
        # Extract GIS data for ML models #
        #################################
        
        print('-- Extracting gis data --')
        if verbose is True:
            print('-- Calculating mean raster value in buffer areas'
                  'for ageML --')

        m1_vars = ['mean_twi', 
                   'stream_den', 
                   'mean_subsurf_contime', 
                   'et_reitz_m',
                   'Rech_eff_myr_Reitz_mean', 
                   'Rech_mmyr_SWBNawqa_mean',
                   'pet_inyr', 
                   'wi_anox_do_and_fe',
                   'SSURGO_avg_fc_mean', 
                   'SSURGO_avg_kfact_mean', 
                   'SSURGO_HYDCLASS_mean', 
                   'SSURGO_AVG_NO10_mean',
                   'SSURGO_hydgrp_B_mean',
                   'SSURGO_AVG_NO4_mean',
                   'SSURGO_AWS25_mean',
                   'SSURGO_wtdep_min_mean',
                   'SSURGO_avg_silt_mean',
                   'SSURGO_avg_bd_mean',
                   'SSURGO_avg_clay_mean',
                   'SSURGO_avg_awc_mean']

        m1_fnams = ['twi_b1km.tif', 'sden_b1km.tif',
                    'ssc_b1km.tif', 'et_b1km.tif', 
                    'RC_eff_0013v2_clip_m.tif', 
                    'SWB_Nawqa_mm_clip.tif', 
                    'hlr1_b1km.tif', 'wi_anox_do&fe.asc',
                    'SSURGO_avg_fc_mean.tif', 
                    'SSURGO_avg_kfact_mean.tif', 
                    'SSURGO_HYDCLASS_mean.tif', 
                    'SSURGO_AVG_NO10_mean.tif',
                    'SSURGO_hydgrp_B_mean.tif',
                    'SSURGO_AVG_NO4_mean.tif',
                    'SSURGO_AWS25_mean.tif',
                    'SSURGO_wtdep_min_mean.tif',
                    'SSURGO_avg_silt_mean.tif',
                    'SSURGO_avg_bd_mean.tif',
                    'SSURGO_avg_clay_mean.tif',
                    'SSURGO_avg_awc_mean.tif']
            
        m1_dict = dict(zip(m1_vars, m1_fnams))

        for var in m1_vars:
            if verbose is True:
                print('  processing var: {}'.format(var))
            input_raster = os.path.join(shpdir, '{}'.format(m1_dict[var]))
            var_list = gisutils.mean_buffer_value(input_raster, self.gdf)
            final_df['{}'.format(var)] = var_list
                
        if verbose is True:
            print('-- Extracting point values from rasters for ageML --')

        m2_vars = [
            'LP1', 'LP2', 'rech48grd_wolock', 
            'DSD1', 'alt_ft_NAVD88', 'LP5', 
            'LP3', 'DSD4', 'DSD3', 'LP8', 'LP6',
            'A_Fe', 'C_C_Inorg', 'A_C_Inorg', 
            'A_C_Org', 'C_C_Org']

        m2_fnams = [
            'lp1_b1km.tif', 'lp2_b1km.tif', 're48_b1km.tif', 'dsd1_b1km.tif', 
            'ned_b1km.tif', 'lp5_b1km.tif', 'lp3_b1km.tif', 'dsd4_b1km.tif', 
            'dsd3_b1km.tif', 'lp8_b1km.tif', 'lp6_b1km.tif','afe5k.tif', 
            'cci5k.tif', 'aci5k.tif', 'aco5k.tif', 'C_C_org.tif']

        m2_dict = dict(zip(m2_vars, m2_fnams))

        for var in m2_vars:
            if verbose is True:
                print('  processing var: {}'.format(var))
            input_raster = os.path.join(shpdir, '{}'.format(m2_dict[var]))
            var_list = gisutils.raster_point_value(input_raster, self.gdf)
            # ned_b1km has units of m, need to convert to ft
            if var == 'alt_ft_NAVD88':
                    var_list = [i * 3.28084 for i in var_list]
            final_df['{}'.format(var)] = var_list
            
        # Extract depth to bedrock and make temp column in dataframe 
        # with point value
        input_raster = os.path.join(shpdir, 'brkdpth_b1km.tif')
        var_list = gisutils.raster_point_value(input_raster, self.gdf)    
        final_df['brkdpth_calculated'.format(var)] = var_list
            
        if verbose is True:
            print('-- Calculating land use variables for ageML --')

        m3_vars = ['LU1982_crops', 'LU1982_pasture', 'LU1982_lowuse',
                   'LU1982_developed', 'LU1982_grazing', 'LU1982_wetlands']
        m3_lu_nums = [43, 44, [50, 60], [21, 22, 23, 24, 25, 26, 27], 45, 12]
        m3_dict = dict(zip(m3_vars, m3_lu_nums))

        for var in m3_vars:
            if verbose is True:
                print('  processing var: {}'.format(var))
            input_raster = os.path.join(shpdir, 'lu82_b1km.tif') 
            var_list = gisutils.landuse_catergory_value(input_raster, self.gdf, 
                                               m3_dict[var], verbose=verbose)
            final_df['{}'.format(var)] = var_list
        if verbose is True:
            print('-- Calculating weighted drainage index for ageML --')

        input_raster = os.path.join(shpdir, 'mur_90m2_b1km.tif')
        drainageclass_file = os.path.join(shpdir, 'WI_DrainageClass.csv')
        var_list = gisutils.weighted_drainage_index(input_raster, self.gdf, 
                                           drainageclass_file)
        final_df['weighted_drainage_index'] = var_list

        if verbose is True:
            print('-- Extracting sedaq_quathick value for ageML --')
        results_list = []
        well_nums = []
        for county in counties:
            if verbose is True:
                print(f'  {county}')
            gdf_county = cty_check_gdf.loc[cty_check_gdf['CTY_NAME'] == 
                                           county]
            county_well_nums = gdf_county['well_num'].tolist()
            shapepath = ctydir + county_dict[county] + '/' + \
                        county_dict[county] + '_sedaq_quathick.shp'
            county_results = gisutils.shapefile_point_value(shapepath, gdf_county)
            results_list.extend(county_results)
            well_nums.extend(county_well_nums)
            
        results_df = pd.DataFrame({'well_num':well_nums,
                                   'sedaq_quathick': results_list})
        final_df = final_df.merge(results_df, on = 'well_num')
        if 'sedaq_quathick_y' in final_df.columns:
            final_df = final_df.drop(columns = 'sedaq_quathick_y')
        if 'sedaq_quathick_x' in final_df.columns:
            final_df = final_df.rename(columns = {'sedaq_quathick_x' : 'sedaq_quathick'})
        
        return final_df

    def setup_run_DTW_ML(self, final_df, usermode, verbose, 
                         data_in_dir = '../data_in/'):
        #################################
        # generate input and run DTW ML #
        #################################
        
        # If user did not supply DTW info, get it from DTW_ML
        if self.run_DTW_ML_flag:  
            dtw_df = final_df.copy()
            if verbose is True:
                print('-- Pulling gis data for DTW ML specific variables --')

            # Drop unneeded parameters
            drop_list = [
                'LP8',
                'LU1982_developed',
                'LU1982_crops',
                'LU1982_pasture',
                'LU1982_grazing',
                'LU1982_lowuse',
                'A_Fe',
                'A_C_Inorg',
                'A_C_Org',
                'C_C_Inorg',
                'p00010_imp',
                'p00095_imp',
                'O2_obs',
                'pH',
                'p00405_imp',
                'p00608_imp',
                'p00671_imp',
                'p00915_imp',
                'p00925_imp',
                'p00930_imp',
                'p00935_imp',
                'p00940_imp',
                'p00945_imp',
                'p00950_imp',
                'p00955_imp',
                'Fe_obs',
                'p01056_imp',
                'NO3_obs',
                'lev_va_merge_nwis_ft',
                'scrndepbot_ft',
                'scrndeptop_ft',
                'NO3_obs',
                'mean_twi',
                'SSURGO_AVG_NO10_mean',
                'SSURGO_AVG_NO4_mean',
                'SSURGO_AWS25_mean',
                'SSURGO_avg_awc_mean',
                'SSURGO_avg_bd_mean',
                'SSURGO_avg_kfact_mean',
                'brkdpth_calculated',
                'sample_dt',
                'sedaq_quathick']

            dtw_df = dtw_df.drop(columns=drop_list)

            rename_dict = {
                'Rech_eff_myr_Reitz_mean':'eff_rech_myr',
                'et_reitz_m':'et_reitz_myr',
                'Rech_mmyr_SWBNawqa_mean':'eff_rech_mmyr_SWBNawqa',
                'rech48grd_wolock':'wolock_rech_mmyr',
                'SSURGO_avg_fc_mean':'SSURGO_avg_fc',
                'SSURGO_avg_silt_mean':'SSURGO_avg_silt',
                'SSURGO_avg_clay_mean':'SSURGO_avg_clay',
                'SSURGO_wtdep_min_mean':'SSURGO_wtdep_min',
                'SSURGO_HYDCLASS_mean':'SSURGO_HYDCLASS',
                'SSURGO_hydgrp_B_mean':'SSURGO_HYDGRPB'}

            dtw_df = dtw_df.rename(columns=rename_dict)
            # Add new buffer mean values
            # Method 1 variables 
            if verbose is True:
                print('-- Calculating mean raster value in buffer '
                      'areas for DTW ML --')

            m1_vars = [
                'twi_wetness',
                'flow_dist',
                'wolock_bfi_percent',
                'bayless_kz_ftd',
                'bayless_trans_ft2d',
                'bayless_thick_glac_ft',
                'SSURGO_avg_om',
                'SSURGO_avg_ksat',
                'SSURGO_avg_por',
                'SSURGO_avg_sand']

            m1_fnams = [
                'twiwetn_b1km.tif',  
                'flowdis_b1km.tif',
                'wolock_bfi.tif',
                'sir155105_kz.tif',
                'sir155105_t.tif',
                'sir155105_gt.tif',
                'SSURGO_avg_om.tif',
                'SSURGO_avg_ksat.tif',
                'SSURGO_avg_por.tif',
                'SSURGO_avg_sand.tif']
                
            m1_dict = dict(zip(m1_vars, m1_fnams))

            for var in m1_vars:
                if verbose is True:
                    print('  processing var: {}'.format(var))
                input_raster = os.path.join(wtmldir, 
                                            '{}'.format(m1_dict[var]))
                var_list = gisutils.mean_buffer_value(input_raster, self.gdf)
                dtw_df['{}'.format(var)] = var_list

            #  Method 2 variables
            if verbose is True:
                print('-- Extracting point values from rasters for '
                      'DTW ML--')

            m2_vars = [
                'DSD2', 'DSD5', 'DSD6', 'DSD7', 
                'LP4', 'LP7', 'zell_wc_wtavg',
                'zell_trans', 'zell_dtw']

            m2_fnams = [
                'dsd2.tif', 'dsd5.tif', 'dsd6.tif', 'dsd7.tif', 
                'lp4.tif', 'lp7.tif', 'zell_wc_wtavg.tif', 
                'zell_trans.tif', 'zell_dtw.tif']

            m2_dict = dict(zip(m2_vars, m2_fnams))
            for var in m2_vars:
                if verbose is True:
                    print('  processing var: {}'.format(var))
                input_raster = os.path.join(wtmldir, 
                                            '{}'.format(m2_dict[var]))
                var_list = gisutils.raster_point_value(input_raster, self.gdf)
                dtw_df['{}'.format(var)] = var_list

            #  Method 5 variables 
            if verbose is True:
                print('-- Extracting point values from shapefiles for '
                      'DTW ML --')

            m5_vars = [
                'Terrane',
                'UNIT_NAME',
                'ROCKDESC']
            m5_cols = [
                'Terrane',
                'UNIT_NAME',
                'ROCKDESC']
            m5_fanmes = [
                'HydrogeologicTerranes_poly.shp',
                'Soller_ds425_SurficialMaterials.shp',
                'NationalGeologicMap.shp']

            m5_dict = dict(zip(m5_vars, m5_fanmes))
            m5_att_dict = dict(zip(m5_vars, m5_cols))

            for var in m5_vars:
                if verbose is True:
                    print('  processing var: {}'.format(var))
                shapepath = os.path.join(wtmldir, m5_dict[var])
                results = gisutils.shapefile_point_value(shapepath, self.gdf, 
                                                attribute=m5_att_dict[var])
                dtw_df['{}'.format(var)] = results

            if verbose is True:
                print('-- Processing BedrockOverlay for DTW ML --')
            dtw_df['BedrockOverlay'] = gisutils.bedrock_overlay(self.gdf, wtmldir, 
                                                       dtw_df, 
                                                       verbose=verbose)

            # Convert dem elevations from ft to m and drop alt_ft_NAVD88
            if verbose is True:
                print('  Converting elevation to meters')
            dtw_df['DEM_LSD_m'] = [i * 0.3048 for i in dtw_df.alt_ft_NAVD88]
            dtw_df = dtw_df.drop(columns='alt_ft_NAVD88')

            dtw_df_final = dtw_df.reset_index()
            dtw_df_final['index'] = [f'"{i+1}"' 
                                     for i in dtw_df_final['index']]
            dtw_df_final = dtw_df_final.rename(columns={'index':''})

            for col in dtw_df_final.columns:
                new_col = f'"{col}"'
                dtw_df_final = dtw_df_final.rename(columns={col:new_col})

            dwt_ml_input = 'WT-ML_input.csv'
            dtw_df_final.to_csv(dwt_ml_input, sep='\t', 
                                index=False, na_rep='NA', 
                                quoting=csv.QUOTE_NONE)

            print('-- Running DTW ML --')
            self.run_DTW_ML_py(dwt_ml_input,
                               dwt_ml_job_file,
                               verbose=verbose)
            dwt_ml_ouptut = 'WT-ML_dtw_preds.csv'
            self.dtw_preds_df = pd.read_csv(dwt_ml_ouptut)

            os.remove(dwt_ml_input) 
            os.remove(dwt_ml_ouptut)

        ##############################################################
        #  Calculate sample depth (z_W) and aquifer thickness (z_A)  #
        #  Sample depth is the depth of the center of the saturated  #
        #  well screen interval below the water table, as per        #
        #  section 3.4 of Green et al. 2021. Note that the NDST will #
        #  use DTW_ML if the user does not supply a depth to water   #
        ##############################################################
        if verbose is True:
            print('-- Calculating Sample Depth (z_W) for ageML --')

        # Handle z_W for GUI - single well  
        if usermode is True:
            if self.run_DTW_ML_flag is True:
                # Get DTW from ML if no user data
                final_df['lev_va_merge_nwis_ft'] = \
                    self.dtw_preds_df.pred_DTW[0]
            if np.any(final_df['lev_va_merge_nwis_ft'] > 
                      # WL below casing
                      final_df['scrndeptop_ft']):  
                final_df['z_W'] = ((final_df['scrndepbot_ft'] + 
                                    final_df['lev_va_merge_nwis_ft']) 
                                    / 2) - final_df['lev_va_merge_nwis_ft']
            # WL above casing (most wells)
            else:  
                final_df['z_W'] = ((final_df['scrndepbot_ft'] + 
                                    final_df['scrndeptop_ft']) 
                                    / 2) - final_df['lev_va_merge_nwis_ft']
        
        # Handle z_W for PEST - many wells  
        else:
            if self.run_DTW_ML_flag is True:
                final_df['lev_va_merge_nwis_ft'].fillna(self.dtw_preds_df
                                                       ['pred_DTW'], 
                                                       inplace=True)

            # Make empty `z_W` to populate for the two possible 
            # WL configurations
            final_df['z_W'] = np.nan
            # 1. Water level above screen top
            final_df.loc[final_df['lev_va_merge_nwis_ft'] > 
                         final_df['scrndeptop_ft'], 'z_W'] = \
                                 ((final_df['scrndepbot_ft'] + \
                                   final_df['lev_va_merge_nwis_ft']) / 2) - \
                                   final_df['lev_va_merge_nwis_ft']
            # 2. Water level below screen top
            final_df.loc[final_df['lev_va_merge_nwis_ft'] <= 
                         final_df['scrndeptop_ft'], 'z_W'] = \
                         ((final_df['scrndepbot_ft'] + \
                         final_df['scrndeptop_ft']) / 2) - \
                         final_df['lev_va_merge_nwis_ft']
        
        # Fill negative values with minimum value; ensures z_W is not negative
        final_df['z_W'] = np.where(final_df['z_W'] < 0, 0.0001,
                                   final_df['z_W'])  

        if verbose is True:
            print('-- Calculating z_A; Aquifer Thickness for ageML --')
        # Calculate z_A as bedrock depth minus depth to water, 
        # or 0.1 if water level deeper than bedock level 
        # as per GreenEtAl2021 Supporting Information
        final_df['z_A'] = final_df['brkdpth_calculated'] - \
                          final_df['lev_va_merge_nwis_ft']

        # Set minimum depth to bedrock 0.1 ft
        if final_df.loc[final_df['z_A'] <= 0].shape[0] > 0:
            final_df.loc[final_df['z_A'] <= 0., 'z_A'] = 0.1

        return final_df

    def setup_run_ageML(self, final_df, verbose, data_in_dir = data_in_dir):
        ###########################
        # Setup for and run ageML #
        ###########################
        
        well_num=final_df['well_num']
        final_df_drop = final_df.drop(columns=['well_num',
                                           'sample_dt',
                                           'latitude_deg', 
                                           'longitude_deg', 
                                           'brkdpth_calculated',
                                           'wi_anox_do_and_fe',
                                           'C_C_Org',
                                           'LU1982_wetlands'])
        final_df_drop = final_df_drop[[
            'scrndepbot_ft', 
            'z_W',
            'NO3_obs',
            'LU1982_crops',
            'LU1982_pasture',
            'p00950_imp',
            'mean_twi',
            'scrndeptop_ft',
            'pH',
            'Fe_obs',
            'p00010_imp',
            'LU1982_lowuse',
            'p00940_imp',
            'pet_inyr',
            'LU1982_developed',
            'p00945_imp',
            'p00955_imp',
            'LP1',
            'LU1982_grazing',
            'p00671_imp',
            'SSURGO_avg_fc_mean',
            'p00095_imp',
            'SSURGO_avg_kfact_mean',
            'LP2',
            'rech48grd_wolock',
            'lev_va_merge_nwis_ft',
            'stream_den',
            'mean_subsurf_contime',
            'DSD1',
            'p00925_imp',
            'p00405_imp',
            'alt_ft_NAVD88',
            'p00930_imp',
            'LP5',
            'A_Fe',
            'SSURGO_HYDCLASS_mean',
            'LP3',
            'weighted_drainage_index',
            'SSURGO_AVG_NO10_mean',
            'O2_obs',
            'DSD4',
            'p00608_imp',
            'et_reitz_m',
            'C_C_Inorg',
            'p01056_imp',
            'SSURGO_hydgrp_B_mean',
            'DSD3',
            'LP8',
            'SSURGO_AVG_NO4_mean',
            'Rech_eff_myr_Reitz_mean',
            'SSURGO_AWS25_mean',
            'SSURGO_wtdep_min_mean',
            'Rech_mmyr_SWBNawqa_mean',
            'LP6',
            'z_A',
            'p00915_imp',
            'A_C_Inorg',
            'A_C_Org',
            'SSURGO_avg_silt_mean',
            'sedaq_quathick',
            'SSURGO_avg_bd_mean', 
            'p00935_imp',
            'SSURGO_avg_clay_mean',
            'SSURGO_avg_awc_mean']]

        headers = final_df_drop.columns.tolist()
         
        #  Add double quotes (") around each header for ageML input file
        final_headers = []
        for header in headers:
            final_headers.append('"{}"'.format(header))
            
        header_dict = dict(zip(headers, final_headers))

        final_df_rename = final_df_drop.rename(header_dict, axis=1)
        
        shape_check = final_df_rename.shape
        assert shape_check[1] == 64 # should be 64 cols

        # Write ageML input file -- must write, can't pass as df
        final_df_rename.to_csv('ageML_input.txt', 
                                index=False, sep='\t', 
                                na_rep='NA', 
                                quoting=csv.QUOTE_NONE)
        
        # run ageML
        ageML_input_data = 'ageML_input.txt'
        
        print('-- Running ageML --')

        self.run_age_ml_py(ageML_input_data,
                           ageML_job_file,
                           verbose=verbose)

        ageML_output_data = 'ageML_input_age.txt'
        ageML_output = pd.read_csv(ageML_output_data, 
                                   sep = '\t', header = (0))
        ageML_output['well_num'] = well_num

        os.remove(ageML_input_data)  
        os.remove(ageML_output_data)
        
        return ageML_output

    def calc_ko2(self, final_df, data_in_dir = data_in_dir):
        #######################################
        # Generate input for k_O2 calculation #
        #######################################
        final_df_kO2 = final_df.copy()
        shpdir = os.path.join(gisdir, 'WI_Buff1km/')
        O2_coeffs = pd.read_csv(O2_coeffs_file, 
                                delim_whitespace = True)

        geo_shp = os.path.join(shpdir, 'Soller_stack_map_clip.shp')
        geo_class = 'Coarse-grained stratified sediment'
        overlap_dict = gisutils.soller_geology_pct_buffer_area(self.gdf, 
                                                      geo_shp, geo_class)

        final_df_kO2['pct_buffer_soller_coarse_gr_strat_sed'] = \
                        [overlap_dict.get(i, 0.) for i in final_df_kO2.index]

        #  Calc uz_thick & convert to m
        final_df_kO2['uz_thick'] = [i*0.3048 if i <= 200. else np.nan 
                                    for i in final_df_kO2
                                    ['lev_va_merge_nwis_ft']] 
        # Populate with DTW_ML info if user DTW is Nan or >200ft                            
        if self.run_DTW_ML_flag:  
            dwt_dict = dict(zip(self.dtw_preds_df.well_num, 
                                self.dtw_preds_df.pred_DTW))
            final_df_kO2['WT-ML_dtw_ft'] = [dwt_dict[i] for i in 
                                            final_df_kO2.well_num]
            final_df_kO2['WT-ML_dtw_m'] = [i*0.3048 for i in 
                                           final_df_kO2['WT-ML_dtw_ft']]
            final_df_kO2['uz_thick'].fillna(final_df_kO2['WT-ML_dtw_m'], 
                                            inplace=True)
        final_df_kO2.loc[final_df_kO2['uz_thick'] <= 0.0, 'uz_thick'] = \
                                                          (0.1 * 0.3048)
        final_df_kO2.to_csv('final_df_kO2.csv')

        O2_rate_list = []
        print('-- Calculating redox rate (k_O2) --')
        for i in range(len(final_df_kO2)):
            O2_rate_list.append(gisutils.calc_O2_rate(final_df_kO2, i, O2_coeffs))

        final_df_kO2['k_o2'] = O2_rate_list

        return final_df_kO2

    def make_user_df_w_params(self, user_df,
                              MP_flag,
                              usermode = True,
                              verbose = False,
                              data_in_dir = data_in_dir):

        """Run GIS attribute functions for an NDST user's well, build 
        inputs for machine learning (ML) models (ageML, dtwML, and the k_O2 
        regression), run the ML models, append GIS attributes and ML 
        results to user sample data, and return as a Pandas dataframe. 
        Can also optionally write dataframe returned by function to file 
        by supplying an outfile path. 

        Parameters
        ----------
        user_file : path to user's sample input excel file
        data_in_dir :  path to directory that contains WI and 
                       county-size gis files for ageML and WT-ML and 
                       ML .joblib files
        outfile_path : (Optional) path to output file. Must be .csv 
                       file. If supplied, writes final dataframe to 
                       csv.
        verbose : bool, default False
                  if True, print all function progress messages.

        Returns
        -------
        df : Pandas dataframe of user sample data with GIS attributes 
             and ML results
        """
        t0 = time.time()

        # Setup input directories relative to data_in_dir 
        print('\nRunning GIS attribute functions and '
              'machine learning (ML) models')
        # Quick checks on outpath
        if self.outfile_path is not None: 
            assert isinstance(self.outfile_path, str), 'outfile_path \
                                                        must be a str'
            assert self.outfile_path.endswith('.csv'), 'outfile must be .csv'

        user_df, final_df = self.process_chem_data(user_df, usermode)
        final_df = self.setup_for_ML(final_df, usermode, verbose)
        final_df = self.setup_run_DTW_ML(final_df, usermode, verbose)
        
        if MP_flag == False:
            ageML_output = self.setup_run_ageML(final_df, verbose)

        final_df_kO2 = self.calc_ko2(final_df)
        
        if MP_flag == False:
            final_pars_df = pd.merge(final_df_kO2, 
                                 ageML_output[['well_num', 'total_tt_years']], 
                                 on='well_num', how='inner')
        else:
            final_pars_df = final_df_kO2.copy()
                                 
        # Remove duplicate columns from the long-term average DF 
        # prior to merge.
        dupcols = ['sample_dt', 'NO3_obs', 'O2_obs', 'pH', 'p00010_imp', 
                   'p00950_imp', 'p00940_imp', 'p00945_imp', 'p00955_imp', 
                   'p00671_imp', 'p00095_imp', 'p00925_imp', 'p00405_imp', 
                   'p00930_imp', 'p00608_imp', 'p01056_imp', 'p00915_imp', 
                   'p00935_imp', 'Fe_obs', 'scrndepbot_ft', 'scrndeptop_ft', 
                   'latitude_deg', 'longitude_deg']
        final_pars_df.drop(columns=dupcols, inplace=True) 
        # Remove DTW (nan) from user DF
        user_df.drop(columns=['lev_va_merge_nwis_ft'], inplace=True)  

        # Both GUI and Pest proceedures use "user_df" and "final_pars_df"
        # to create the "everything" dataframe.  The "final_df" created
        # above contains GUI vs PEST specific formatted data (eg, annual 
        # average for GUI; individual samples for PEST).
        if usermode:
            for drop_this in ['altitude', 'pump_Q']:
                if drop_this in final_pars_df.columns:
                    # Prevent duplication upon merge
                    final_pars_df.drop(columns = [drop_this], inplace=True) 
            self.everything = pd.merge(user_df, final_pars_df, 
                                       on=['well_num'], how='inner')
        else:
            final_pars_df.drop(columns = ['ORIG_HRZ_COLL_MTHD_CODE'], 
                               inplace = True)
            self.everything = pd.merge(user_df, final_pars_df, on=['well_num',
                                       'site_no'], how='inner')
            # Convert nitrate obs from log space
            self.everything['NO3_obs'] = [np.exp(i) for i in
                                          self.everything['NO3_obs']]
        self.everything['sample_dt'] = pd.to_datetime(self.everything
                                                     ['sample_dt'])
        # When the input file has an empty date column, the above line doesn't
        # work properly.
        if self.everything['sample_dt'].isnull().any():
            self.everything = self.everything.assign(sample_dt = datetime.today())

        # Convert to string for backward compatability
        for i in self.everything.index:  
            self.everything.loc[i, 'sample_dt'] = \
            self.everything.loc[i].sample_dt.strftime("%Y-%m-%d")

        if 'Well ID or well name_x' in self.everything.columns:
            self.everything = self.everything.rename(columns = {'Well ID or '
                                      'well name_x' : 'Well ID or well name'})

        if self.outfile_path is not None:
            self.everything.to_csv(self.outfile_path, index=False)
            #print(f'wrote {self.outfile_path}\n')
        if debug:
            print("Finished in {:.2f}s\n".format(time.time() - t0))

        return self.everything

    def build_user_df(self, MP_flag = False):
        temp_user_df = self.pull_user_input()
        check_location(temp_user_df)
        self.user_df = self.make_user_df_w_params(user_df=temp_user_df, 
                                                  MP_flag=MP_flag,
                                                  usermode=True,
                                                  verbose=False,
                                                  data_in_dir=data_in_dir)
        self.pull_septic_new(self.user_df)
        self.pull_IBIS(self.user_df)
        self.gdf = gpd.GeoDataFrame(self.user_df,
                       crs=CRS("epsg:4326"),
                       geometry=gpd.points_from_xy(self.user_df.longitude_deg,
                                                   self.user_df.latitude_deg))
        self.params = dict()
        self.user_df = self.find_grid_pars(self.gdf, self.user_df, 
                                           self.params)
        return self