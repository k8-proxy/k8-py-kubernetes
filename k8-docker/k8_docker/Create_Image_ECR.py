from osbot_aws.AWS_Config import AWS_Config

from osbot_aws.apis.ECR import ECR
from osbot_docker.API_Docker import API_Docker
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, file_write
from osbot_utils.utils.Misc import base64_to_str


class Create_Image_ECR:

    def __init__(self, image_name, image_tag='latest'):
        self.api_docker      = API_Docker()
        self.ecr             = ECR()
        self.aws_config      = AWS_Config()
        self.image_name      = image_name
        self.image_tag       = image_tag

    def build_image(self):
        repository = self.image_repository()
        tag        = self.image_tag
        result     = self.api_docker.image_build(path=self.path_image(), repository=repository, tag=tag)
        return result.get('status') == 'ok'

    def create_repository(self):
        self.ecr.repository_create(self.image_name)
        return self.ecr.repository_exists(self.image_name)

    def image_repository(self):
        account_id = self.aws_config.aws_session_account_id()
        region     = self.aws_config.aws_session_region_name()
        return f'{account_id}.dkr.ecr.{region}.amazonaws.com/{self.image_name}'

    def ecr_login(self):
        auth_data = self.ecr.authorization_token()
        return self.api_docker.registry_login(registry=auth_data.get('registry'),
                                              username=auth_data.get('username'),
                                              password=auth_data.get('password'))


    def path_image(self):
        return path_combine(self.path_images(), self.image_name)

    def path_images(self):
        return path_combine(__file__, '../../images')

    def push_image(self):
        return self.api_docker.image_push(self.image_repository(), self.image_tag)


    def run(self):
        create_repository = self.create_repository   ()
        ecr_login         = self.ecr_login           ()
        build_image       = self.build_image         ()
        push_image        = self.push_image         ()
        return {'create_repository' : create_repository,
                'ecr_login'         : ecr_login        ,
                'build_image'       : build_image      ,
                'push_image'        : push_image       }
