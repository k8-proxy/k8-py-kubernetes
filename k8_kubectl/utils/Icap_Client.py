from datetime import time
from re import search

from osbot_utils.utils.Misc import remove, to_int
from osbot_utils.utils.Files import path_combine

from osbot_docker.API_Docker import API_Docker


class Icap_Client:

    def __init__(self):
        self.image_repository = "k8_kubectl__icap_client"
        self.image_tag        = "latest"
        self.image_name       = f"{self.image_repository}:{self.image_tag}"
        self.icap_client_path = '/usr/local/c-icap/bin/c-icap-client'
        self.api_docker = API_Docker()

    def extract_time(self,output):
        regex_time_data = '\nreal\t(.*)\nuser\t(.*)\nsys\t(.*)\n'
        regex_time      = '(.*)m(.*)\.(.*)s'
        match_time_data = search(regex_time_data, output)
        time_str        = ''
        time_object     = ''
        if match_time_data:
            time_str      = match_time_data.group(1)
            match_time    = search(regex_time, time_str)
            minutes       = to_int(match_time.group(1))
            seconds       = to_int(match_time.group(2))
            micro_seconds = to_int(match_time.group(3)) * 1000
            time_object   = time(0, minutes, seconds, micro_seconds)
            output        = remove(output, match_time_data.group(0))
        return {"output": output, "time_str": time_str, 'time_object': time_object}

    def icap_echo(self, icap_server):
        icap_params =  f'-i {icap_server} '   #-s gw_rebuild
        return self.icap_run(icap_params)

    def icap_echo_service(self, icap_server, service_name):
        icap_params =  f'-i {icap_server} -s {service_name}'
        return self.icap_run(icap_params)

    def icap_help(self):
        return self.icap_run('-h')

    def icap_process_file(self):
        pass

    def icap_run(self, params=None):
        icap_params = f'time {self.icap_client_path} {params}'
        output      = self.api_docker.docker_run_bash(self.image_name, icap_params)
        console     = output.get('stdout') + output.get('stderr')
        return self.extract_time(console)

    def image_exists(self):
        return self.image_name in self.api_docker.images_names()

    def image_build(self):
        path = self.path_folder_with_docker_file()
        result = self.api_docker.image_build(path, self.image_repository, self.image_tag)
        return result.get('status') == 'ok'

    def path_folder_with_docker_file(self):
        return path_combine(__file__, '../../../docker/icap-client')




