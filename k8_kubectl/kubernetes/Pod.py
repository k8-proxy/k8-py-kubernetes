from kubernetes.client import ApiException
from kubernetes.watch                             import Watch
from osbot_utils.utils.Json import json_loads

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Status                     import status_ok, status_error

class Pod:

    def __init__(self, name, cluster):
        self.name    = name
        self.cluster = cluster

    @cache_on_self
    def api_core(self):
        return self.cluster.api_core()

    def create(self, manifest):
        try:
            pod_info = self.api_core().create_namespaced_pod(body=manifest, namespace=self.cluster.namespace().name)
            return status_ok(message="pod created", data=pod_info)
        except ApiException as exception:
            exception_body = json_loads(exception.body)
            return status_error(message=exception_body.get('message'), error=exception)
        except Exception as exception:
            return status_error(error=exception)

    def delete(self):
        if self.exists():       # todo: check for other states of pod that could affect this deletion action
            data = self.api_core().delete_namespaced_pod(name=self.name, namespace=self.cluster.namespace().name)
            return status_ok(message="pod deleted", data=data)

        return status_ok(message="pod not deleted (since it didn't exist)")

    def exists(self):
        return self.info() != {}

    def format_pod(self, item):
        data = {}
        if item:
            data = { "id"        : item.metadata.uid             ,
                     "ip"        : item.status.pod_ip            ,
                     "image"     : item.spec.containers[0].image ,
                     "phase"     : item.status.phase             ,
                     "name"      : item.metadata.name            ,
                     "namespace" : item.metadata.namespace       ,
                     "start_time": item.status.start_time        }
        return data

    def info(self):
        return self.format_pod(self.info_raw().get('data'))

    def info_raw(self):
        try:
            data = self.api_core().read_namespaced_pod(name=self.name, namespace=self.cluster.namespace().name)
            return status_ok(data=data)
        except Exception as exception:
            return status_error(error=exception)

    def event_wait_for(self, wait_for_type, wait_for_phase=None, label='', timeout=10):
        for event in Watch().stream(func            = self.api_core().list_namespaced_pod,
                                    namespace       = self.cluster.namespace().name      ,
                                    label_selector  = label                              ,
                                    timeout_seconds = timeout                            ):
            event_type  = event.get('type')
            event_phase = event.get('object').status.phase
            #print(event_type, event_phase)          # todo: capture in log
            if event_type == wait_for_type:
                if event_phase is not None or event_phase == wait_for_phase:
                    return True
        return False

    def event_wait_for__type__deleted(self, label=None,timeout=20):
        return self.event_wait_for(wait_for_type='DELETED', wait_for_phase=None, label=label, timeout=timeout)

    def __repr__(self):
        return f'Pod: {self.name}'