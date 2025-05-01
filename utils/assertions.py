import xml.etree.ElementTree as ET


def assert_response_xml(response, tag, body):
    try:
        # Парсим XML-ответ
        response_root = ET.fromstring(response.text)
        # Парсим body как XML
        body_root = ET.fromstring(body)
        # Ищем указанный тег в обоих XML
        response_element = response_root.find(tag)
        body_element = body_root.find(tag)
        assert response_element.text == body_element.text, (
            f"""
            Value mismatch for tag '{tag}': response value '{response_element.text}'
            doesn't match body value '{body_element.text}'
            """
        )
    except ET.ParseError:
        assert False, "Failed to parse one of the XML inputs"

