from osbot_utils.decorators.methods.cache import cache
from osbot_utils.utils.Json import json_loads

from k8_kubectl.kubernetes.Cluster import Cluster


class Pod():

    def __init__(self, pod_name, namespace='default'):
        self.pod_name  = pod_name
        self.namespace = namespace

    @cache
    def api_core(self):
        return Cluster().api_core()

    def create(self, manifest, namespace='default'):
        try:
            pod_info = self.api_core().create_namespaced_pod(body=manifest, namespace=namespace)
            return {'status': 'ok', 'data' : pod_info }
        except Exception as exception:
            error = json_loads(exception.body)
            return {'status':'error', 'message': error.get('message'), 'error': error }

    def delete(self):
        if self.exists():       # false positive when pod is running
            self.api_core().delete_namespaced_pod(name=self.pod_name, namespace=self.namespace)
            return True
        return False            # todo add a wait for deletion

    def exists(self):
        return self.info() is not None

    def info(self):
        try:
            return self.api_core().read_namespaced_pod(name=self.pod_name, namespace='default')
        except:
            return None