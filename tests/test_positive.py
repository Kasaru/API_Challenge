import json

import allure
import pytest
import endpoints
from utils.checking import Checking
from utils.data_generation import DataGeneration
from utils.methods import HttpMethods, BeautifyMethods

base_url = 'https://apichallenges.herokuapp.com'

allure.epic('Positive tests')
class TestApiChallengePositive:

    @pytest.mark.get_challenges_list
    def test_get_challenges(self, header):
        with allure.step('Issue a GET request on the `/challenges` end point'):
            url = base_url + endpoints.challenges
            response = HttpMethods.get(url, headers = header)
            Checking.check_status_code_json(response,200)
            Checking.check_response_header(response,'Content-Type','application/json')
            Checking.check_challenge_status(response)
            BeautifyMethods.print_pretty_json(response.json())

    @pytest.mark.get_todos_list
    def test_get_todos(self,header):
        with allure.step('Issue a GET request on the `/todos` end point'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url,header)
            Checking.check_status_code_json(response, 200)
            Checking.check_response_header(response,'Content-Type','application/json')
            Checking.check_tag_list_length(response,'todos',10)

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        with allure.step('Issue a GET request on the `/todos/{id}` end point to return a specific todo'):
            url = base_url + endpoints.todo_id
            response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)
            Checking.check_response_header(response,'Content-Type','application/json')
            Checking.check_todo_id(response, url)


    @pytest.mark.post_todo_with_done_status_true
    def test_post_todo_with_done_status_true(self,header):
        with allure.step('Issue a POST request to successfully create a todo'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(10,True,10,False)
            response = HttpMethods.post_json(url,header,body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 201)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')


    @pytest.mark.get_todos_with_done_status
    def test_get_todos_with_done_status(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with a query filter to get only todos which are '
              '"done". There must exist both "done" and "not done" todos, to pass this challenge.'):
            url = base_url + endpoints.todos + endpoints.done_status
            response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)

    @pytest.mark.head_todos
    def test_head_todos(self,header):
        with allure.step('Issue a HEAD request on the `/todos` end point'):
            url = base_url + endpoints.todos
            response = HttpMethods.head(url,header)
            Checking.check_status_code_json(response,200)

    @pytest.mark.title_length_50
    def test_title_length_50(self,header):
        with allure.step('Issue a POST request to successfully create a todo with title length = 50'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,10)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,201)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.description_length_200
    def test_description_length_200(self, header):
        with allure.step('Issue a POST request to successfully create a todo with title length = 50'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(10,True,200)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 201)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.max_description_and_title_length
    def test_max_description_and_title_length(self, header):
        with allure.step('Issue a POST request to create a todo with maximum length title and description fields.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,200)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 201)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.update_todo_via_put
    def test_update_todo_via_put(self,header):
        with allure.step('Issue a PUT request to update an existing todo with a complete payload i.e. title, description and donestatus.'):
            url = base_url + endpoints.todo_id
            body = DataGeneration.generate_full_todo_body_json(50,True,200)
            response = HttpMethods.put(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 200)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.update_todo_via_post
    def test_update_todo_via_post(self, header):
        with allure.step('Issue a POST request to successfully update a todo'):
            url = base_url + endpoints.todo_id
            get_response = HttpMethods.get(url, header)
            Checking.check_status_code_json(get_response,200)
            BeautifyMethods.print_pretty_json(get_response.json())
            body = DataGeneration.generate_full_todo_body_json(10, True, 10)
            response = HttpMethods.post_json(url, header, body)
            print('Changed todo: \n',json.dumps(response.json(), indent=4, ensure_ascii=False))
            Checking.check_status_code_json(response, 200)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.partial_update_todo_via_put
    def test_partial_update_todo_via_put(self, header):
        with allure.step('Issue a PUT request to update an existing todo with just mandatory items in payload i.e. title.'):
            url = base_url + endpoints.todo_id
            body = DataGeneration.generate_one_field_todo_body_json('title',5)
            response = HttpMethods.put(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)
            Checking.check_body_field_json(response,body,'title')
            Checking.check_tag_value_json(response,'doneStatus',False)
            Checking.check_tag_value_json(response, 'description', '')

    @pytest.mark.delete_todo
    def test_delete_todo(self,header):
        with allure.step('Issue a DELETE request to successfully delete a todo'):
            url = base_url + endpoints.todo_id
            get_response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(get_response.json())
            response = HttpMethods.delete(url, header)
            Checking.check_status_code_json(response,200)
            check_response = HttpMethods.get(url, header)
            Checking.check_status_code_json(check_response,404)


    @pytest.mark.get_options
    def test_get_options(self,header):
        with allure.step('Issue an OPTIONS request on the `/todos` end point.'):
            url = base_url + endpoints.todos
            response = HttpMethods.options(url,header)
            Checking.check_status_code_json(response,200)
            Checking.check_response_header(response,'Access-Control-Allow-Methods','*')


    @pytest.mark.get_todos_xml
    def test_get_todos_xml(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with an `Accept` header of `application/xml` to receive results in XML format'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, {**header, 'Accept': 'application/xml'})
            BeautifyMethods.print_pretty_xml(response.text)
            Checking.check_status_code_json(response,200)
            Checking.check_response_header(response,'Content-Type','application/xml')

    @pytest.mark.get_todos_json
    def test_get_todos_json(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with an `Accept` header of `application/json` to receive results in JSON format'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, {**header, 'Accept': 'application/json'})
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)

    @pytest.mark.get_todos_pref
    def test_get_todos_pref(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with an '
                         '`Accept` header of `application/xml, application/json` to receive results in the preferred XML format'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, {**header, 'Accept': 'application/xml, application/json'})
            BeautifyMethods.print_pretty_xml(response.text)
            Checking.check_status_code_json(response,200)

    @pytest.mark.get_todos_with_blank_accept
    def test_get_todos_with_blank_accept(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with no '
                         '`Accept` header present in the message to receive results in default JSON format'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, {**header, 'Accept': ''})
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)

    @pytest.mark.post_todo_via_xml
    def test_post_todo_via_xml(self,header):
        with allure.step('Issue a POST request on the `/todos` end point to create a todo using '
                         'Content-Type `application/xml`, and Accepting only XML ie. Accept header of `application/xml`'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_xml(10, True, 10)
            response = HttpMethods.post_xml(url, {**header,'Accept' : 'application/xml', 'Content-Type' : 'application/xml'},body)
            BeautifyMethods.print_pretty_xml(response.text)
            Checking.check_status_code_xml(response,201)
            Checking.check_response_header(response, 'Content-Type', 'application/xml')
            Checking.assert_response_xml(response,'title',body)
            Checking.assert_response_xml(response, 'doneStatus', body)
            Checking.assert_response_xml(response, 'description', body)

    @pytest.mark.post_todo_via_json
    def test_post_todo_via_json(self, header):
        with allure.step('Issue a POST request on the `/todos` end point to create a todo using '
                         'Content-Type `application/json`, and Accepting only JSON ie. Accept header of `application/json`'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(10, True, 10)
            response = HttpMethods.post_json(url, {**header, 'Accept': 'application/json', 'Content-Type': 'application/json'},body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,201)
            Checking.check_response_header(response, 'Content-Type', 'application/json')
            Checking.check_body_field_json(response,body,'title')
            Checking.check_body_field_json(response,body,'doneStatus')
            Checking.check_body_field_json(response,body,'description')

    @pytest.mark.get_progress
    def test_get_progress(self, header):
        with allure.step('Issue a GET request on the `/challenger/{guid}` end point, with an existing challenger GUID. '
                         'This will return the progress data payload that can be used to later restore your progress to this status.'):
            url = base_url + endpoints.challenger + header['X-Challenger']
            response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)
            Checking.check_tag_list_length(response,'challengeStatus',59)

    @pytest.mark.put_restorable_challenger_progress_status
    def test_put_restorable_challenger_progress_status(self, header):
        with allure.step('Issue a PUT request on the `/challenger/{guid}` end point, with an existing challenger GUID '
                         'to restore that challengers progress into memory.'):
            url = base_url + endpoints.challenger + header['X-Challenger']
            response_get = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(response_get.json())
            Checking.check_status_code_json(response_get,200)
            Checking.check_tag_list_length(response_get,'challengeStatus',59)
            response_put = HttpMethods.put(url, header,response_get.json())
            BeautifyMethods.print_pretty_json(response_put.json())
            Checking.check_status_code_json(response_put,200)
            Checking.check_tag_list_length(response_put,'challengeStatus',59)

    @pytest.mark.get_challenger_database
    def test_get_challenger_database(self, header):
        with allure.step('Issue a GET request on the `/challenger/database/{guid}` end point, '
                         'to retrieve the current todos database for the user. can use this to restore state later.'):
            url = base_url + endpoints.challenger_database + header['X-Challenger']
            response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)

    @pytest.mark.xfail
    @pytest.mark.put_challenger_database
    def test_put_challenger_database(self, header):
        with allure.step('Issue a PUT request on the `/challenger/database/{guid}` end point, with a payload to restore the Todos database in memory.'):
            url = base_url + endpoints.challenger_database + header['X-Challenger']
            get_response = HttpMethods.get(url, header)
            BeautifyMethods.print_pretty_json(get_response.json())
            Checking.check_status_code_json(get_response,200)
            put_response = HttpMethods.put(url, header,get_response.json())
            Checking.check_status_code_json(put_response,204)
            Checking.check_responses_equal_json(get_response,put_response)


    @pytest.mark.post_xml_to_json
    def test_post_xml_to_json(self,header):
        with allure.step('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/xml` '
                         'but Accept `application/json`'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_xml(10, True, 10)
            response = HttpMethods.post_xml(url,{**header,'Content-Type':'application/xml','Accept':'application/json'},body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,201)
            Checking.check_json_field_with_xml_body(response,body,'title')
            Checking.check_json_field_with_xml_body(response, body, 'doneStatus')
            Checking.check_json_field_with_xml_body(response, body, 'description')

    @pytest.mark.post_json_to_xml
    def test_post_json_to_xml(self,header):
        with allure.step('Issue a POST request on the `/todos` end point to create a todo using Content-Type `application/json` '
                         'but Accept `application/xml`'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(10, True, 10)
            response = HttpMethods.post_json(url,{**header,'Content-Type':'application/json','Accept':'application/xml'},body)
            BeautifyMethods.print_pretty_xml(response.text)
            Checking.check_status_code_xml(response,201)
            Checking.check_xml_field_with_json_body(response,body,'title')
            Checking.check_xml_field_with_json_body(response, body, 'doneStatus')
            Checking.check_xml_field_with_json_body(response, body, 'description')

    @pytest.mark.get_heartbeat
    def test_get_heartbeat(self,header):
        with allure.step('Issue a GET request on the `/heartbeat` end point and receive 204 when server is running'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.get(url,header)
            Checking.check_status_code_xml(response,204)

    @pytest.mark.post_secret_token
    def test_post_secret_token(self,header):
        with allure.step('Issue a POST request on the `/secret/token` end point and receive 201 when Basic auth username/password is admin/password'):
            url = base_url + endpoints.secret_token
            response = HttpMethods.post_json_basic(url,header,{'test':'test'},'admin', 'password')
            Checking.check_status_code_json(response,201)

    @pytest.mark.get_secret_note
    def test_get_secret_note(self, header):
        with allure.step('Issue a GET request on the `/secret/note` end point receive 200 when valid X-AUTH-TOKEN used '
                         '- response body should contain the note'):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'test': 'test'},'admin', 'password')
            url = base_url + endpoints.secret_note
            response = HttpMethods.get(url, {**header, 'X-AUTH-TOKEN': pre_response.headers['X-AUTH-TOKEN']})
            Checking.check_status_code_json(response,200)

    @pytest.mark.post_secret_note
    def test_post_secret_note(self, header):
        with allure.step('Issue a POST request on the `/secret/note` end point with a note payload e.g. {"note":"my note"} '
                         'and receive 200 when valid X-AUTH-TOKEN used. Note is maximum length 100 chars and will be truncated when stored.'):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'test': 'test'}, 'admin', 'password')
            body = DataGeneration.generate_note_body()
            url = base_url + endpoints.secret_note
            response = HttpMethods.post_json(url, {**header, 'X-AUTH-TOKEN': pre_response.headers['X-AUTH-TOKEN']},body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)
            Checking.check_tag_in_response_json(response,'note')

    @pytest.mark.get_secret_note_bearer
    def test_get_secret_note_bearer(self, header):
        with allure.step('Issue a GET request on the `/secret/note` end point receive 200 when using the X-AUTH-TOKEN value as an '
                         'Authorization Bearer token - response body should contain the note'):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'note': 'test'},'admin', 'password')
            url = base_url + endpoints.secret_note
            response = HttpMethods.get(url, {**header, 'Authorization': f'Bearer {pre_response.headers['X-AUTH-TOKEN']}'})
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)

    @pytest.mark.post_secret_note_bearer
    def test_post_secret_note_bearer(self, header):
        with allure.step('Issue a POST request on the `/secret/note` end point with a note payload e.g. {"note":"my note"} and receive 200 when valid '
                         'X-AUTH-TOKEN value used as an Authorization Bearer token. Status code 200 received. '):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'note': 'test'}, 'admin', 'password')
            url = base_url + endpoints.secret_note
            body = DataGeneration.generate_note_body()
            response = HttpMethods.post_json(url, {**header, 'Authorization': f'Bearer {pre_response.headers['X-AUTH-TOKEN']}'},body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response,200)


    @pytest.mark.delete_all_todos
    def test_delete_all_todos(self,header):
        with allure.step('Issue a DELETE request to successfully delete the last todo in system so that there are no more todos in the system'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, header)
            response_data = response.json()
            ids = [todo['id'] for todo in response_data.get('todos', [])]
            for id in ids:
                todo_url = f'{base_url}{endpoints.todos}/{id}'
                response_del = HttpMethods.delete(todo_url, header)
                Checking.check_status_code_xml(response_del,200)
                check_response = HttpMethods.get(todo_url,header)
                Checking.check_status_code_xml(check_response,404)

    @pytest.mark.create_maximum_todos
    def test_create_maximum_todos(self,header):
        with allure.step('Issue as many POST requests as it takes to add the maximum number of TODOS allowed for a user.'):
            url = base_url + endpoints.todos
            while True:
                body = DataGeneration.generate_full_todo_body_json(10, True, 10)
                response = HttpMethods.post_json(url, header, body)
                if response.status_code == 400:
                    Checking.check_tag_in_response_json(response, 'errorMessages')
                    Checking.check_error_message_json(response,'ERROR: Cannot add instance, maximum limit of 20 reached')
                    print("Received 400 status code. Maximum todos reached.")
                    break
                BeautifyMethods.print_pretty_json(response.json())
                Checking.check_status_code_json(response,201)
                Checking.check_body_field_json(response,body,'title')
                Checking.check_body_field_json(response,body,'doneStatus')
                Checking.check_body_field_json(response,body,'description')