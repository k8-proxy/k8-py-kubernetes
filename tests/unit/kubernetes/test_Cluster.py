from pprint import pprint
from unittest import TestCase

import pytest
from pytest import skip

from osbot_utils.utils.Files import path_combine, file_exists
from osbot_utils.utils.Yaml import yaml_load
from k8_kubernetes.kubernetes.Cluster import Cluster


class test_Kubectl(TestCase):

    def setUp(self):
        self.cluster = Cluster()
        if self.cluster.load_config() is False:
            skip('no K8 clusters available in current environment')
        print()

    @pytest.mark.skip('refactor into a new Deployment class')
    def test_deployment(self):
        deployment_file = path_combine('../../test_files/deployment','nginx-deployment.yaml')
        assert file_exists(deployment_file)
        deployment = yaml_load(deployment_file)
        resp = self.cluster.api_apps().create_namespaced_deployment(body=deployment, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)

    def test_namespaces(self):
        assert len(self.cluster.namespaces()) > 0

    def test_namespaces_infos(self):
        namespaces = self.cluster.namespaces_infos(index_by='name')
        assert 'default' in namespaces
        assert namespaces.get('default').get('name'  )       == 'default'
        assert namespaces.get('default').get('status').phase == 'Active'

    def test_pods(self):
        assert type(self.cluster.pods()) is list

    def test_pods_all(self):
        assert len(self.cluster.pods_all()) > 0
