from http.client import responses

import pytest
import endpoints
from utils.data_generation import DataGeneration
from utils.methods import BeautifyMethods, HttpMethods

base_url = 'https://apichallenges.herokuapp.com'

class TestApiChallengeNegative():
    @pytest.mark.get_todo_not_plural
    def test_get_todo(self, header):
        print('Issue a GET request on the `/todo` end point should 404 because nouns should be plural')
        url = base_url + endpoints.invalid_todo_endpoint
        response = HttpMethods.get(url, header)

        assert response.status_code == 404, f'Status code is not 404: {response.status_code}'

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        print('Issue a GET request on the `/todos/{id}` end point for a todo that does not exist')
        url = base_url + endpoints.invalid_todo_id
        response = HttpMethods.get(url, header)

        assert response.status_code == 404, f'Status code is not 404: {response.status_code}'

    @pytest.mark.post_todo_with_string_done_status
    def test_post_todo_with_string_done_status(self,header):
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
        response = HttpMethods.post_json(url,header,body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == "Failed Validation: doneStatus should be BOOLEAN but was STRING", ('Incorrect error'
                                                                                                                         f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.post_todo_with_int_done_status
    def test_post_todo_with_int_done_status(self, header):
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
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
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
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
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
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == "Failed Validation: Maximum allowable length exceeded for title - maximum allowed is 50", ('Incorrect error'
                                                                                             f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_description
    def test_too_long_description(self, header):
        print('Issue a POST request to create a todo but fail length validation on the `description` because your description exceeds more than maximum allowable characters.')
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(201)
        url = base_url + endpoints.todos
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][
                   0] == "Failed Validation: Maximum allowable length exceeded for description - maximum allowed is 200", (
            'Incorrect error'
            f'message: {response.json()['errorMessages'][0]}')

    @pytest.mark.too_long_description_with_space
    def test_too_long_description_with_space(self, header):
        print('Issue a POST request to create a todo but fail length validation on the `description` because your description exceeds maximum allowable characters. + space.')
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(200) + ' '
        url = base_url + endpoints.todos
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
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
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 413, f'Status code is not 413: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
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
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == "Could not find field: unrecognisedField", (
                                                        f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.create_todo_via_put
    def test_create_todo_via_put(self, header):
        print('Issue a PUT request to unsuccessfully create a todo')
        url = base_url + endpoints.invalid_todo_id
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
        }
        response = HttpMethods.put(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == 'Cannot create todo with PUT due to Auto fields id', (
            f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.update_todo_via_post
    def test_update_todo_via_post(self, header):
        print('Issue a POST request for a todo which does not exist. Expect to receive a 404 response.')
        url = base_url + endpoints.invalid_todo_id
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
        }
        response = HttpMethods.post_json(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 404, f'Status code is not 404: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == f'No such todo entity instance with id == {endpoints.invalid_todo_id[endpoints.invalid_todo_id.rfind('/') + 1:]} found', (
            f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.update_todo_via_put_without_title
    def test_update_todo_via_put_without_title(self, header):
        print('Issue a PUT request to fail to update an existing todo because title is missing in payload')
        url = base_url + endpoints.todo_id
        random_description = DataGeneration.generate_description()
        body = {
            'doneStatus': True,
            'description': random_description,
        }
        response = HttpMethods.put(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == 'title : field is mandatory', (
            f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.update_todo_via_put_with_wrong_id
    def test_update_todo_via_put_with_wrong_id(self, header):
        print('Issue a PUT request to fail to update an existing todo because title is missing in payload')
        url = base_url + endpoints.todo_id
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        random_id = DataGeneration.generate_int()
        body = {
            'id': random_id,
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
        }
        response = HttpMethods.put(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 400, f'Status code is not 400: {response.status_code}'
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {BeautifyMethods.print_pretty_json(response.json())}'
        assert response.json()['errorMessages'][0] == f'Can not amend id from {endpoints.todo_id[endpoints.todo_id.rfind('/') + 1:]} to {body['id']}', (
            f'Incorrect error message: {response.json()['errorMessages'][0]}')

    @pytest.mark.get_todos_not_acceptable
    def test_get_todos_not_acceptable(self, header):
        print('Issue a GET request on the `/todos` end point with no `Accept` header present in the message to receive results in default JSON format')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, {**header, 'Accept': 'application/gzip'})
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 406, f"Status code is not 406: {response.status_code}. Response: {response.json()}"
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {response.json()}'
        assert response.json()['errorMessages'][0] == f'Unrecognised Accept Type', (
            f'Incorrect error message: {response.json()["errorMessages"][0]}')

    @pytest.mark.post_todos_not_acceptable_content_type
    def test_post_todos_not_acceptable_content_type(self, header):
        print('Issue a POST request on the `/todos` end point with an unsupported content type to generate a 415 status code')
        url = base_url + endpoints.todo_id
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description,
        }
        response = HttpMethods.post_json(url, {**header, 'Content-Type': '123' },body)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 415, f"Status code is not 415: {response.status_code}. Response: {response.json()}"
        assert 'errorMessages' in response.json(), f'No errorMessage in response, {response.json()}'
        assert response.json()['errorMessages'][0] == f'Unsupported Content Type - 123', (
            f'Incorrect error message: {response.json()["errorMessages"][0]}')

    @pytest.mark.delete_heartbeat
    def test_delete_heartbeat(self, header):
        print('Issue a DELETE request on the `/heartbeat` end point and receive 405 (Method Not Allowed)')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.delete(url,header)
        assert response.status_code == 405, f"Status code is not 405: {response.status_code}. Response: {response.json()}"

    @pytest.mark.patch_heartbeat
    def test_patch_heartbeat(self, header):
        print('Issue a PATCH request on the `/heartbeat` end point and receive 500 (internal server error)')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.patch(url, header,{})
        assert response.status_code == 500, f"Status code is not 500: {response.status_code}. Response: {response.json()}"

    @pytest.mark.trace_heartbeat
    def test_trace_heartbeat(self, header):
        print('Issue a POST request on the `/heartbeat` end point and receive 501 (Not Implemented) when you override the Method Verb to a TRACE')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.trace(url, header)
        assert response.status_code == 501, f"Status code is not 501: {response.status_code}. Response: {response.json()}"

    @pytest.mark.override_delete_heartbeat
    def test_override_delete_heartbeat(self, header):
        print('Issue a POST request on the `/heartbeat` end point and receive 405 when you override the Method Verb to a DELETE')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Delete'},{})
        assert response.status_code == 405, f"Status code is not 405: {response.status_code}. Response: {response.json()}"

    @pytest.mark.override_patch_heartbeat
    def test_override_patch_heartbeat(self, header):
        print('Issue a POST request on the `/heartbeat` end point and receive 500 when you override the Method Verb to a PATCH')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Patch'},{})
        assert response.status_code == 500, f"Status code is not 500: {response.status_code}. Response: {response.json()}"

    @pytest.mark.override_trace_heartbeat
    def test_override_trace_heartbeat(self, header):
        print('Issue a POST request on the `/heartbeat` end point and receive 501 (Not Implemented) when you override the Method Verb to a TRACE')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Trace'},{})
        assert response.status_code == 501, f"Status code is not 501: {response.status_code}. Response: {response.json()}"

    @pytest.mark.post_secret_token_incorrect_uname
    def test_post_secret_token_incorrect_uname(self,header):
        print('Issue a POST request on the `/secret/token` end point and receive 401 when Basic auth username/password is not admin/password')
        url = base_url + endpoints.secret_token
        response = HttpMethods.post_json_basic(url,header,{},'amin', 'password')
        assert response.status_code == 401, f"Status code is not 401: {response.status_code}. Response: {response.json()}"

    @pytest.mark.get_secret_note_invalid_x_auth
    def test_get_secret_note_invalid_x_auth(self, header):
        print('Issue a GET request on the `/secret/note` end point and receive 403 when X-AUTH-TOKEN does not match a valid token')
        url = base_url + endpoints.secret_token
        pre_response = HttpMethods.post_json_basic(url, header, {'test': 'test'}, 'admin', 'password')
        url = base_url + endpoints.secret_note
        response = HttpMethods.get(url, {**header, 'X-AUTH-TOKEN': pre_response.headers['X-AUTH-TOKEN'][:-6]+'kasaru'})
        assert response.status_code == 403, f"Status code is not 403: {response.status_code}. Response: {response.json()}"

    @pytest.mark.get_secret_note_without_x_auth
    def test_get_secret_note_without_x_auth(self, header):
        print('Issue a GET request on the `/secret/note` end point and receive 401 when no X-AUTH-TOKEN header present')
        url = base_url + endpoints.secret_note
        response = HttpMethods.get(url, header)
        assert response.status_code == 401, f"Status code is not 401: {response.status_code}. Response: {response.json()}"
