import sys, os

from no3gwt.config import *

def test_gisdir():
    # test out platform dependant paths
    assert gisdir == '../data_in/gis'
    assert O2_coeffs_file == '../data_in/O2_coeffs.txt'
    assert septic_file == '../data_mid/septic_all7.nc'
    assert ag_input_path == '../data_mid/ibis_21_int_clipped.nc'
    assert flux_file == '../data_mid/flux_21_int_clipped.nc' 
    assert rdsdir == '../data_in/ml_models/'
    assert ageML_job_file == os.path.join(rdsdir,'age_ml_model.joblib')
    assert dwt_ml_job_file == os.path.join(rdsdir,'wt_ml_model.joblib')
    assert O2_init == 9.8
    assert O2_rate_intercept == 0.113029469814271
    assert O2_min_rate == 0.066
    assert O2_max_rate == 100