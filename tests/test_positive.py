import json
import pytest
import endpoints
from endpoints import heartbeat
from utils.assertions import assert_response_xml
from utils.data_generation import DataGeneration
from utils.methods import HttpMethods, BeautifyMethods, ResponseMethods

base_url = 'https://apichallenges.herokuapp.com'


class TestApiChallengePositive():

    @pytest.mark.get_challenges_list
    def test_get_challenges(self, header):
        print('Issue a GET request on the `/challenges` end point')
        url = base_url + endpoints.challenges
        response = HttpMethods.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers['Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert response.json()['challenges'][1]['status'] == True, f'Status is not True: {response.json()["challenges"][1]["status"]}'

        print(json.dumps(response.json()['challenges'][1], indent=4, ensure_ascii=False))

    @pytest.mark.get_todos_list
    def test_get_todos(self,header):
        print('Issue a GET request on the `/todos` end point')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, headers = header)

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers['Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
        assert len(response.json()['todos']) == 10, f'Response lenght is incorrect {len(response.json()['todos'])}'

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        print('Issue a GET request on the `/todos/{id}` end point to return a specific todo')
        url = base_url + endpoints.todo_id
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())

        assert response.status_code == 200, f'Status code is not 200: {response.status_code}'
        assert response.headers['Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers["Content-Type"]}'
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
        response = HttpMethods.post_json(url,header,body)
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
        response = HttpMethods.post_json(url, header, body)
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
        response = HttpMethods.post_json(url, header, body)
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
        response = HttpMethods.post_json(url, header, body)
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
        response = HttpMethods.post_json(url, header, body)
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

    @pytest.mark.get_todos_with_blank_accept
    def test_get_todos_with_blank_accept(self, header):
        print('Issue a GET request on the `/todos` end point with no `Accept` header present in the message to receive results in default JSON format')
        url = base_url + endpoints.todos
        response = HttpMethods.get(url, {**header, 'Accept': ''})
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"

    @pytest.mark.post_todo_via_xml
    def test_post_todo_via_xml(self,header):
        print('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/xml`, and Accepting only XML ie. Accept header of `application/xml`')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body =f'''
        <todo>
            <title>{random_title}</title>
            <doneStatus>true</doneStatus>
            <description>{random_description}</description>
        </todo>
        '''
        response = HttpMethods.post_xml(url, {**header,'Accept' : 'application/xml', 'Content-Type' : 'application/xml'},body)
        BeautifyMethods.print_pretty_xml(response.text)
        assert response.status_code == 201, f"Status code is not 201: {response.status_code}. Response: {response.text}"
        assert response.headers['Content-Type'] == 'application/xml', f'Content-Type is not application/xml: {response.headers["Content-Type"]}'
        assert_response_xml(response,'title',body)
        assert_response_xml(response, 'doneStatus', body)
        assert_response_xml(response, 'description', body)

    @pytest.mark.post_todo_via_json
    def test_post_todo_via_json(self, header):
        print('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/json`, and Accepting only JSON ie. Accept header of `application/json`')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post_json(url, {**header, 'Accept': 'application/json', 'Content-Type': 'application/json'},body)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 201, f"Status code is not 201: {response.status_code}. Response: {response.text}"
        assert response.headers['Content-Type'] == 'application/json', f'Content-Type is not application/json: {response.headers['Content-Type']}'
        assert response.json()['title'] == body['title'], f"Unexpected title: {response.json()['title']}. Expected: {body['title']}"
        assert response.json()['doneStatus'] == body['doneStatus'], f"Unexpected doneStatus: {response.json()['doneStatus']}. Expected: {body['doneStatus']}"
        assert response.json()['description'] == body['description'], f"Unexpected description: {response.json()['description']}. Expected: {body['description']}"

    @pytest.mark.get_progress
    def test_get_progress(self, header):
        print('Issue a GET request on the `/challenger/{guid}` end point, with an existing challenger GUID. This will return the progress data payload that can be used to later restore your progress to this status.')
        url = base_url + endpoints.challenger + header['X-Challenger']
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert len(response.json()['challengeStatus']) == 59, 'Incorrect list length'

    @pytest.mark.put_restorable_challenger_progress_status
    def test_put_restorable_challenger_progress_status(self, header):
        print('Issue a PUT request on the `/challenger/{guid}` end point, with an existing challenger GUID to restore that challengers progress into memory.')
        url = base_url + endpoints.challenger + header['X-Challenger']
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert len(response.json()['challengeStatus']) == 59, 'Incorrect list length'
        response = HttpMethods.put(url, header,response.json())
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        assert len(response.json()['challengeStatus']) == 59, 'Incorrect list length'

    @pytest.mark.get_challenger_database
    def test_get_challenger_database(self, header):
        print('Issue a GET request on the `/challenger/database/{guid}` end point, to retrieve the current todos database for the user. You can use this to restore state later.')
        url = base_url + endpoints.challenger_database + header['X-Challenger']
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"

    @pytest.mark.xfail
    @pytest.mark.put_challenger_database
    def test_put_challenger_database(self, header):
        print('Issue a PUT request on the `/challenger/database/{guid}` end point, with a payload to restore the Todos database in memory.')
        url = base_url + endpoints.challenger_database + header['X-Challenger']
        response = HttpMethods.get(url, header)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 200, f"Status code is not 200: {response.status_code}. Response: {response.json()}"
        put_response = HttpMethods.put(url, header,response.json())
        assert put_response.status_code == 204, f"Status code is not 204: {put_response.status_code}. Response"
        assert put_response.json() == response.json(), 'PUT response is not equal to the original response'

    @pytest.mark.post_xml_to_json
    def test_post_xml_to_json(self,header):
        print('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/xml` but Accept `application/json`')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = f'''
        <todo>
            <title>{random_title}</title>
            <doneStatus>true</doneStatus>
            <description>{random_description}</description>
        </todo>
        '''
        response = HttpMethods.post_xml(url,{**header,'Content-Type':'application/xml','Accept':'application/json'},body)
        BeautifyMethods.print_pretty_json(response.json())
        assert response.status_code == 201, f"Status code is not 201: {response.status_code}. Response: {response.json()}"
        assert response.json()['title'] == ResponseMethods.get_value_from_xml_by_tag(body,'title'), f"Unexpected title: {response.json()['title']}. Expected: {ResponseMethods.get_value_from_xml_by_tag(body,'title')}"
        assert response.json()['doneStatus'] == ResponseMethods.get_value_from_xml_by_tag(body,'doneStatus'), f"Unexpected title: {response.json()['doneStatus']}. Expected: {ResponseMethods.get_value_from_xml_by_tag(body, 'doneStatus')}"
        assert response.json()['description'] == ResponseMethods.get_value_from_xml_by_tag(body,'description'), f"Unexpected title: {response.json()['description']}. Expected: {ResponseMethods.get_value_from_xml_by_tag(body, 'description')}"

    @pytest.mark.post_json_to_xml
    def test_post_json_to_xml(self,header):
        print('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/json` but Accept `application/xml`')
        url = base_url + endpoints.todos
        random_title = DataGeneration.generate_name()
        random_description = DataGeneration.generate_description()
        body = {
            'title': random_title,
            'doneStatus': True,
            'description': random_description
        }
        response = HttpMethods.post_json(url,{**header,'Content-Type':'application/json','Accept':'application/xml'},body)
        BeautifyMethods.print_pretty_xml(response.text)
        assert response.status_code == 201, f"Status code is not 201: {response.status_code}. Response: {response.text}"
        assert ResponseMethods.get_value_from_xml_by_tag(response.text,'title') == body['title'], f"Unexpected title: {ResponseMethods.get_value_from_xml_by_tag(response.text, 'title')}. Expected: {body['title']}"
        assert ResponseMethods.get_value_from_xml_by_tag(response.text, 'doneStatus') == body['doneStatus'], f"Unexpected title: {ResponseMethods.get_value_from_xml_by_tag(response.text, 'doneStatus')}. Expected: {body['doneStatus']}"
        assert ResponseMethods.get_value_from_xml_by_tag(response.text, 'description') == body['description'], f"Unexpected title: {ResponseMethods.get_value_from_xml_by_tag(response.text, 'description')}. Expected: {body['description']}"
        print(header)

    @pytest.mark.get_heartbeat
    def test_get_heartbeat(self,header):
        print('Issue a GET request on the `/heartbeat` end point and receive 204 when server is running')
        url = base_url + endpoints.heartbeat
        response = HttpMethods.get(url,header)
        assert response.status_code == 204, f"Status code is not 204: {response.status_code}. Response: {response.text}"

    @pytest.mark.post_secret_token
    def test_post_secret_token(self,header):
        print('Issue a POST request on the `/secret/token` end point and receive 201 when Basic auth username/password is admin/password')
        url = base_url + endpoints.secret_token
        response = HttpMethods.post_json_basic(url,header,{'test':'test'},'admin', 'password')
        assert response.status_code == 201, f"Status code is not 201: {response.status_code}. Response: {response.json()}"