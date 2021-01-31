from osbot_aws.AWS_Config import AWS_Config

from osbot_aws.apis.ECR import ECR
from osbot_docker.API_Docker import API_Docker
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, file_write
from osbot_utils.utils.Misc import base64_to_str


class Create_Image_ECR:

    def __init__(self, ecr_repository, image_name, image_tag='latest'):
        self.api_docker      = API_Docker()
        self.ecr             = ECR()
        self.aws_config      = AWS_Config()
        self.ecr_repository  = ecr_repository
        self.image_name      = image_name
        self.image_tag       = image_tag

    def build_image(self):
        repository = self.image_name
        tag        = self.image_tag
        result     = self.api_docker.image_build(path=self.path_image(), repository=repository, tag=tag)
        return result.get('status') == 'ok'


    def ecr_login(self):
        auth_data = self.ecr.authorization_token()
        return self.api_docker.registry_login(registry=auth_data.get('registry'),
                                              username=auth_data.get('username'),
                                              password=auth_data.get('password'))

    def path_image(self):
        return path_combine(self.path_images(), self.image_name)

    def path_images(self):
        return path_combine(__file__, '../../images')

