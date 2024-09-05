import os, sys
import pandas as pd
import pytest

"""
test_ml_models.py
----------------------------------
Tests for functions that run ML models using r2py.
"""

import no3gwt.well_setup as ws
from no3gwt.gis_attribute_utils import calc_O2_rate

@pytest.fixture(scope="function")
def user_input_file(project_root_path):
    return(os.path.join(project_root_path, 
                        'data_in', 
                        'example2.xlsx')
                        )

@pytest.fixture(scope="function")
def processed_file(project_root_path):
    return(os.path.join(project_root_path, 
                        'data_in', 
                        'example_input.csv')
                        )

# ageML input data
@pytest.fixture(scope="function")
def ageML_input_data():
    return('no3gwt/tests/data/ageML_input.txt')

# ageML .rds file
@pytest.fixture(scope="function")
def ageML_joblib_file():
    return 'data_in/ml_models/age_ml_model.joblib'

# DTW ML input data
@pytest.fixture(scope="function")
def dwt_ml_input():
    return('no3gwt/tests/data/WT-ML_input.csv')
    
# WT ML .rds file
@pytest.fixture(scope="function")
def dwt_ml_joblib_file():
    return 'data_in/ml_models/wt_ml_model.joblib'

#  k_02 function input file
@pytest.fixture(scope="function")
def kO2_data(test_data_path):
    return os.path.join(test_data_path, 'final_df_kO2.csv')

#  Chris' O2 coefficients for k_O2 function
@pytest.fixture(scope="function")
def O2_coeffs(project_root_path):
    return os.path.join(project_root_path, 'data_in', 'O2_coeffs.txt')


def test_run_ageML(ageML_input_data, ageML_joblib_file, test_data_path):
    ws_class = ws.WellInfo(user_input_file)
    ws_class.run_age_ml_py(ageML_input_data, model_path=ageML_joblib_file)
    ageML_output_data = os.path.join(test_data_path, 'ageML_input_age.txt')
    ageML_output = pd.read_csv(ageML_output_data, sep = '\t', header = (0))
    assert ageML_output.shape == (1,67)
    assert ageML_output.preds.values[0] == 0.9302217553506676
    assert ageML_output.total_tt_years.values[0] == 2.923897978906668
     

def test_run_DTW_ML(dwt_ml_input, dwt_ml_joblib_file, test_data_path):
    ws_class = ws.WellInfo(user_input_file)
    ws_class.run_DTW_ML_py(dwt_ml_input, model_path=dwt_ml_joblib_file)
    dwt_ml_ouptut = os.path.join(test_data_path, 'WT-ML_dtw_preds.csv')
    dtw_preds_df = pd.read_csv(dwt_ml_ouptut)
    assert dtw_preds_df.shape == (1, 56)
    assert dtw_preds_df.pred_DTW.values[0] == 31.839316855222894
     

def test_calc_O2_rate(kO2_data, O2_coeffs):
    final_df_kO2 = pd.read_csv(kO2_data, index_col=0)
    O2_coeffs = pd.read_csv(O2_coeffs, 
                            delim_whitespace = True)
    O2_rate_list = []
    for i in range(len(final_df_kO2)):
        O2_rate_list.append(calc_O2_rate(final_df_kO2, i, O2_coeffs))
    final_df_kO2['k_o2'] = O2_rate_list
    assert final_df_kO2.k_o2.values[0] == 0.066
