import allure
import pytest
import endpoints
from utils.checking import Checking
from utils.data_generation import DataGeneration
from utils.methods import BeautifyMethods, HttpMethods

base_url = 'https://apichallenges.herokuapp.com'

allure.epic('Negative Tests')
class TestApiChallengeNegative():
    @pytest.mark.get_todo_not_plural
    def test_get_todo(self, header):
        with allure.step('Issue a GET request on the `/todo` end point should 404 because nouns should be plural'):
            url = base_url + endpoints.invalid_todo_endpoint
            response = HttpMethods.get(url, header)
            Checking.check_status_code_json(response, 404)

    @pytest.mark.get_todo_by_id
    def test_get_todo_by_id(self, header):
        with allure.step('Issue a GET request on the `/todos/{id}` end point for a todo that does not exist'):
            url = base_url + endpoints.invalid_todo_id
            response = HttpMethods.get(url, header)
            Checking.check_status_code_json(response, 404)

    @pytest.mark.post_todo_with_string_done_status
    def test_post_todo_with_string_done_status(self,header):
        with allure.step('Issue a POST request to create a todo but fail validation on the `doneStatus` field'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_invalid_str_full_todo_body_json(10,5,10)
            response = HttpMethods.post_json(url,header,body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: doneStatus should be BOOLEAN but was STRING')

    @pytest.mark.post_todo_with_int_done_status
    def test_post_todo_with_int_done_status(self, header):
        with allure.step('Issue a POST request to create a todo but fail validation on the `doneStatus` field'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_invalid_int_full_todo_body_json(10,10)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: doneStatus should be BOOLEAN but was NUMERIC')

    @pytest.mark.too_long_title
    def test_too_long_title(self, header):
        with allure.step('Issue a POST request to create a todo but fail length validation on the `title` field '
                         'because title exceeds more than maximum allowable characters.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(51,True,10)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: Maximum allowable length exceeded for title - maximum allowed is 50')

    @pytest.mark.too_long_title_with_space
    def test_too_long_title_with_space(self, header):
        with allure.step('Issue a POST request to create a todo but fail length validation on the `title` field '
                         'because title exceeds maximum allowable characters + space.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,10,True)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: Maximum allowable length exceeded for title - maximum allowed is 50')

    @pytest.mark.too_long_description
    def test_too_long_description(self, header):
        with allure.step('Issue a POST request to create a todo but fail length validation on the `description` '
                         'because  description exceeds more than maximum allowable characters.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,201)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: Maximum allowable length exceeded for description - maximum allowed is 200')

    @pytest.mark.too_long_description_with_space
    def test_too_long_description_with_space(self, header):
        with allure.step('Issue a POST request to create a todo but fail length validation on the `description` '
                         'because description exceeds maximum allowable characters. + space.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,200,False,True)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Failed Validation: Maximum allowable length exceeded for description - maximum allowed is 200')

    @pytest.mark.too_long_content
    def test_too_long_content(self,header):
        with allure.step('Issue a POST request to create a todo but fail payload length validation on the `description` '
                         'because whole payload exceeds maximum allowable 5000 characters.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_full_todo_body_json(50,True,5000)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 413)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Error: Request body too large, max allowed is 5000 bytes')

    @pytest.mark.unrecognised_field
    def test_unrecognised_field(self,header):
        with allure.step('Issue a POST request to create a todo but fail validation because your payload contains an unrecognised field.'):
            url = base_url + endpoints.todos
            body = DataGeneration.generate_unexpected_field_full_todo_body_json(10,True,10)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Could not find field: unrecognisedField')

    @pytest.mark.create_todo_via_put
    def test_create_todo_via_put(self, header):
        with allure.step('Issue a PUT request to unsuccessfully create a todo'):
            url = base_url + endpoints.invalid_todo_id
            body = DataGeneration.generate_full_todo_body_json(10,True,10)
            response = HttpMethods.put(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'Cannot create todo with PUT due to Auto fields id')

    @pytest.mark.update_todo_via_post
    def test_update_todo_via_post(self, header):
        with allure.step('Issue a POST request for a todo which does not exist. Expect to receive a 404 response.'):
            url = base_url + endpoints.invalid_todo_id
            body = DataGeneration.generate_full_todo_body_json(10,True,10)
            response = HttpMethods.post_json(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 404)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,f'No such todo entity instance with id == {endpoints.invalid_todo_id[endpoints.invalid_todo_id.rfind('/') + 1:]} found')

    @pytest.mark.update_todo_via_put_without_title
    def test_update_todo_via_put_without_title(self, header):
        with allure.step('Issue a PUT request to fail to update an existing todo because title is missing in payload'):
            url = base_url + endpoints.todo_id
            body = DataGeneration.generate_todo_body_without_title_json(True,10)
            response = HttpMethods.put(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,'title : field is mandatory')

    @pytest.mark.update_todo_via_put_with_wrong_id
    def test_update_todo_via_put_with_wrong_id(self, header):
        with allure.step('Issue a PUT request to fail to update an existing todo because id different in payload.'):
            url = base_url + endpoints.todo_id
            body = DataGeneration.generate_todo_body_with_random_id_json(10,True,10, True)
            response = HttpMethods.put(url, header, body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 400)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,f'Can not amend id from {endpoints.todo_id[endpoints.todo_id.rfind('/') + 1:]} to {body['id']}')

    @pytest.mark.get_todos_not_acceptable
    def test_get_todos_not_acceptable(self, header):
        with allure.step('Issue a GET request on the `/todos` end point with no `Accept` header present in the message '
                         'to receive results in default JSON format'):
            url = base_url + endpoints.todos
            response = HttpMethods.get(url, {**header, 'Accept': 'application/gzip'})
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 406)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,f'Unrecognised Accept Type')

    @pytest.mark.post_todos_not_acceptable_content_type
    def test_post_todos_not_acceptable_content_type(self, header):
        with allure.step('Issue a POST request on the `/todos` end point with an unsupported content type to generate a 415 status code'):
            url = base_url + endpoints.todo_id
            body = DataGeneration.generate_full_todo_body_json(10,True,10)
            response = HttpMethods.post_json(url, {**header, 'Content-Type': '123' },body)
            BeautifyMethods.print_pretty_json(response.json())
            Checking.check_status_code_json(response, 415)
            Checking.check_tag_in_response_json(response, 'errorMessages')
            Checking.check_error_message_json(response,f'Unsupported Content Type - 123')

    @pytest.mark.delete_heartbeat
    def test_delete_heartbeat(self, header):
        with allure.step('Issue a DELETE request on the `/heartbeat` end point and receive 405 (Method Not Allowed)'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.delete(url,header)
            Checking.check_status_code_json(response, 405)

    @pytest.mark.patch_heartbeat
    def test_patch_heartbeat(self, header):
        with allure.step('Issue a PATCH request on the `/heartbeat` end point and receive 500 (internal server error)'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.patch(url, header,{})
            Checking.check_status_code_json(response, 500)

    @pytest.mark.trace_heartbeat
    def test_trace_heartbeat(self, header):
        with allure.step('Issue a POST request on the `/heartbeat` end point and receive 501 (Not Implemented) '
                         'when override the Method Verb to a TRACE'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.trace(url, header)
            Checking.check_status_code_json(response, 501)

    @pytest.mark.override_delete_heartbeat
    def test_override_delete_heartbeat(self, header):
        with allure.step('Issue a POST request on the `/heartbeat` end point and receive 405 when override the Method Verb to a DELETE'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Delete'},{})
            Checking.check_status_code_json(response, 405)

    @pytest.mark.override_patch_heartbeat
    def test_override_patch_heartbeat(self, header):
        with allure.step('Issue a POST request on the `/heartbeat` end point and receive 500 when override the Method Verb to a PATCH'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Patch'},{})
            Checking.check_status_code_json(response, 500)

    @pytest.mark.override_trace_heartbeat
    def test_override_trace_heartbeat(self, header):
        with allure.step('Issue a POST request on the `/heartbeat` end point and receive 501 (Not Implemented) '
                         'when override the Method Verb to a TRACE'):
            url = base_url + endpoints.heartbeat
            response = HttpMethods.post_json(url, {**header,'X-HTTP-Method-Override':'Trace'},{})
            Checking.check_status_code_json(response, 501)

    @pytest.mark.post_secret_token_incorrect_uname
    def test_post_secret_token_incorrect_uname(self,header):
        with allure.step('Issue a POST request on the `/secret/token` end point and receive 401 when Basic auth username/password '
                         'is not admin/password'):
            url = base_url + endpoints.secret_token
            response = HttpMethods.post_json_basic(url,header,{},'amin', 'password')
            Checking.check_status_code_json(response, 401)

    @pytest.mark.get_secret_note_invalid_x_auth
    def test_get_secret_note_invalid_x_auth(self, header):
        with allure.step('Issue a GET request on the `/secret/note` end point and receive 403 when X-AUTH-TOKEN does not match a valid token'):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'test': 'test'}, 'admin', 'password')
            url = base_url + endpoints.secret_note
            response = HttpMethods.get(url, {**header, 'X-AUTH-TOKEN': pre_response.headers['X-AUTH-TOKEN'][:-6]+'kasaru'})
            Checking.check_status_code_json(response, 403)

    @pytest.mark.get_secret_note_without_x_auth
    def test_get_secret_note_without_x_auth(self, header):
        with allure.step('Issue a GET request on the `/secret/note` end point and receive 401 when no X-AUTH-TOKEN header present'):
            url = base_url + endpoints.secret_note
            response = HttpMethods.get(url, header)
            Checking.check_status_code_json(response, 401)

    @pytest.mark.post_secret_note_invalid_x_auth
    def test_post_secret_note_invalid_x_auth(self, header):
        with allure.step('Issue a POST request on the `/secret/note` end point with a note payload {"note":"my note"} and receive 403 '
                         'when X-AUTH-TOKEN does not match a valid token'):
            url = base_url + endpoints.secret_token
            pre_response = HttpMethods.post_json_basic(url, header, {'test': 'test'}, 'admin', 'password')
            body = {"note":"my note"}
            url = base_url + endpoints.secret_note
            response = HttpMethods.post_json(url,{**header, 'X-AUTH-TOKEN': pre_response.headers['X-AUTH-TOKEN'][:-6] + 'kasaru'},body)
            Checking.check_status_code_json(response, 403)

    @pytest.mark.post_secret_note_without_x_auth
    def test_post_secret_note_without_x_auth(self, header):
        with allure.step('Issue a POST request on the `/secret/note` end point with a note payload {"note":"my note"} '
                         'and receive 401 when no X-AUTH-TOKEN present'):
            url = base_url + endpoints.secret_note
            body = DataGeneration.generate_note_body()
            response = HttpMethods.post_json(url, header,body)
            Checking.check_status_code_json(response, 401)