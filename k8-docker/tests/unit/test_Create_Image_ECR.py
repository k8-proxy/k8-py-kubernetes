from unittest import TestCase

from osbot_utils.utils.Json import json_loads, json_parse

from osbot_aws.AWS_Config import AWS_Config

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, file_exists, path_combine

from k8_docker.Create_Image_ECR import Create_Image_ECR


class test_Create_Image_ECR(TestCase):

    def setUp(self) -> None:
        #self.ecr_repository = 'osbot_unit_tests'
        self.image_name     = 'scratch'
        self._ = Create_Image_ECR(self.image_name)

    def test_build_image(self):
        assert self._.build_image() is True

    def test_create_repository(self):
        assert self._.create_repository() is True

    def test_image_repository(self):
        aws_config = AWS_Config()
        account_id = aws_config.aws_session_account_id()
        region     = aws_config.aws_session_region_name()
        assert self._.image_repository() == f'{account_id}.dkr.ecr.{region}.amazonaws.com/{self.image_name}'

    def test_ecr_login(self):
        assert self._.ecr_login() == {'IdentityToken': '', 'Status': 'Login Succeeded'}

    def test_path_image(self):
        assert folder_exists(self._.path_image())

    def test_path_images(self):
        assert folder_exists(self._.path_images())

    def test_push_image(self):
        result = self._.push_image()

        pprint(result)


    def test_run(self):
        result = Create_Image_ECR('ubuntu').run()
        pprint(result)