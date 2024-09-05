def test_project_root_path(project_root_path):
    assert project_root_path.endswith('no3gwt')
    assert not project_root_path.endswith('no3gwt/no3gwt')


