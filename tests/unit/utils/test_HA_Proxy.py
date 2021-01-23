from unittest import TestCase
from k8_kubectl.utils.HA_Proxy import HA_Proxy


class test_HA_Proxy(TestCase):

    def setUp(self) -> None:
        self.ha_proxy = HA_Proxy()

    def test_server_url(self):
        config = self.ha_proxy.config_from_env()
        assert self.ha_proxy.server_url() == f"{config.get('schema')}://{config.get('server')}:{config.get('port')}"

    def test_stats(self):
        result = self.ha_proxy.stats()
        assert 'svname' in set(result[0])
        from pprint import pprint
        from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import env_vars
        pprint(env_vars())
