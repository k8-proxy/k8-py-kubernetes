from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, file_exists, path_combine

from k8_docker.Create_Image_ECR import Create_Image_ECR


class test_Create_Image_ECR(TestCase):

    def setUp(self) -> None:
        self.ecr_repository = 'osbot_unit_tests'
        self.image_name     = 'scratch'
        self._ = Create_Image_ECR(self.ecr_repository, self.image_name)

    def test_build_image(self):
        assert self._.build_image() is True

    def test_ecr_login(self):
        assert self._.ecr_login() == {'IdentityToken': '', 'Status': 'Login Succeeded'}

    def test_path_image(self):
        assert folder_exists(self._.path_image())

    def test_path_images(self):
        assert folder_exists(self._.path_images())
