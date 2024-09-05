import os, shutil
import pandas as pd
import pytest

@pytest.fixture(scope="session")
def project_root_path():
    filepath = os.path.split(os.path.abspath(__file__))[0]
    return os.path.normpath(os.path.join(filepath, '../../'))

@pytest.fixture(scope="session")
def test_data_path(project_root_path):
    """Root folder for the project (with setup.py),
    two levels up from the location of this file.
    """
    return os.path.join(project_root_path, 'no3gwt', 'tests', 'data')

@pytest.fixture(scope="session")
def user_data(project_root_path):
    """Example user data for tests.
    """
    return pd.read_csv(os.path.join(project_root_path, 
                                    'no3gwt', 
                                    'tests', 
                                    'data', 
                                    'user_data.csv'), index_col='well_num')


@pytest.fixture(scope="session", autouse=True)
def tmpdir(project_root_path):
    folder = project_root_path + '/no3gwt/tests/tmp'
    reset = True
    if reset:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    return folder

