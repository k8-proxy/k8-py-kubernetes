from pprint import pprint
from unittest import TestCase

from k8_kubectl.kubernetes.Cluster import Cluster
from k8_kubectl.kubernetes.Manifest import Manifest
from osbot_utils.utils.Misc import append_random_string, lower


class Start_Adaptation_Pods:

    def __init__(self, namespace, config_file):
        self.cluster    = Cluster(namespace=namespace, config_file=config_file)
        self.image_name = 'nginx'

    def create_pods(self, pod_name):
        pod_name     = lower(pod_name)                          # make sure the pod name is all lowercase
        pod_manifest = self.get_manifest(pod_name)
        pod          = self.cluster.pod(pod_name=pod_name)
        create       = pod.create(manifest=pod_manifest)
        return { "pod": pod, "create": create }

    def list_pods(self):
        return self.cluster.pods()

    def get_manifest(self, pod_name):
        return Manifest().pod_simple(pod_name, self.image_name)



class test_Start_Adaptation_Pods(TestCase):

    def setUp(self) -> None:
        self.config_file = "/Users/diniscruz/_dev/_AWS_Config/54.171.103.144/config"
        self.namespace   = "default-test"

        self._ = Start_Adaptation_Pods(namespace=self.namespace, config_file=self.config_file)
        print()

    def test_create_pods(self):
        pod_name = append_random_string('a-new-test-pod')
        result = self._.create_pods(pod_name)
        pods = self._.list_pods()
        pprint(result)
        #pprint(pods)


    def test_list_pods(self):
        pods = self._.list_pods()
        pprint(pods)


