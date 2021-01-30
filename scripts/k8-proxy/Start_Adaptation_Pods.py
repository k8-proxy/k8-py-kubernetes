import os
from pprint import pprint
from unittest import TestCase

from dotenv import load_dotenv

from k8_kubernetes.kubernetes.Cluster import Cluster
from k8_kubernetes.kubernetes.Manifest import Manifest
from osbot_utils.utils.Misc import append_random_string, lower


class Start_Adaptation_Pods:

    def __init__(self, namespace, config_file):
        self.cluster     = Cluster(default_namespace=namespace, config_file=config_file)
        self.image_name  = 'nginx'
        self.name_prefix = 'temp-pods'

    def create_pods(self, count):
        pods = []
        for i in range(0,count):
            pod = self.create_pod()
            pods.append(pod)
        return pods

    def create_pod(self):
        pod_name     = append_random_string(self.name_prefix)
        pod_manifest = self.get_manifest(pod_name)
        pod          = self.cluster.pod_create(name=pod_name, manifest=pod_manifest).get('pod')
        return pod

    def delete_pods(self):
        deleted_pods = []
        for pod in self.cluster.pods():
            pod_name = pod.name
            if pod_name.startswith(self.name_prefix):
                deleted_pods.append(pod_name)
        return deleted_pods

    def list_pods(self):
        return self.cluster.pods()

    def get_manifest(self, pod_name):
        return Manifest().pod_simple(pod_name, self.image_name)

    def setup(self):
        self.cluster.namespace().create()  # make sure test namespace exists
        return self


class test_Start_Adaptation_Pods(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.config_file = os.environ.get('TEST_KUBE_CONFIG_FILE')
        self.namespace   = os.environ.get('TEST_KUBE_NAMESPACE')

        self._ = Start_Adaptation_Pods(namespace=self.namespace, config_file=self.config_file)
        self._.setup()
        print()

    def test_create_pod(self):
        result = self._.create_pod()
        pods = self._.list_pods()
        pprint(result)
        pprint(pods)

    def test_create_pods(self):
        self._.create_pods(10)

    def test_create_delete_pods(self):
        pods = self._.create_pods(10)
        for pod in pods:
            print(f"deleting pod {pod.name}")
            pod.delete()

    def test_delete_pods(self):
        pods = self._.delete_pods()
        pprint(pods)

    def test_list_pods(self):
        pods = self._.cluster.pods()
        pprint(pods)

    def test_setup(self):
        assert self._.setup() == self._
