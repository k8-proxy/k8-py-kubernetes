import warnings

from kubernetes import config, client
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Misc import ignore_warning__unclosed_ssl


class Cluster:

    def __init__(self, namespace='default', config_file=None):
        ignore_warning__unclosed_ssl()
        self.namespace   = namespace
        self.config_file = config_file

    @cache_on_self
    def api_apps(self) -> AppsV1Api:
        self.load_config()
        return client.AppsV1Api()

    @cache_on_self
    def api_core(self) -> CoreV1Api:
        self.load_config()
        return client.CoreV1Api()

    def info(self):
        return self.api_core().list_config_map_for_all_namespaces()

    def load_config(self):
        try:
            config.load_kube_config(config_file=self.config_file)
            return True
        except Exception as error:
            print(error)
            return False

    @index_by
    def namespaces(self):
        namespaces = []
        for item in self.api_core().list_namespace().items:
            namespace = {   "id"  : item.metadata.uid    ,
                            "name": item.metadata.name   }
            namespaces.append(namespace)
        return namespaces

    def pod(self, pod_name):
        from k8_kubectl.kubernetes.Pod import Pod                                               # circular reference
        return Pod(pod_name=pod_name, cluster=self)

    @index_by
    @group_by
    def pods(self):
        pods = []
        if self.namespace:
            pods_data = self.api_core().list_namespaced_pod(self.namespace)
        else:
            pods_data = self.api_core().list_pod_for_all_namespaces(watch=False)
        for item in pods_data.items:
            pod = { "id"         : item.metadata.uid         ,
                    "ip"         : item.status.pod_ip        ,
                    "phase"      : item.status.phase         ,
                    "name"       : item.metadata.name        ,
                    "namespace"  : item.metadata.namespace   ,
                    "start_time" : item.status.start_time    }
            pods.append(pod)
        return pods

    def pods_in_phase(self, phase):
        return self.pods(group_by='phase').get(phase)

    def pods_pending(self):
        return self.pods_in_phase('Pending')


