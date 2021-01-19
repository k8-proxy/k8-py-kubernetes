from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Misc import random_string

from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import lower
from k8_kubectl.kubernetes.Manifest import Manifest
from k8_kubectl.kubernetes.Pod import Pod



class test_Pod(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.pod_name     = 'temp-pod'
        cls.image_name   = 'nginx'
        cls.pod_manifest = Manifest().pod_simple(cls.pod_name, cls.image_name)
        cls.pod          = Pod(cls.pod_name)
        cls.pod_info     = cls.pod.create(cls.pod_manifest)

        #assert cls.pod_info.kind == 'Pod'

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.pod.delete() is True

    def setUp(self) -> None:
        pass

    def test_create(self):
        pass                # todo: add tests for bad creation workflows

    def test_delete(self):
        pass                # todo: add tests for bad deletion params

    def test_exists(self):
        assert self.pod.exists()                    is True
        assert Pod(lower(random_string())).exists() is False

    def test_info(self):
        pod_info = self.pod.info()
        assert pod_info.kind                     == 'Pod'
        assert pod_info.metadata.name            == self.pod_name
        assert pod_info.spec.containers[0].image == 'nginx'


