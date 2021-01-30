from unittest import TestCase

from k8_kubernetes.utils.EC_Server import EC2_Server


class test_EC2_Server(TestCase):

    def setUp(self) -> None:
        self.ec2_servers = EC2_Server()

