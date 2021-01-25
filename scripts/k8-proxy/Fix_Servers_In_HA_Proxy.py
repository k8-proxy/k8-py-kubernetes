from pprint import pprint
from unittest import TestCase

from k8_kubectl.utils.Icap_Server import Icap_Server


class Fix_Servers_In_HA_Proxy:

    def __init__(self):
      self.icap_timeout = 15
      self.icap_service = 'gw_rebuild'

    def target_ips(self):
        # ips = ['51.143.248.246', '51.89.210.149', '3.248.187.0', '54.155.152.233', '34.245.236.144', '34.245.48.242',
        #        '34.242.162.186', '34.244.46.139', '34.241.51.250', '34.247.85.155', '34.251.124.159', '3.250.57.14',
        #        '34.244.7.158', '54.154.178.234', '63.33.204.68', '34.247.48.151', '18.202.249.123', '34.244.33.69',
        #        '3.248.203.245']
        ip_icap_head = ['51.143.248.246',
                        '51.89.210.149',
                        '3.248.187.0',
                        '34.245.236.144',
                        '34.245.48.242',
                        '34.242.162.186',
                        '34.244.46.139',
                        '34.247.85.155',
                        '3.250.57.14',
                        '34.244.7.158',
                        '54.154.178.234',
                        '18.202.249.123',
                        '3.248.203.245']

        ip_icap_file_ok = ['34.245.48.242',
                           '34.244.7.158',
                           '54.154.178.234',
                           '3.248.203.245',
                           '34.242.162.186']
        ip_icap_file_not_ok = ['51.143.248.246',
                    '51.89.210.149',
                    '3.248.187.0',
                    '34.245.236.144',
                    '34.244.46.139',
                    '34.247.85.155',
                    '3.250.57.14',
                    '18.202.249.123']
        return ip_icap_file_ok

    def get_icap_server(self, server_ip):
        return Icap_Server(server_address = server_ip    ,
                           icap_service   = self.icap_service ,
                           icap_timeout   = self.icap_timeout )

    def get_ha_proxy_status(self):
        return self.get_status("status_ha_proxy")

    def get_icap_echo_status(self):
        return self.get_status("status_icap_echo")

    def get_icap_file_status(self):
        return self.get_status("status_icap_file")

    def get_status(self, status_function):
        result = {'ok' :[], 'not_ok': [] }
        for server_ip in self.target_ips():
            icap_server = self.get_icap_server(server_ip)
            if getattr(icap_server, status_function)():
                result.get('ok').append(server_ip)
            else:
                result.get('not_ok').append(server_ip)
        return result





class test_Fix_Servers_In_HA_Proxy(TestCase):

    def setUp(self) -> None:
        self._ = Fix_Servers_In_HA_Proxy()
        print()

    def test_get_ha_proxy_status(self):
        result = self._.get_ha_proxy_status()
        pprint(result)

    def test_get_icap_head_status(self):
        self._.icap_timeout = 60
        result = self._.get_icap_echo_status()
        pprint(result)

        result = {'not_ok': ['54.155.152.233',
                    '34.241.51.250',
                    '34.251.124.159',
                    '63.33.204.68',
                    '34.247.48.151',
                    '34.244.33.69'],
                  'ok': ['51.143.248.246',
                        '51.89.210.149',
                        '3.248.187.0',
                        '34.245.236.144',
                        '34.245.48.242',
                        '34.242.162.186',
                        '34.244.46.139',
                        '34.247.85.155',
                        '3.250.57.14',
                        '34.244.7.158',
                        '54.154.178.234',
                        '18.202.249.123',
                        '3.248.203.245']}

    def test_get_icap_file_status(self):
        result = self._.get_icap_file_status()
        pprint(result)

        {'not_ok': ['34.245.48.242',
                    '34.244.7.158',
                    '54.154.178.234',
                    '3.248.203.245',
                    '34.242.162.186'],
         'ok': []}


        # {'not_ok': ['51.143.248.246',
        #             '51.89.210.149',
        #             '3.248.187.0',
        #             '34.245.236.144',
        #             '34.242.162.186',
        #             '34.244.46.139',
        #             '34.247.85.155',
        #             '3.250.57.14',
        #             '18.202.249.123'],
        #  'ok': ['34.245.48.242', '34.244.7.158', '54.154.178.234', '3.248.203.245']}