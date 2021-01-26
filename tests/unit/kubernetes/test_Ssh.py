import os
from os import environ
from pprint import pprint
from unittest import TestCase

from dotenv import load_dotenv
from pytest import skip

from osbot_utils.utils.Files import file_not_exists

from k8_kubectl.kubernetes.Ssh import Ssh


class test_Ssh(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        self.ssh_config = {
            "user"    : os.environ.get('TEST_SSH_USER'  ),
            "server"  : os.environ.get('TEST_SSH_SERVER'),
            "ssh_key" : os.environ.get('TEST_SSH_KEY'   )
        }
        if file_not_exists(self.ssh_config.get('ssh_key')):
            skip('no ssh key in current test environemnt')
        self.ssh        = Ssh(ssh_config=self.ssh_config)
        print()

    # base methods
    def test_server_in_known_hosts(self):
        result = self.ssh.server_in_known_hosts()           # todo: add method to programatically add the server to the known_hosts file
        assert type(result) is bool

    def test_exec_ssh_command(self):
        assert self.ssh.exec_ssh_command('uname') == {'error': '', 'output': 'Linux\n', 'status': True}
        assert self.ssh.exec_ssh_command('aaaa' ) == {'error': 'bash: aaaa: command not found\n', 'output': '', 'status': False}

    def test_get_get_scp_params(self):
        source_file = 'source_file'
        target_file = 'target_file'
        ssh_params = self.ssh.get_scp_params(source_file, target_file)
        assert ssh_params == ['-i', self.ssh_config.get('ssh_key'),
                              f"{self.ssh_config.get('user')}@{self.ssh_config.get('server')}:{source_file}",
                              target_file]


    def test_get_get_ssh_params(self):
        ssh_params = self.ssh.get_ssh_params('aaa')
        assert ssh_params == ['-o StrictHostKeyChecking=no',
                              '-t', '-i', self.ssh_config.get('ssh_key'),
                              self.ssh_config.get('user') + '@' + self.ssh_config.get('server'),
                              'aaa']

    def test_exec(self):
        assert 'bin' in self.ssh.exec('cd /; ls')

    # helper methods

    def test_uname(self):
        assert self.ssh.uname() == 'Linux'

    # def create_pods(self, count):
    #     return self.ssh.exec(f'/home/ubuntu/icap-infrastructure/scripts/create_pod.sh {count}')
    #
    # def test_created_pod(self):
    #     self.create_pods(1)
    #     #assert 'bin' in self.ssh.exec('ls')
    # # helper methods: esxcli




