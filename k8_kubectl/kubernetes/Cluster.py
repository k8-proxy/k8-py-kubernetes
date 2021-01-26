import warnings

from kubernetes import config, client
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api

from k8_kubectl.kubernetes.Namespace                import Namespace
from k8_kubectl.kubernetes.Pod                      import Pod
from osbot_utils.decorators.lists.group_by          import group_by
from osbot_utils.decorators.lists.index_by          import index_by
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Misc                         import ignore_warning__unclosed_ssl


class Cluster:

    def __init__(self, default_namespace='default', config_file=None):
        ignore_warning__unclosed_ssl()
        self.default_namespace   = Namespace(name=default_namespace, cluster=self)
        self.config_file         = config_file

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

    def namespace(self, name=None) -> Namespace:
        if name:
            return Namespace(name=name, cluster=self)
        return self.default_namespace

    def namespaces(self):
        return [self.namespace(name) for name in self.namespaces_names()]

    @index_by
    @group_by
    def namespaces_infos(self):
        return [self.namespace(name).info() for name in self.namespaces_names()]

    def namespaces_names(self):
        return [item.metadata.name for item in self.namespaces_raw()]

    def namespaces_raw(self):
        return self.api_core().list_namespace().items

    def pod(self, pod_name):
        from k8_kubectl.kubernetes.Pod import Pod                                               # circular reference
        return Pod(name=pod_name, cluster=self)

    @index_by
    @group_by
    def pods(self):
        pods = []
        pods_data = self.api_core().list_namespaced_pod(namespace=self.namespace().name)
        for item in pods_data.items:
            pods.append(Pod(item.metadata.name, cluster=self))
        return pods

    def pods_all(self):
        pods = []
        pods_data = self.api_core().list_pod_for_all_namespaces(watch=False)
        for item in pods_data.items:
            pods.append(Pod(item.metadata.name, cluster=self))
        return pods

    def pods_in_phase(self, phase):
        return self.pods(group_by='phase').get(phase)

    def pods_pending(self):
        return self.pods_in_phase('Pending')

    def set_default_namespace(self, name):
        self.default_namespace = Namespace(name)

