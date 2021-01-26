from kubernetes import client
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Status import status_ok, status_error, status_warning


class Namespace:
    def __init__(self, name, cluster):
        self.cluster   = cluster
        self.name      = name

    def create(self):
        if self.exists():
            return status_error(message=f"namespace already existed: {self.name}")
        try:
            manifest = client.V1Namespace(metadata=client.V1ObjectMeta(name=self.name))
            result = self.cluster.api_core().create_namespace(manifest)
        except Exception as exception:
            return status_error(data=exception)

        return status_ok(message="namespace created", data=result)

    def delete(self):
        if self.exists():
            result = self.cluster.api_core().delete_namespace(name=self.name)
            return status_ok(message="namespace deleted", data=result)
        return status_warning(message="namespace already existed")

    def exists(self):
        return self.info() != {}

    def format_namespace(self, item):
        data = {}
        if item:
            metadata = item.metadata
            data = {  'annotations': metadata.annotations        ,
                      'label'      : metadata.labels             ,
                      'created_at' : metadata.creation_timestamp ,
                      'name'       : metadata.name               ,
                      'spec'       : item.spec                   ,
                      'status'     : item.status                 }
        return data

    def info(self):
        return self.format_namespace(self.info_raw())

    def info_raw(self):
        try:
            return self.cluster.api_core().read_namespace(name=self.name)
        except:
            return None

    def not_exists(self):
        return self.info() == {}
