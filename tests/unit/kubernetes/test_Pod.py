from unittest import TestCase
from k8_kubectl.kubernetes.Cluster import Cluster
from osbot_utils.utils.Misc import random_string, lower
from k8_kubectl.kubernetes.Manifest import Manifest
from k8_kubectl.kubernetes.Pod import Pod

class test_Pod(TestCase):

    pod : Pod

    @classmethod
    def setUpClass(cls) -> None:
        cls.pod_name     = 'temp-pod'
        cls.image_name   = 'nginx'
        cls.pod_manifest = Manifest().pod_simple(cls.pod_name, cls.image_name)
        cls.cluster      = Cluster()
        cls.pod          = Pod(name=cls.pod_name, cluster=cls.cluster)
        cls.pod_info     = cls.pod.create(cls.pod_manifest)

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.pod.delete().get('message')         == "pod deleted"
        assert cls.pod.event_wait_for__type__deleted() is True
        assert cls.pod.exists()                        is False

    def setUp(self) -> None:
        pass

    def test_create(self):
        assert self.pod.event_wait_for('MODIFIED', 'Running')

    def test_delete(self):
        pass                # todo: add tests for bad deletion params

    def test_exists(self):
        assert self.pod.exists()                          is True
        assert Pod(lower(random_string()), None).exists() is False

    def test_info(self):
        pod_info = self.pod.info()
        del pod_info['id']
        del pod_info['start_time']
        assert pod_info == {'image'     : 'nginx'   ,
                            'ip'        : None      ,
                            'name'      : 'temp-pod',
                            'namespace' : 'default' ,
                            'phase'     : 'Pending' }




