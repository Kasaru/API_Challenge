import json

import pytest
import requests

import endpoints
from utils.data_generation import DataGeneration

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

        assert response.status_code == 404, f'Status code is not 404: {response.status_code}'

    @pytest.mark.post_todo_with_done_status_negative
    def test_post_todo_with_done_status_negative(self,header):
        print('Issue a POST request to create a todo but fail validation on the `doneStatus` field')

        random_name = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        random_status = DataGeneration.generate_word()

        url = base_url + endpoints.todos

        body = {
            'title': random_name,
            'doneStatus': random_status,
            'description': random_description
        }

        response = requests.post(url,headers=header,json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Failed Validation: doneStatus should be BOOLEAN but was STRING", ('Incorrect error'
                                                                                                                         f'message: {response.json()['errorMessages'][0]}')



