class Manifest:

    # todo: check if the code below can be replaced with something like
    #  client.V1Namespace(metadata=client.V1ObjectMeta(name=self.name))
    def pod_simple(self, pod_name, image_name):
        return  { 'apiVersion': 'v1'                                       ,
                  'kind'      : 'Pod'                                      ,
                  'metadata'  : { 'name'      : pod_name                } ,
                  'spec'      : { 'containers': [{ 'image': image_name ,
                                                   'name' : image_name }] } }