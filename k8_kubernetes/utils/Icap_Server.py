from k8_kubernetes.utils.Files_To_Rebuild import Files_To_Rebuild
from k8_kubernetes.utils.Icap_Client import Icap_Client
from osbot_utils.utils.Http import port_is_open, OPTIONS, is_port_open

from k8_kubernetes.utils.HA_Proxy import HA_Proxy


class Icap_Server:

    def __init__(self, server_address, icap_service, port=1344, icap_timeout=15):
        self.server_address = server_address
        self.icap_service   = icap_service
        self.port           = port
        self.ha_proxy       = HA_Proxy()
        self.icap_client    = Icap_Client()
        self.icap_client.set_icap_timeout(icap_timeout)


    def stats(self):
        return self.ha_proxy.server_stats(self.server_address)


    def status_ha_proxy(self):
        stats = self.stats()
        if stats:
            return self.stats().get('check_status') == 'L4OK'

    def status_http_port(self, timeout=1):
        return is_port_open(self.server_address, self.port, timeout=timeout)

    def status_icap_echo(self):
        result = self.icap_client.icap_echo(self.server_address)
        if result.get('docker_run').get('status') == 'error':
            return False
        return result.get('icap_headers').get('status_code') == '200'

    def status_icap_file(self):
        file_to_rebuild = Files_To_Rebuild().file_word_with_macros()
        file_to_process = file_to_rebuild.get('local_path')
        result = self.icap_client.icap_process_file(self.server_address, self.icap_service, file_to_process)
        docker_run   = result.get('icap_result').get('docker_run')
        #icap_headers = result.get('icap_result').get('icap_headers')
        md5s         = result.get('md5s')
        if docker_run.get('status') == 'ok':
            if md5s:
                return md5s.get('rebuilt') is not None
        return False