import os
import subprocess
from pprint import pprint
from unittest import TestCase

from dotenv import load_dotenv

from k8_kubernetes.utils.Files_To_Rebuild import Files_To_Rebuild
from osbot_utils.utils.Files import folder_exists, path_combine, file_exists, create_temp_file

from k8_kubernetes.utils.Icap_Client import Icap_Client


class test_Icap_Client(TestCase):

    def setUp(self) -> None:
        load_dotenv()                                                       # todo: write helper function to get a valid test server
        self.icap_client    = Icap_Client()
        self.target_ip      = os.environ.get('TEST_ICAP_SERVER')            # todo: write helper function to get a valid test server
        self.target_service = os.environ.get('TEST_ICAP_SERVICE')
        print()

    def test_get_processing_config(self):
        temp_file = create_temp_file()
        config    = self.icap_client.get_processing_config(temp_file)
        assert file_exists(config.get('local_config').get('input_file'))    # todo: rewire asserts below

        # temp_file_name = file_name(temp_file)
        # icap_session_folder = self.icap_client.create_temp_processing_file_folder(temp_file)
        # assert folder_exists(icap_session_folder)
        # assert folder_exists(path_combine(icap_session_folder, 'input'))
        # assert folder_exists(path_combine(icap_session_folder, 'output'))
        # assert folder_exists(path_combine(icap_session_folder, f'input/{temp_file_name}'))

    def test_extract_headers(self):
        output = (   'OK done with options!\n'
                     'ICAP server:34.242.162.186, ip:172.17.0.3, port:1344\n'
                     '\n'
                     'Preview:1024 keepalive:1,allow204:0\n'
                     'OK allocating request going to send request\n'
                     'Allocate a new entity of type 1\n'
                     'Allocate a new entity of type 3\n'
                     'Going to add 4 response headers\n'
                     'Add resp header: HTTP/1.0 200 OK\n'
                     'Add resp header: Date: Sun Jan 24 21:24:29 2021\n'
                     'Add resp header: Last-Modified: Sun Jan 24 21:24:29 2021\n'
                     'Add resp header: Content-Length: 39233\n'
                     'Preview response was with status: 100 \n'
                     'Response was with status:200 \n'
                     'Get entity from trash....\n'
                     'Get entity from trash....\n'
                     'OK reading headers, going to read body\n'
                     '\n'
                     'ICAP HEADERS:\n'
                     '\tICAP/1.0 200 OK\n'
                     '\tServer: C-ICAP/0.5.7\n'
                     '\tConnection: keep-alive\n'
                     '\tISTag: CI0001-2.1.1\n'
                     '\tEncapsulated: res-hdr=0, res-body=266\n'
                     '\n'
                     'RESPMOD HEADERS:\n'
                     '\tHTTP/1.0 200 OK\n'
                     '\tDate: Sun Jan 24 21:24:29 2021\n'
                     '\tLast-Modified: Sun Jan 24 21:24:29 2021\n'
                     '\tContent-Length: 31076\n'
                     '\tX-Adaptation-File-Id: f1f86f79-fce1-4f6b-9453-d3283dc2eba4\n'
                     '\tVia: ICAP/1.0 mvp-icap-service-7bdcd685b7-j2cn5 (C-ICAP/0.5.7 Glasswall '
                     'Rebuild service )\n'
                     '\n'
                     'Done\n'
                     '\n'
                     'real\t0m6.113s\n'
                     'user\t0m0.003s\n'
                     'sys\t0m0.008s\n')

        icap_headers = self.icap_client.extract_icap_headers(output)
        assert icap_headers['k8_container'] == 'mvp-icap-service-7bdcd685b7-j2cn5'

    def test_extract_time(self):
        text_before = "AAAAA before"
        time_text = "\nreal\t0m0.005s\nuser\t0m0.002s\nsys\t0m0.003s\n"
        output = text_before + time_text
        result  = self.icap_client.extract_time(output)
        assert '0m0.00' in result.get('time_str')

    def test_icap_echo(self):
        result = self.icap_client.icap_echo(self.target_ip)
        assert 'ICAP server' in result.get('docker_run').get('stderr')
        assert result.get('icap_headers').get('status_code' ) == '200'
        assert result.get('icap_headers').get('schema'      ) == 'ICAP'
        assert result.get('icap_headers').get('Methods'     ) == 'RESPMOD, REQMOD'

    def test_icap_echo_service(self):
            service_name = 'gw_rebuild'
            service_echo = 'Glasswall Rebuild service'
            output = self.icap_client.icap_echo_service(self.target_ip,service_name)
            assert service_echo in output.get('icap_headers').get('Service')

    def test_icap_help(self):
        assert '-V \t\t\t: Print version and exits\n' in self.icap_client.icap_help()

    def test_icap_process_file(self):
        file_to_rebuild    = Files_To_Rebuild().file_word_with_macros()
        file_to_process    = file_to_rebuild.get('local_path')
        expected_file_md5  = file_to_rebuild.get('md5s'      ).get('rebuilt')
        expected_file_size = file_to_rebuild.get('file_sizes').get('rebuilt')
        result             = self.icap_client.icap_process_file(self.target_ip, self.target_service, file_to_process)
        config             = result.get('config')
        original_file      = config.get('local_config').get('input_file')
        rebuilt_file       = config.get('local_config').get('output_file')

        assert file_exists(original_file)
        assert file_exists(rebuilt_file)

        assert result.get('file_sizes').get('rebuilt') == expected_file_size
        assert result.get('md5s'      ).get('rebuilt') == expected_file_md5
        pprint(result)

    def test_icap_process_file__with_timeout(self):
        file_to_rebuild = Files_To_Rebuild().file_word_with_macros()
        file_to_process = file_to_rebuild.get('local_path')
        self.icap_client.set_icap_timeout(0.5)
        result = self.icap_client.icap_process_file(self.target_ip, self.target_service, file_to_process)
        docker_run = result.get('icap_result').get('docker_run')
        assert docker_run.get('status') == 'error'
        assert type(docker_run.get('error')) == subprocess.TimeoutExpired

    def test_icap_run(self):
        icap_params = ''
        result      = self.icap_client.icap_run(icap_params)
        assert "Connection to 'localhost:1344' failed/timedout" in result.get('docker_run').get('stderr')
        assert result.get('duration').get('time_date').microsecond < 100 * 1000 # less than 100ms

    def test_image_build(self):
        assert self.icap_client.image_build() is True

    def test_image_exists(self):
        assert self.icap_client.image_exists() is True

    def test_path_folder_with_docker_file(self):
        path       = self.icap_client.path_folder_with_docker_file()
        dockerfile = path_combine(path, 'Dockerfile')
        assert folder_exists(path)
        assert file_exists  (dockerfile)




