'''
Configuration file for the Wisconsin Nitrate Decision Support Tool (WI-NDST).

This file contains variables that are assigned information about the directory
structure of the local computer setup, parameter values, and input file names 
(& paths) that should NOT change under normal operation. Indeed, modification 
of these variables should be avoided unless directed to do so for a very 
specific (and rare) reason.  The variables are specified here rather than 
"hard-coded" into the NDST software files in order to 1. provide greater 
transparancy, and 2. simplify possible future software updates. The variables 
are defined as follows:

import os : A Python library; NOT a variable.
    "os" is an open source library (computer code) that facilitates manipulation
    of directories on computers.  It is imported here to "join" subdirectories
    in some of the variables below.
data_in_dir : string
    Relative path to the folder containing the user's input data for their well
    of interest (for example, the "example_multiple_sample_input.xlsx" file).
gisdir : string 
    Relative path to the folder containing GIS data used by the statistical and
    Machine Learning support models.
pestdir : string 
    Relative path to the folder containing files that characterize the Monte 
    Carlo realizations generated during the calibration process.
output_path : string 
    Relative path to the folder containing output (a PDF file) from each 
    execution of the MC_current or MC_future functions.
outfile_path: string
    Relative path to the file containing a .csv version of the user_df
    that has both user-supplied information and gis and ML model derived
    information about the well. This file is not used by the rest of the code,
    but is provided in case the user would like to look at some of the values.
septic_file : string 
    Relative path and name for the file that contains spatially and 
    historically variable nitrate leaching rate estimates from septic systems.
ag_input_path : string 
    Relative path and name for the file that contains spatially and 
    historically variable nitrate leaching rate estimates from agricultural
    sources.
flux_file : string 
    Relative path and name for the file that contains spatially and 
    historically variable water infiltrated below the root zone. These data
    come from the same support model that generates the "ag_input_path" file.
sep_out_file : string 
    Relative path and name for the output file that stores data from the
    "septic_file" that is specific to the location of the user's selected well.
N_out_file : string 
    Relative path and name for the output file that stores data from the
    "ag_input_path" file that is specific to the location of the user's 
    selected well.
DTW_path : string 
    Relative path and name for the file that represents the depth to water
    Machine Learning support model.
ageML_path : string 
    Relative path and name for the file that represents the Machine Learning 
    support model that computes mean groundwater age for the WI-NDST.
 O2_init : float
    The initial oxygen concentration at the water table in mg/L.
O2_coeffs_file : string 
    Relative path and name for the file that contains trained ("calibrated") 
    coefficient values for the oxygen reduction rate support model.
O2_rate_intercept : float 
    The trained ("calibrated") intercept value for the oxygen reduction rate
    support model.
O2_min_rate : float 
    The minimum oxygen reduction rate allowed for use with the WI-NDST. Any 
    rate computed by the oxygen reduction support model for a well of
    interest that is less than this value will be set to this value.
O2_max_rate : float 
    The maximum oxygen reduction rate allowed for use with the WI-NDST. Any 
    rate computed by the oxygen reduction support model for a well of
    interest that is greater than this value will be set to this value.
grid_file : string 
    Relative path and name for the file that represents the USGS National grid
    clipped to the state of Wisconsin.
par_ens_file : string 
    Relative path and name for the file that contains parameter values for 
    each pilot point for each parameter for each realization from the 
    calibration process.
grid_pars_path : string 
    Relative path and name of the directory containing zipped (gz) gridded 
    files of the parameter values for each parameter for each realization 
    from the calibration process.
'''

import os, platform

# check to see if running on Docker or locally and
# set appropriate paths

if platform.node().startswith('jupyter'):
    data_in_dir = '../../shared-data/data_in/'
else:
    data_in_dir = '../data_in/'
    
gisdir = os.path.join(data_in_dir, 'gis')
O2_coeffs_file = os.path.join(data_in_dir, 'O2_coeffs.txt')

pestdir = '../pest/'
output_path = '../output/'
outfile_path = '../output/user_output.csv'
septic_file = '../data_mid/septic_all7.nc'
ag_input_path = '../data_mid/ibis_21_int_clipped.nc'
flux_file = '../data_mid/flux_21_int_clipped.nc' 
sep_out_file = '../data_mid/Septic_leach_data.csv'
N_out_file = '../data_mid/NO3_leach_data.csv'
rdsdir =  os.path.join(data_in_dir, 'ml_models/')
ageML_job_file = os.path.join(rdsdir,'age_ml_model.joblib')
dwt_ml_job_file = os.path.join(rdsdir,'wt_ml_model.joblib')
wtmldir =  os.path.join(gisdir, 'WT-ML/')
O2_init = 9.8
O2_rate_intercept = 0.113029469814271
O2_min_rate = 0.066
O2_max_rate = 100
grid_file = os.path.join(gisdir, 'NationalGrid/natlGrid_WIbuff_block.tif')
par_ens_file = os.path.join(pestdir, 'ndst_merge_maxsing.2.par.csv')
grid_pars_path = os.path.join(pestdir, 'ies_parameter_ensembles')