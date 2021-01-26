from unittest                           import TestCase
from osbot_aws.apis.Lambda              import Lambda
from osbot_aws.deploy.Deploy_Lambda     import Deploy_Lambda
from k8_kubernetes.lambdas.hello_world  import run

class test_hello_world(TestCase):
    def setUp(self) -> None:
        self.handler     = run
        self.deploy      = Deploy_Lambda(self.handler)
        self.lambda_name = self.deploy.lambda_name()

    def test_invoke_directly(self):
        assert self.handler.__module__          == self.lambda_name
        assert self.handler({}                ) == 'From lambda code, hello None'
        assert self.handler({'name' : 'world'}) == 'From lambda code, hello world'

    def test_deploy_lambda(self):
        assert self.deploy.deploy() is True

    def test_invoke_lambda__using_k8_lambda_class(self):
        assert self.deploy.invoke() == 'From lambda code, hello None'

    def test_invoke_lambda__using_lambda_class(self):
        event = {'name' : 'world'}
        assert Lambda(self.lambda_name).invoke(event) == 'From lambda code, hello world'