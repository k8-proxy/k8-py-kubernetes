from unittest import TestCase

from k8_kubectl.tools.Icap_Server_Status import Icap_Server_Status


class test_Icap_Server_Status(TestCase):

    def setUp(self) -> None:
        self.icap_server_status = Icap_Server_Status()

