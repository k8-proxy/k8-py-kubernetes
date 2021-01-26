from pprint                              import pprint
from unittest                            import TestCase
from osbot_aws.apis.Lambda               import Lambda
from osbot_aws.deploy.Deploy_Lambda      import Deploy_Lambda
from k8_kubernetes.lambdas.exec_commands import run

class test_hello_world(TestCase):
    def setUp(self) -> None:
        self.handler       = run                                        # link to the run method in exec_commands.py
        self.deploy_lambda = Deploy_Lambda(self.handler)                # use OSBot_AWS helper class for deploying lambdas
        self.aws_lambda    = Lambda(self.deploy_lambda.lambda_name())   # use OSBot_Lambda helper class to invoke lambdas
        print()

    def _deploy_lambda(self):
        self.deploy_lambda.deploy()                                     # create or update lambda function

    def test_invoke_lambda(self):
        self._deploy_lambda()                                           # use when making changes to the lambda code
        event = {}                                                      # payload to send to lambda function
        result = self.aws_lambda.invoke(event)                          # invoke function in AWS
        pprint(result)                                                  # print value returned by the function