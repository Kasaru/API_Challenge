import json
import pytest
import requests
import endpoints
from utils.data_generation import DataGeneration

base_url = 'https://apichallenges.herokuapp.com'


class TestApiChallengePositive():

    @pytest.mark.get_challenges_list
    def test_get_challenges(self, header):
        print('Issue a GET request on the `/challenges` end point')
        url = base_url + endpoints.challenges
        response = requests.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers[
                   'Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert response.json()['challenges'][1]['status'] == True, f'Status is not True: {response.json()["challenges"][1]["status"]}'

        print(json.dumps(response.json()['challenges'][1], indent=4, ensure_ascii=False))

    @pytest.mark.get_todos_list
    def test_get_todos(self,header):
        print('Issue a GET request on the `/todos` end point')
        url = base_url + endpoints.todos
        response = requests.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers[
                   'Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert len(response.json()['todos']) == 10, f'Response lenght is incorrect {len(response.json()['todos'])}'

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        print('Issue a GET request on the `/todos/{id}` end point to return a specific todo')
        url = base_url + endpoints.todo_id
        response = requests.get(url, headers=header)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))


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
        'title': f'{random_title}',
        'doneStatus': True,
        'description': f'{random_description}'
        }
        response = requests.post(url,headers=header,json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body['title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body['doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body['description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"


    @pytest.mark.get_todos_with_done_status
    def test_get_todos_with_done_status(self, header):
        print('Issue a GET request on the `/todos` end point with a query filter to get only todos which are '
              '"done". There must exist both "done" and "not done" todos, to pass this challenge.')
        url = base_url + endpoints.todos + endpoints.done_status
        response = requests.get(url, headers=header)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'

    @pytest.mark.head_todos
    def test_head_todos(self,header):
        print('Issue a HEAD request on the `/todos` end point')

        url = base_url + endpoints.todos

        response = requests.head(url,headers=header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'

    @pytest.mark.title_length_50
    def test_title_length_50(self,header):
        print('Issue a POST request to successfully create a todo with title length = 50')

        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_long_text(50)
        random_description = DataGeneration.generate_description()

        body = {
            'title': f'{random_title}',
            'doneStatus': True,
            'description': f'{random_description}'
        }
        response = requests.post(url, headers=header, json=body)

        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == body[
            'title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body[
            'doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body[
            'description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"
