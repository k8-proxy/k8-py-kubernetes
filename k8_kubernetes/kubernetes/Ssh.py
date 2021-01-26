import os

from osbot_utils.utils.Files import temp_file, file_contents
from osbot_utils.utils.Process import exec_process

class Ssh:
    def __init__(self, ssh_config):
        self.ssh_config       = ssh_config
        self.last_exec_result = None
        self.verify_host      = False

    # base methods
    def exec(self, command):
        result = self.exec_ssh_command(command)
        output = result['output'].strip()
        return output

    def server_in_known_hosts(self):
        home        = os.environ.get('HOME')
        known_hosts = file_contents(f'{home}/.ssh/known_hosts')
        target      = self.ssh_config.get('server')
        return target in known_hosts


    def exec_scp_command(self, source_file, target_file=None):
        if target_file is None:
            target_file = temp_file()

        result = exec_process("scp", self.get_scp_params(source_file, target_file))
        if self.filter_exec_results(result).get('status'):
            return target_file

    def exec_ssh_command(self, command):
        result = exec_process("ssh", self.get_ssh_params(command))
        return self.filter_exec_results(result)


    def filter_exec_results(self, result):
        result['stderr'] = result['stderr'].replace('Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n', '') # Note: ok to ignore this error
        if result['stderr'] and not result['stdout']:                                                                                 # add an simple execution status
            result['status'] = False
        else:
            result['status'] = True

        result = {                                          # do this to improve result data structure and fields name
                    "error"  : result['stderr'],
                    "output" : result['stdout'],
                    "status" : result['status']
        }
        self.last_exec_result = result
        return result

    def get_scp_params(self, source_file, target_file):                                                # todo : refactor with get_ssh_params to reuse common components
        ssh_config = self.ssh_config
        ssh_params = []
        if self.verify_host:
            ssh_params.append('-o StrictHostKeyChecking=no')
        ssh_params.extend(['-i', ssh_config.get('ssh_key')]                                    )       # add ssh key to login as
        ssh_params.append(f"{ssh_config.get('user')}@{ssh_config.get('server')}:{source_file}" )       # add target host name and source file
        ssh_params.append(target_file                                                          )       # add target file
        return ssh_params

    def get_ssh_params(self, command):
        ssh_params = []
        if self.verify_host is False:
           ssh_params.append('-o StrictHostKeyChecking=no')
        ssh_params.append('-t'                                                              )       # -t "Force pseudo-tty allocation" note: Using -tt will make the returned data to be ascii encoded which is not what we want
        ssh_params.extend(['-i', self.ssh_config.get('ssh_key'                            )])       # add ssh key to login as
        ssh_params.append(f"{self.ssh_config.get('user')}@{self.ssh_config.get('server')}"  )       # add target host name
        ssh_params.append(command                                                           )       # add command to execute
        return ssh_params

    # helper methods:
    def cat  (self, path      ): return self.exec(f'cat {path}'           )
    def df   (self, path      ): return self.exec(f'df {path}'            )
    def du   (self, path      ): return self.exec(f'du - sh {path}'       )
    def ls   (self, path      ): return self.exec(f'ls {path}'            )
    def tail (self, path, size): return self.exec(f'tail -n {size} {path}')
    def uname(self            ): return self.exec('uname'                 )




