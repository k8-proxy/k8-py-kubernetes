from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import path_combine, file_exists
from osbot_utils.utils.Misc import random_string
from osbot_utils.utils.Yaml import yaml_load

from k8_kubectl.kubernetes.Cluster import Cluster
from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import lower


class test_Kubectl(TestCase):

    def setUp(self):
        self.k8 = Cluster()
        print()

    def test_deployment(self):
        deployment_file = path_combine('../../test_files/deployment','nginx-deployment.yaml')
        assert file_exists(deployment_file)
        deployment = yaml_load(deployment_file)
        resp = self.k8.api_apps().create_namespaced_deployment(body=deployment, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)

    def test_namespaces(self):
        assert len(self.k8.namespaces()) > 0


    def test_pods(self):
        assert len(self.k8.pods()) > 0

        pprint(self.k8.pods(index_by='name'))
