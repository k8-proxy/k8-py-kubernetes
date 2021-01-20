import os
from pprint import pprint
from unittest import TestCase

from osbot_aws.apis.Session import Session

os.environ['AWS_PROFILE_NAME'  ] = "785217600689_AdministratorAccess"
os.environ['AWS_DEFAULT_REGION'] = "eu-west-3"


class OSBot_AWS__SSM:

    def __init__(self):
        self.client = Session().client('ssm')

    def command_run(self, instance_id, command):
        resp = self.client.send_command(
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': [command]},
            InstanceIds=[instance_id],
        )
        return resp

    def commands_list(self):
        return self.client.list_commands()




class test_OSBot_AWS__SSM(TestCase):

    def setUp(self):
        self._ = OSBot_AWS__SSM()
        print()

    def test_command_run(self):
        instance_id = 'i-01df957fb4f99888e'
        command     = 'pwd'
        result = self._.command_run(instance_id, command)

        pprint(result)

    def test_commands_list(self):
        result = self._.commands_list()
        pprint(result)




