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

    @pytest.mark.post_todo_with_string_done_status_negative
    def test_post_todo_with_string_done_status_negative(self,header):
        print('Issue a POST request to create a todo but fail validation on the `doneStatus` field')

        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        random_status = DataGeneration.generate_word()

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': random_status,
            'description': random_description
        }

        response = requests.post(url,headers=header,json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Failed Validation: doneStatus should be BOOLEAN but was STRING", ('Incorrect error'
                                                                                                                         f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.post_todo_with_int_done_status_negative
    def test_post_todo_with_int_done_status_negative(self, header):
        print('Issue a POST request to create a todo but fail validation on the `doneStatus` field')

        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        random_status = DataGeneration.generate_int()

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': random_status,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Failed Validation: doneStatus should be BOOLEAN but was NUMERIC", ('Incorrect error'
                                                                                         f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_title
    def test_too_long_title(self, header):
        print('Issue a POST request to create a todo but fail length validation on the `title` field because title exceeds more than maximum allowable characters.')
        random_title = DataGeneration.generate_long_text(51)
        random_description = DataGeneration.generate_description()

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Failed Validation: Maximum allowable length exceeded for title - maximum allowed is 50", ('Incorrect error'
                                                                                             f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_title_with_space
    def test_too_long_title_with_space(self, header):
        print('Issue a POST request to create a todo but fail length validation on the `title` field because title exceeds maximum allowable characters + space.')
        random_title = DataGeneration.generate_long_text(50) + ' '
        random_description = DataGeneration.generate_description()

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Failed Validation: Maximum allowable length exceeded for title - maximum allowed is 50", ('Incorrect error'
                                                                                             f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_description
    def test_too_long_description(self, header):
        print(
            'Issue a POST request to create a todo but fail length validation on the `description` because your description exceeds more than maximum allowable characters.')
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(201)

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][
                   0] == "Failed Validation: Maximum allowable length exceeded for description - maximum allowed is 200", (
            'Incorrect error'
            f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_description_with_space
    def test_too_long_description_with_space(self, header):
        print(
            'Issue a POST request to create a todo but fail length validation on the `description` because your description exceeds maximum allowable characters. + space.')
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(200) + ' '

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][
                   0] == "Failed Validation: Maximum allowable length exceeded for description - maximum allowed is 200", (
            'Incorrect error'
            f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_content
    def test_too_long_content(self,header):
        print('Issue a POST request to create a todo but fail payload length validation on the `description` because your whole payload exceeds maximum allowable 5000 characters.')
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(5000)

        url = base_url + endpoints.todos

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 413, f'Status code is not 413: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Error: Request body too large, max allowed is 5000 bytes", (
                                                        f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.unrecognised_field
    def test_unrecognised_field(self,header):
        print('Issue a POST request to create a todo but fail validation because your payload contains an unrecognised field.')

        url = base_url + endpoints.todos

        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
            'unrecognisedField': 'unrecognisedField'
        }

        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'
        assert response.json()['errorMessages'][0] == "Could not find field: unrecognisedField", (
                                                        f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.create_todo_via_put
    def test_create_todo_via_put(self,header):
        print('Issue a PUT request to unsuccessfully create a todo')

        url = base_url + endpoints.invalid_todo_endpoint

        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
        }

        response = requests.put(url, headers=header, json=body)

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {print(json.dumps(response.json(), indent=4, ensure_ascii=False))}'