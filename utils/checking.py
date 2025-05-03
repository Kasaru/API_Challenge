import xml.etree.ElementTree as ET

from utils.methods import BeautifyMethods, ResponseMethods


class Checking:
    @staticmethod
    def assert_response_xml(response, tag, body):
        try:
            # Парсим XML-ответ
            response_root = ET.fromstring(response.text)
            # Парсим body как XML
            body_root = ET.fromstring(body)
            # Ищем указанный тег в обоих XML
            response_element = response_root.find(tag)
            body_element = body_root.find(tag)
            if body_element.text == 'True':
                body_element.text = 'true'
            assert response_element.text == body_element.text, (
                f"""
                Value mismatch for tag '{tag}': response value '{response_element.text}'
                doesn't match body value '{body_element.text}'
                """
            )
        except ET.ParseError:
            assert False, "Failed to parse one of the XML inputs"

    @staticmethod
    def check_status_code_xml(response,status_code):
        assert response.status_code == status_code, f"Status code is not {status_code}: {response.status_code}. Response: {response.text}"

    @staticmethod
    def check_status_code_json(response,status_code):
        assert response.status_code == status_code, f"Status code is not {status_code}: {response.status_code}. Response: {response.json()}"

    @staticmethod
    def check_tag_in_response_json(response, tag):
        assert tag in response.json(), f'Missing {tag} in response, {BeautifyMethods.print_pretty_json(response.json())}'

    @staticmethod
    def check_error_message_json(response,expected_message):
        assert response.json()['errorMessages'][0] == expected_message, ('Incorrect error'f'message: {response.json()['errorMessages'][0]}')

    @staticmethod
    def check_body_field_json(response, body, tag):
        assert response.json()[tag] == body[tag], f"Unexpected {tag}: {response.json()[tag]}. Expected: {body[tag]}"

    @staticmethod
    def check_json_field_with_xml_body(response, body, tag):
        assert response.json()[tag] == ResponseMethods.get_value_from_xml_by_tag(body,tag), f"Unexpected {tag}: {response.json()[tag]}. Expected: {ResponseMethods.get_value_from_xml_by_tag(body,tag)}"

    @staticmethod
    def check_xml_field_with_json_body(response, body, tag):
        assert ResponseMethods.get_value_from_xml_by_tag(response.text, tag) == body[tag], f"Unexpected {tag}: {ResponseMethods.get_value_from_xml_by_tag(response.text, tag)}. Expected: {body[tag]}"

    @staticmethod
    def check_response_header(response,header_name,header_value):
        assert response.headers[header_name] == header_value, f'Incorrect {header_name}: {response.headers[header_name]}'

    @staticmethod
    def check_tag_list_length(response,tag,length):
        assert len(response.json()[tag]) == length, f'Incorrect {tag} list length'

    @staticmethod
    def check_todo_id(response,url):
        assert response.json()['todos'][0]['id'] == int(url[url.rfind('/') + 1:]), f'Todo id is incorrect {response.json()['todos'][0]['id']}'

    @staticmethod
    def check_challenge_status(response):
        assert response.json()['challenges'][1]['status'] == True, f'Status is not True: {response.json()["challenges"][1]["status"]}'

    @staticmethod
    def check_responses_equal_json(first_response,second_response):
        assert second_response.json() == first_response.json(), 'Second response is not equal to the original response'

    @staticmethod
    def check_tag_value_json(response, tag, tag_value):
        assert response.json()[tag] == tag_value, f"Unexpected {tag}: {response.json()[tag]}. Expected: {tag_value}"
