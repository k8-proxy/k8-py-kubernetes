import os
from pprint import pprint
from unittest import TestCase

from dotenv import load_dotenv
from kubernetes import client
from osbot_utils.utils.Misc import random_text, random_id

from k8_kubernetes.kubernetes.Cluster import Cluster
from k8_kubernetes.kubernetes.Namespace import Namespace
from osbot_utils.utils.Files import file_exists


class test_Namespace(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.config_file = os.environ.get('TEST_KUBE_CONFIG_FILE')
        self.name        = os.environ.get('TEST_KUBE_NAMESPACE')
        self.cluster     = Cluster  (default_namespace=self.name, config_file=self.config_file)
        self._           = Namespace(name             =self.name, cluster    =self.cluster    )

    def test__init__(self):
        assert file_exists(self.config_file)
        assert self._.name == self.name

    #def test_create(self):
    #    pass    # see test_create__delete

    def test_create__delete(self):
        namespace = Namespace(random_id(prefix='unit-test-'), cluster=self.cluster)
        assert namespace.exists    ()                       is False
        assert namespace.info      ()                       == {}
        assert namespace.create    ().get('message')        == 'namespace created'
        assert namespace.exists    ()                       is True
        assert namespace.info      ().get('status' ).phase  =='Active'
        assert self.cluster.namespaces_names().index(namespace.name) > -1
        assert namespace.delete    ().get('message')        == 'namespace deleted'
        assert namespace.info      ().get('status' ).phase  =='Terminating'
        #assert namespace.exists()                is True # todo add method to wait for termination status to complete

    # def test_exists(self):
    #     pass    # see test_create__delete
    #
    # def test_info(self):
    #     pass    # see test_create__delete