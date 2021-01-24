from unittest import TestCase
from k8_kubectl.utils.Icap_Server import Icap_Server

ips = ['51.143.248.246', '51.89.210.149', '3.248.187.0', '54.155.152.233', '34.245.236.144', '34.245.48.242', '34.242.162.186', '34.244.46.139', '34.241.51.250', '34.247.85.155', '34.251.124.159', '3.250.57.14', '34.244.7.158', '54.154.178.234', '63.33.204.68', '34.247.48.151', '18.202.249.123', '34.244.33.69', '3.248.203.245']

class test_Icap_Server(TestCase):

    def setUp(self) -> None:
        self.server_address = '51.143.248.246'
        self.icap_server = Icap_Server(self.server_address)
        print()


    def test_status(self):
        assert self.icap_server.status() in ['L4OK', 'L4TOUT']

        #for ip in ips:
        #    status = Icap_Server(ip).status()
        #    print('::', ip, status)

