import os
from pprint import pprint
from unittest import TestCase

from dotenv import load_dotenv
from pytest import skip

from k8_kubernetes.utils.HA_Proxy import HA_Proxy
from k8_kubernetes.utils.Icap_Server import Icap_Server

class test_Icap_Server(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.server_address = os.environ.get('TEST_ICAP_SERVER')
        self.icap_service   = os.environ.get('TEST_ICAP_SERVICE')
        self.icap_timeout   = 20
        self.icap_server    = Icap_Server(server_address=self.server_address, icap_service=self.icap_service, icap_timeout=self.icap_timeout)


    def test_status_ha_proxy(self):
        self.ha_proxy = HA_Proxy()
        if self.ha_proxy.server_online() is False:
            skip('ha_proxy server is not online')
        assert self.icap_server.status_ha_proxy() is True

    def test_status_http_port(self):
        assert self.icap_server.status_http_port() is True

    def test_status_icap_echo(self):
        assert self.icap_server.status_icap_echo() is True

    def test_status_icap_file(self):
        assert self.icap_server.status_icap_file() is True

