import os

from dotenv import load_dotenv

from k8_kubernetes.kubernetes.Ssh import Ssh
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class EC2_Server:
    def __init__(self, server_ip):
        self.server_ip = server_ip

    @cache_on_self
    def ssh_config(self):
        load_dotenv()
        return {"server" : self.server_ip,
                "ssh_key": os.environ.get('SSH_KEY'),
                "user"   : os.environ.get('SSH_USER')}

    def ssh(self):
        return Ssh(self.ssh_config())

    def exec_command(self, command):
        return self.ssh().exec_ssh_command(command)

    def df(self, path):
        return self.ssh().df(path)