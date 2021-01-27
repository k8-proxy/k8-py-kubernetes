from pprint                              import pprint
from unittest                            import TestCase
from osbot_utils.utils.Misc              import trim
from osbot_aws.apis.Lambda               import Lambda
from osbot_aws.deploy.Deploy_Lambda      import Deploy_Lambda
from k8_kubernetes.lambdas.exec_commands import run

class test_hello_world(TestCase):
    def setUp(self) -> None:
        self.handler       = run                                        # link to the run method in exec_commands.py
        self.deploy_lambda = Deploy_Lambda(self.handler)                # use OSBot_AWS helper class for deploying lambdas
        self.aws_lambda    = Lambda(self.deploy_lambda.lambda_name())   # use OSBot_Lambda helper class to invoke lambdas
        print()

    def update_lambda(self):
        self.deploy_lambda.add_osbot_utils()                            # adding the osbot_utils package to the source code
        self.deploy_lambda.deploy()                                     # create or update lambda function

    def exec_in_lambda(self, command, params=None):
        #self.update_lambda()
        event = {'command': command, 'params' : params }
        result = self.aws_lambda.invoke(event)
        return trim(result.get('error' )) + \
               trim(result.get('stderr')) + \
               trim(result.get('stdout'))

    def test_invoke_lambda(self):
        result = self.exec_in_lambda('ls','/bin')
        print(result)


    def test_ip     (self):  assert self.exec_in_lambda('ip'     ) == "[Errno 2] No such file or directory: 'ip'"
    def test_ls     (self):  assert self.exec_in_lambda('ls'     ) == 'dotenv\nk8_kubernetes\nosbot_utils'
    def test_ls_root(self):  assert self.exec_in_lambda('ls', '/') == ('bin\nboot\ndev\netc\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar')
    def test_pwd    (self):  assert self.exec_in_lambda('pwd'    ) == '/var/task'
    def test_uname  (self):  assert self.exec_in_lambda('uname'  ) == 'Linux'
