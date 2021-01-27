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