import json
import pytest
import requests
import endpoints
from utils.data_generation import DataGeneration
from utils.methods import BeautifyMethods, HttpMethods

base_url = 'https://apichallenges.herokuapp.com'


class TestApiChallengePositive():

    @pytest.mark.get_challenges_list
    def test_get_challenges(self, header):
        print('Issue a GET request on the `/challenges` end point')
        url = base_url + endpoints.challenges
        response = HttpMethods.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers[
                   'Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert response.json()['challenges'][1]['status'] == True, f'Status is not True: {response.json()["challenges"][1]["status"]}'

        print(json.dumps(response.json()['challenges'][1], indent=4, ensure_ascii=False))

    @pytest.mark.get_todos_list
    def test_get_todos(self,header):
        print('Issue a GET request on the `/todos` end point')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers[
                   'Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert len(response.json()['todos']) == 10, f'Response lenght is incorrect {len(response.json()['todos'])}'

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        print('Issue a GET request on the `/todos/{id}` end point to return a specific todo')
        url = base_url + endpoints.todo_id
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers[
                   'Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert response.json()['todos'][0]['id'] == int(url[url.rfind('/')+1:]), f'Todo id is incorrect {response.json()['todos'][0]['id']}'


    @pytest.mark.post_todo_with_done_status_true
    def test_post_todo_with_done_status_true(self,header):
        print('Issue a POST request to successfully create a todo')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
        'title': random_title,
        'doneStatus': True,
        'description': random_description
        }
        response = HttpMethods.post(url,header,body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body['title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body['doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body['description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"


    @pytest.mark.get_todos_with_done_status
    def test_get_todos_with_done_status(self, header):
        print('Issue a GET request on the `/todos` end point with a query filter to get only todos which are '
              '"done". There must exist both "done" and "not done" todos, to pass this challenge.')
        url = base_url + endpoints.todos + endpoints.done_status
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'

    @pytest.mark.head_todos
    def test_head_todos(self,header):
        print('Issue a HEAD request on the `/todos` end point')
        url = base_url + endpoints.todos
        response = HttpMethods.head(url,header)
        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'

    @pytest.mark.title_length_50
    def test_title_length_50(self,header):
        print('Issue a POST request to successfully create a todo with title length = 50')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_long_text(50)
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.description_length_200
    def test_description_length_200(self, header):
        print('Issue a POST request to successfully create a todo with title length = 50')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_long_text(200)
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.max_description_and_title_length
    def test_max_description_and_title_length(self, header):
        print('Issue a POST request to create a todo with maximum length title and description fields.')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_long_text(50)
        random_description = DataGeneration.generate_long_text(200)
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.update_todo_via_put
    def test_update_todo_via_put(self,header):
        print('Issue a PUT request to update an existing todo with a complete payload i.e. title, description and donestatus.')
        url = base_url + endpoints.todo_id
        random_title = DataGeneration.generate_long_text(50)
        random_description = DataGeneration.generate_long_text(200)
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.put(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.update_todo_via_post
    def test_update_todo_via_post(self, header):
        print('Issue a POST request to successfully update a todo')
        url = base_url + endpoints.todo_id
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        get_response = HttpMethods.get(url, header)
        assert get_response.status_code == 200, f"Status code is not 200: {get_response.status_code}. Response: {get_response.json()}"
        BeautifyMethods.print_pretty_json(get_response.json())

        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post(url, header, body)
        print('Changed todo: \n',json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.partial_update_todo_via_put
    def test_partial_update_todo_via_put(self, header):
        print('Issue a PUT request to update an existing todo with just mandatory items in payload i.e. title.')
        url = base_url + endpoints.todo_id
        random_title = DataGeneration.generate_long_text(50)

        body = {
            'title': random_title
        }

        response = HttpMethods.put(url, header, body)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == False, f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: False"
        assert response.json()['description'] == '', f"Unexpected description: {response.json()['description']}. Expected: ''"

    @pytest.mark.delete_todo
    def test_delete_todo(self,header):
        print('Issue a DELETE request to successfully delete a todo')
        url = base_url + endpoints.todo_id
        get_response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(get_response.json())
        response = HttpMethods.delete(url, header)
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        check_response = HttpMethods.get(url, header)
        assert check_response.status_code == 404, f"Status code is not 404: {check_response.status_code}. Response: {check_response.json()}"


    @pytest.mark.get_options
    def test_get_options(self,header):
        print('Issue an OPTIONS request on the `/todos` end point. You might want to manually check the "Allow" header in the response is as expected.')
        url = base_url + endpoints.todos
        response = HttpMethods.options(url,header)
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert response.headers['Access-Control-Allow-Methods'] == '*', f'Incorrect allowed methods: {response.headers['Access-Control-Allow-Methods']}'


    @pytest.mark.get_todos_xml
    def test_get_todos_xml(self, header):
        print('Issue a GET request on the `/todos` end point with an `Accept` header of `application/xml` to receive results in XML format')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, {**header, 'Accept': 'application/xml'})
        BeautifyMethods.print_pretty_xml(response.text)
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert response.headers['Content-Type'] == 'application/xml', f'Content-Type is not application/xml: {response.headers["Content-Type"]}'


    @pytest.mark.get_todos_json
    def test_get_todos_json(self, header):
        print('Issue a GET request on the `/todos` end point with an `Accept` header of `application/json` to receive results in JSON format')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, {**header, 'Accept': 'application/json'})
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"

    @pytest.mark.get_todos_pref
    def test_get_todos_pref(self, header):
        print('Issue a GET request on the `/todos` end point with an `Accept` header of `application/xml, application/json` to receive results in the preferred XML format')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, {**header, 'Accept': 'application/xml, application/json'})
        BeautifyMethods.print_pretty_xml(response.text)
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"

