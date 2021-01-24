from kubernetes.watch import Watch
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Json import json_loads

from k8_kubectl.kubernetes.Cluster import Cluster


class Pod:

    def __init__(self, pod_name, cluster=None):
        self.pod_name    = pod_name
        self.cluster     = cluster or Cluster()

    @cache_on_self
    def api_core(self):
        return self.cluster.api_core()

    def create(self, manifest):
        try:
            pod_info = self.api_core().create_namespaced_pod(body=manifest, namespace=self.cluster.namespace)
            return {'status': 'ok', 'data' : pod_info }
        except Exception as exception:
            error = json_loads(exception.body)
            return {'status':'error', 'message': error.get('message'), 'error': error }

    def delete(self):
        if self.exists():       # todo: check for side effects
        #try:
            self.api_core().delete_namespaced_pod(name=self.pod_name, namespace=self.cluster.namespace)
            return True
        #except Exception as exception:
        #    from pprint import pprint
        #    pprint(exception)
        return False            # todo add a wait for deletion

    def exists(self):
        return self.info() is not None

    def info(self):
        try:
            return self.api_core().read_namespaced_pod(name=self.pod_name, namespace=self.cluster.namespace)
        except: #Exception as exception:
            return None                     # todo: capture exception in log

    def event_wait_for(self, wait_for_type, wait_for_phase=None, label='', timeout=10):
        for event in Watch().stream(func            = self.api_core().list_namespaced_pod,
                                    namespace       = self.cluster.namespace                     ,
                                    label_selector  = label                              ,
                                    timeout_seconds = timeout                            ):
            event_type  = event.get('type')
            event_phase = event.get('object').status.phase
            print(event_type, event_phase)
            if event_type == wait_for_type:
                if event_phase is not None or event_phase == wait_for_phase:
                    return True
        return False

    def event_wait_for__type__deleted(self, label=None,timeout=20):
        return self.event_wait_for(wait_for_type='DELETED', wait_for_phase=None, label=label, timeout=timeout)