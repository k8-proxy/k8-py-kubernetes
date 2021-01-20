import os
from pprint import pprint
from unittest import TestCase

from osbot_aws.apis.Ec2 import Ec2
from osbot_aws.apis.S3 import S3
from osbot_aws.apis.Session import Session

os.environ['AWS_PROFILE_NAME'  ] = "785217600689_AdministratorAccess"
os.environ['AWS_DEFAULT_REGION'] = "eu-west-3"

class Start_ICAP_Server_AWS:
    def __init__(self):
        self.ec2 = Ec2()


    def ec2_servers(self):
        return self.ec2.instances_details()


class test_Start_ICAP_Server_AWS(TestCase):

    def setUp(self):
        self._ = Start_ICAP_Server_AWS()
        print()

    def test_ec2_servers(self):
        result = self._.ec2_servers()
        pprint(result)
