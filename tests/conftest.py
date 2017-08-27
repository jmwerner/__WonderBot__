import pytest

@pytest.fixture(scope="session")
def subreddit_name():
    return 'arresteddevelopment'

@pytest.fixture(scope="session")
def login_file_name():
    return 'login_info.json'
