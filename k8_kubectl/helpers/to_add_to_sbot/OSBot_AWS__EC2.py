import os
from pprint import pprint
from unittest import TestCase

from osbot_aws.apis.Ec2 import Ec2

os.environ['AWS_PROFILE_NAME'  ] = "785217600689_AdministratorAccess"
os.environ['AWS_DEFAULT_REGION'] = "eu-west-3"


class OSBot_AWS__EC2:

    def __init__(self):
        self.ec2    = Ec2()
        self.client = self.ec2.ec2

    def instance_create(self, image_id, instance_type='t2.micro', iam_instance_profile=None):
        kwargs = {
            "ImageId"      : image_id,
            "InstanceType" : instance_type,
            "MaxCount"     : 1,
            "MinCount"     : 1,
            #"KeyName"      : "KeyName",
            "UserData"     : "UserData",
            "AdditionalInfo": "AdditionalInfo",
            "TagSpecifications": [{ "ResourceType" : "instance",
                                    "Tags" : [ { 'Key': 'Name', 'Value': 'from python' }]}]

        }
        if iam_instance_profile: kwargs["IamInstanceProfile"] = iam_instance_profile
        result = self.client.run_instances(**kwargs)
        instance = result.get('Instances')[0]
        return  instance.get('InstanceId')

    def instance_details(self, instance_id):
        result = self.client.describe_instances(InstanceIds=[instance_id])
        return result.get('Reservations')[0].get('Instances')[0]

    def instance_delete(self, instance_id):
        return self.client.terminate_instances(InstanceIds=[instance_id])

    def wait_for(self, waiter_type, instance_id):
        waiter = self.client.get_waiter('instance_running')
        return waiter.wait(InstanceIds=[instance_id])

    def wait_for_instance_status_ok(self, instance_id):
        return self.wait_for('instance_status_ok', instance_id)

    def wait_for_instance_running(self, instance_id):
        return self.wait_for('instance_running', instance_id)


class test_OSBOT_AWS__EC2(TestCase):

    def setUp(self) -> None:
        self._             = OSBot_AWS__EC2()
        self.image_id      = 'ami-00798d7180f25aac2'  # amazon linux 2
        print()

    def test_create_instance(self):
        instance_id = self._.instance_create(self.image_id)         # todo: add tests with different instant_types
        assert instance_id in self._.ec2.instances_details()
        result_delete = self._.instance_delete(instance_id)
        terminating_instance = result_delete.get('TerminatingInstances')[0]
        assert terminating_instance.get('CurrentState') == {'Code': 32, 'Name': 'shutting-down'}
        assert terminating_instance.get('InstanceId'  ) == instance_id

    def test_instance_details(self):
        instance_id = "i-091dddd63738f20c2"
        result = self._.instance_details(instance_id)
        pprint(result)

    def test_wait_for_instance_running(self):
        instance_id = self._.instance_create(self.image_id)
        result = self._.wait_for_instance_running(instance_id)
        #pprint(result)                             # todo: add check for running state
        #pprint(self._.ec2.instances_details())
        self._.instance_delete(instance_id)

    def test_wait_for_instance_status_ok(self):
        instance_id = self._.instance_create(self.image_id)
        result = self._.wait_for_instance_status_ok(instance_id)
        #pprint(result)
        #pprint(self._.ec2.instances_details())     # todo: add check for running state
        self._.instance_delete(instance_id)


    def test___misc(self):
        iam_instance_profile = { "Name": 'AmazonSSMRoleForInstancesQuickSetup'}
        instance_id = self._.instance_create(self.image_id, iam_instance_profile = iam_instance_profile)
        pprint(instance_id)





