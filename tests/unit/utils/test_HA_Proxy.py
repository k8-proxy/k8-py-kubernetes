from pprint import pprint
from unittest import TestCase

from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import list_set
from k8_kubectl.utils.HA_Proxy import HA_Proxy


class test_HA_Proxy(TestCase):

    def setUp(self) -> None:
        self.ha_proxy = HA_Proxy()
        print()

    def test_resolve_server_id(self):
        ip           = self.ha_proxy.server_ips()[0]
        server_id    = self.ha_proxy.resolve_server_id(ip)
        server_stats = self.ha_proxy.server_stats(server_id)
        pprint(server_stats)

    def test_server_url(self):
        config = self.ha_proxy.config_from_env()
        assert self.ha_proxy.server_url() == f"{config.get('schema')}://{config.get('server')}:{config.get('port')}"

    def test_stats(self):
        assert 'svname' in set(self.ha_proxy.stats()[0])

    def test_server_list(self):
        assert len(self.ha_proxy.server_list()) > 0

    def test_server_names_and_ips(self):
        data = self.ha_proxy.server_names_and_ips()
        assert list_set(data) == ['ips', 'names']

    def test_server_ips(self):
        ips = self.ha_proxy.server_ips()
        assert len(ips) > 0
        assert len(ips[0].split('.')) == 4

    def test_server_names(self):
        names = self.ha_proxy.server_names()
        assert len(names) > 0
        assert len(names[0].split('.')) == 1

