from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import file_contents, file_exists

from k8_kubernetes.kubernetes.Cluster import Cluster
from k8_kubernetes.kubernetes.Pod import Pod


class Delete_Pending_Pods:

    def __init__(self, namespace, config_file):
      self.cluster = Cluster(namespace=namespace, config_file=config_file)

    def delete_pods(self):
        deleted_pods = []
        for pod in self.cluster.pods_pending():
            pod_name = pod.get('name')
            if self.cluster.pod(pod_name=pod_name).delete():
                deleted_pods.append(pod_name)
            else:
                print(f'Error: failed to delete pod {pod_name}')
        return deleted_pods

class test_Delete_Pending_Pods(TestCase):

    def setUp(self) -> None:
        self.config_file = "/Users/diniscruz/_dev/_AWS_Config/54.171.103.144/config"
        self.namespace   = "icap-adaptation"

        self._ = Delete_Pending_Pods(namespace=self.namespace, config_file=self.config_file)
        print()

    def test_delete_pods(self):
        result = self._.delete_pods()

        pprint(result)

    def test_check_pods(self):
        cluster = Cluster(namespace=self.namespace, config_file=self.config_file)

        pprint(cluster.pod('adaptation-service-7c5b5b9548-2vb5w').info())





