from pprint import pprint
from unittest import TestCase
from k8_kubectl.utils.Icap_Server import Icap_Server

class test_Icap_Server(TestCase):

    def setUp(self) -> None:
        #self.server_address = '51.143.248.246'
        #self.server_address = "20.67.220.25"
        self.server_address = '34.242.162.186'
        self.server_address = '52.50.33.203'
        #'3.250.131.130'
        self.icap_service   = 'gw_rebuild'
        self.icap_timeout   = 15
        self.icap_server    = Icap_Server(server_address=self.server_address, icap_service=self.icap_service, icap_timeout=self.icap_timeout)


    def test_status_ha_proxy(self):
        assert self.icap_server.status_ha_proxy() is True #['L4OK', 'L4TOUT']

    def test_status_http_port(self):
        assert self.icap_server.status_http_port() is True

    def test_status_icap_echo(self):
        assert self.icap_server.status_icap_echo() is True

    def test_status_icap_file(self):
        assert self.icap_server.status_icap_file() is True

