import pytest
import requests

import endpoints

base_url = 'https://apichallenges.herokuapp.com'

class TestApiChallengePositive():
    @pytest.mark.get_todo_not_plural
    def test_get_todo(self, header):
        print('Issue a GET request on the `/todo` end point should 404 because nouns should be plural')
        url = base_url + endpoints.invalid_todo_endpoint
        response = requests.get(url, headers=header)

        assert response.status_code == 404, f'Status code is not 404: {response.status_code}'

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        print('Issue a GET request on the `/todos/{id}` end point for a todo that does not exist')
        url = base_url + endpoints.invalid_todo_id
        response = requests.get(url, headers=header)

        assert response.status_code == 404, f'Status code is not 200: {response.status_code}'

