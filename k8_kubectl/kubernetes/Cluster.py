import warnings

from kubernetes import config, client
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache import cache

from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import ignore_warning__unclosed_ssl


class Cluster:

    def __init__(self):
        ignore_warning__unclosed_ssl()

    @cache
    def api_apps(self) -> AppsV1Api:
        config.load_kube_config()
        return client.AppsV1Api()

    @cache
    def api_core(self) -> CoreV1Api:
        config.load_kube_config()
        return client.CoreV1Api()

    @index_by
    def namespaces(self):
        namespaces = []
        for item in self.api_core().list_namespace().items:
            namespace = {   "id"  : item.metadata.uid    ,
                            "name": item.metadata.name   }
            namespaces.append(namespace)
        return namespaces

    @index_by
    @group_by
    def pods(self):
        pods = []
        for item in self.api_core().list_pod_for_all_namespaces(watch=False).items:
            pod = { "id"         : item.metadata.uid         ,
                    "ip"         : item.status.pod_ip        ,
                    "phase"      : item.status.phase         ,
                    "name"       : item.metadata.name        ,
                    "namespace"  : item.metadata.namespace   ,
                    "start_time" : item.status.start_time    }
            pods.append(pod)

        return pods


