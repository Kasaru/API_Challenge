import json
import xml.dom.minidom
import allure
import requests
from utils.logger import Logger


class HttpMethods:

    def get(url,headers):
        with allure.step("GET"):
            Logger.add_request(url,method="GET")
            result = requests.get(url,headers=headers)
            Logger.add_response(result)
            return result

    @staticmethod
    def post(url,headers,body):
        with allure.step("POST"):
            Logger.add_request(url, method="POST")
            result = requests.post(url, headers=headers,json=body)
            Logger.add_response(result)
            return result

    @staticmethod
    def put(url,headers,body):
        with allure.step("PUT"):
            Logger.add_request(url, method="PUT")
            result = requests.put(url, headers=headers,json=body)
            Logger.add_response(result)
            return result

    @staticmethod
    def delete(url,headers):
        with allure.step("DELETE"):
            Logger.add_request(url, method="DELETE")
            result = requests.delete(url, headers=headers)
            Logger.add_response(result)
            return result
        
    def options(url, headers):
        with allure.step("OPTIONS"):
            Logger.add_request(url, method="OPTIONS")
            result = requests.options(url, headers=headers)
            Logger.add_response(result)
            return result
    
    def head(url, headers):
        with allure.step("HEAD"):
            Logger.add_request(url, method="HEAD")
            result = requests.head(url, headers=headers)
            Logger.add_response(result)
            return result

    @staticmethod
    def trace(url, headers):
        with allure.step("TRACE"):
            Logger.add_request(url, method="TRACE")
            result = requests.request('trace', url, headers=headers)
            Logger.add_response(result)
            return result

    @staticmethod
    def patch(url, headers, body):
        with allure.step("PATCH"):
            Logger.add_request(url, method="PATCH")
            result = requests.patch(url, headers=headers,json=body)
            Logger.add_response(result)
            return result


class BeautifyMethods:

    @staticmethod
    def print_pretty_xml(xml_string):
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        print(pretty_xml)

    @staticmethod
    def print_pretty_json(json_string):
        pretty_json = json.dumps(json_string, indent=4, ensure_ascii=False)
        print(pretty_json)