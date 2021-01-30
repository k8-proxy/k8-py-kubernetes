from pprint import pprint
from unittest import TestCase

from k8_kubernetes.utils.Icap_Client import Icap_Client
from osbot_aws.apis.Lambda import Lambda


class test_icap_client_lambda(TestCase):

    def setUp(self) -> None:
        self.aws_lambda = Lambda('icap-client-lambda')
        print()

    def test_invoke_function(self):
        payload = {"command": "/usr/local/c-icap/bin/c-icap-client",
                   "params": ["-i","54.171.103.144","-s","gw_rebuild"]}
        result = self.aws_lambda.invoke(payload)

        icap_data = result.get('stderr')
        icap_headers = Icap_Client().extract_icap_headers(icap_data)
        pprint(icap_headers)

    def test_invoke_function_ssh(self):
        payload = {"command": "ssh",
                   "params": ["-i","asf", "ubuntu@54.171.103.144"]}
        result = self.aws_lambda.invoke(payload)

        pprint(result)

    def check_icap_server(self,address):
        payload = {"command": "/usr/local/c-icap/bin/c-icap-client",
                   "params": ["-i",address,"-s","gw_rebuild"]}
        result = self.aws_lambda.invoke(payload)
        pprint(result)
        icap_data = result.get('stderr')
        icap_headers = Icap_Client().extract_icap_headers(icap_data)
        return icap_headers

    def test_check_icap_server(self):
        address = "52.47.91.28"
        result = self.check_icap_server(address)
        pprint(result)