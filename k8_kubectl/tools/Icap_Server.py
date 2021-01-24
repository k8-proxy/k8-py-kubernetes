from osbot_utils.utils.Http import port_is_open, OPTIONS, is_port_open

from k8_kubectl.utils.HA_Proxy import HA_Proxy


class Icap_Server:

    def __init__(self, server_address, port=1344):
        self.server_address = server_address
        self.port           = port
        self.ha_proxy       = HA_Proxy()


    def stats(self):
        return self.ha_proxy.server_stats(self.server_address)

    def status(self):
        stats = self.stats()
        if stats:
            return self.stats().get('check_status')
        else:
            stats = self.stats()

    def is_port_open(self, timeout=0.5):
        return is_port_open(self.server_address, self.port, timeout=timeout)