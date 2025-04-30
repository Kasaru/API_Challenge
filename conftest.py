import pytest
import requests


@pytest.fixture(scope="session")
def header():
    url = 'https://apichallenges.herokuapp.com/challenger'
    response = requests.post(url)
    token = response.headers['X-Challenger']
    header = {'X-Challenger': f'{token}'}
    print(header)
    return header

