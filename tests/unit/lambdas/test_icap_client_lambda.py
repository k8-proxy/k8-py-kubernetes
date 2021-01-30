import  os
from    pprint      import pprint
from    unittest    import TestCase
from    dotenv      import load_dotenv

from osbot_aws.apis.Lambda           import Lambda
from k8_kubernetes.utils.Icap_Client import Icap_Client


class test_icap_client_lambda(TestCase):

    def setUp(self) -> None:
        load_dotenv()                                                   # todo: refactor into helper class
        self.target_ip = os.environ.get('TEST_ICAP_SERVER')
        self.aws_lambda = Lambda('icap-client-lambda')
        print()

    def test_invoke_function(self):
        payload = {"command": "/usr/local/c-icap/bin/c-icap-client",
                   "params": ["-i", self.target_ip, "-s", "gw_rebuild"]}
        result = self.aws_lambda.invoke(payload)

        icap_data = result.get('stderr')
        icap_headers = Icap_Client().extract_icap_headers(icap_data)
        assert icap_headers.get('status_code') == '200'
        assert icap_headers.get('Service'    ) == 'C-ICAP/0.5.7 server - Glasswall Rebuild service'

    def test_invoke_function_ssh(self):
        payload = {"command": "ssh",
                   "params": ["-i","asf", f"ubuntu@{self.target_ip }"]}
        result = self.aws_lambda.invoke(payload)

        assert result.get('stderr') == 'PRIV_END: seteuid: Operation not permitted\r\n'

    def check_icap_server(self,address):
        payload = {"command": "/usr/local/c-icap/bin/c-icap-client",
                   "params": ["-i",address,"-s","gw_rebuild"]}
        result = self.aws_lambda.invoke(payload)
        pprint(result)
        icap_data = result.get('stderr')
        icap_headers = Icap_Client().extract_icap_headers(icap_data)
        return icap_headers

    def test_check_icap_server(self):
        icap_headers = self.check_icap_server(self.target_ip )
        assert icap_headers.get('status_code') == '200'
        assert icap_headers.get('Service') == 'C-ICAP/0.5.7 server - Glasswall Rebuild service'