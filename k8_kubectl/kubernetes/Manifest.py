class Manifest:

    def pod_simple(self, pod_name, image_name):
        return  { 'apiVersion': 'v1'                                       ,
                  'kind'      : 'Pod'                                      ,
                  'metadata'  : { 'name'      : pod_name                } ,
                  'spec'      : { 'containers': [{ 'image': image_name ,
                                                   'name' : image_name }] } }