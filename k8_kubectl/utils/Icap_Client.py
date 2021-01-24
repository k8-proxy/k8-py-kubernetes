from datetime import time
from re import search

from osbot_utils.utils.Misc import remove, to_int, random_uuid, new_guid
from osbot_utils.utils.Files import path_combine, file_name, current_temp_folder, file_contents, \
    folder_create, create_folder_in_parent, file_copy, file_exists, file_md5

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
        return self.icap_run('-h').get('output')

    def get_processing_local_config(self, target_file_name):
        icap_processing_folder  = path_combine(current_temp_folder(), 'icap_processing_folder')
        icap_session            = new_guid()
        icap_session_folder     = path_combine(icap_processing_folder, icap_session)
        input_folder            = create_folder_in_parent(icap_session_folder, 'input' )
        output_folder           = create_folder_in_parent(icap_session_folder, 'output')
        input_file              = path_combine(input_folder , target_file_name)
        output_file             = path_combine(output_folder, target_file_name)
        return { "temp_folder"  : icap_session_folder ,
                 "session_id"   : icap_session        ,
                 "input_file"   : input_file          ,
                 "output_file"  : output_file         }

    def get_processing_docker_config(self, target_file_name):
        icap_folder    = '/icap_folder'
        input_folder   = path_combine(icap_folder  , 'input'         )
        output_folder  = path_combine(icap_folder  , 'output'        )
        input_file     = path_combine(input_folder , target_file_name)
        output_file    = path_combine(output_folder, target_file_name)
        return { "icap_folder"  : icap_folder ,
                 "input_file"   : input_file  ,
                 "output_file"  : output_file }

    def get_processing_config(self, target_file):
        target_file_name = file_name(target_file)
        config = {
            "target_file"   : target_file                                        ,
            "file_name"     : target_file_name                                   ,
            "local_config"  : self.get_processing_local_config (target_file_name),
            "docker_config" : self.get_processing_docker_config(target_file_name)
        }
        file_copy(source=target_file, destination=config.get('local_config').get('input_file'))
        return config

    def get_processing_result(self, config, icap_result):
        target_file  = config.get('local_config').get('input_file')
        rebuilt_file = config.get('local_config').get('output_file')

        processing_result = {
            "config"     : config                                   ,
            "icap_result": icap_result                              ,
            "md5s"       : { "target_file" : file_md5(target_file)  ,
                             "rebuilt_file": None                   }}

        if file_exists(rebuilt_file):
            processing_result.get("md5s")['rebuilt_file'] = file_md5(rebuilt_file)

        return processing_result

    def icap_process_file(self, target_ip, target_service, target_file):
        self.api_docker.set_debug()
        config                = self.get_processing_config(target_file)
        path_local_icap_data  = config.get('local_config').get('temp_folder')
        path_docker_icap_data = config.get('docker_config').get('icap_folder')
        input_file            = config.get('docker_config').get('input_file')
        output_file           = config.get('docker_config').get('output_file')
        docker_options        = { 'key':'-v' , 'value': f'{path_local_icap_data}:{path_docker_icap_data}'}
        command               = f'-i {target_ip} -s {target_service} -f {input_file} -o {output_file}'
        #command               = f'-i {target_ip}'
        icap_result           = self.icap_run(command, options=docker_options)
        processing_result     = self.get_processing_result(config, icap_result)
        return processing_result

    def icap_run(self, params=None, options=None):
        icap_params = f'time {self.icap_client_path} {params}'
        output      = self.api_docker.docker_run_bash(self.image_name,image_params=icap_params, options=options)
        console     = output.get('stdout') + output.get('stderr')
        return self.extract_time(console)

    def icap_run_command(self, command, options=None):
        output = self.api_docker.docker_run_bash(self.image_name, image_params=command,options=options)
        console = output.get('stdout') + output.get('stderr')
        return console


    def image_exists(self):
        return self.image_name in self.api_docker.images_names()

    def image_build(self):
        path = self.path_folder_with_docker_file()
        result = self.api_docker.image_build(path, self.image_repository, self.image_tag)
        return result.get('status') == 'ok'

    def path_folder_with_docker_file(self):
        return path_combine(__file__, '../../../docker/icap-client')




