from pprint import pprint
from unittest import TestCase

from k8_kubectl.utils.Files_To_Rebuild import Files_To_Rebuild
from osbot_utils.utils.Files import folder_exists, path_combine, file_exists, create_temp_file, file_name, file_md5, \
    file_sha256

from k8_kubectl.utils.Icap_Client import Icap_Client


class test_Icap_Client(TestCase):

    def setUp(self) -> None:
        self.icap_client    = Icap_Client()
        self.target_ip      = '34.242.162.186'
        self.target_service = 'gw_rebuild'
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

    def test_extract_time(self):
        text_before = "AAAAA before"
        time_text = "\nreal\t0m0.005s\nuser\t0m0.002s\nsys\t0m0.003s\n"
        output = text_before + time_text
        result  = self.icap_client.extract_time(output)
        assert result.get('output') == text_before
        assert '0m0.00' in result.get('time_str')

    def test_icap_echo(self):
        #ip = "20.67.220.25"
        ip = '34.244.46.139'

        assert 'ICAP server' in self.icap_client.icap_echo(ip).get('output')

    def test_icap_echo_service(self):
            # ip = "20.67.220.25"
            ip = '34.244.46.139'
            service_name = 'gw_rebuild'
            service_echo = 'Glasswall Rebuild service'
            assert service_echo in self.icap_client.icap_echo_service(ip,service_name).get('output')

    def test_icap_help(self):
        assert '-V \t\t\t: Print version and exits\n' in self.icap_client.icap_help()

    def test_icap_process_file(self):
        file_to_process     = Files_To_Rebuild().file_word_with_macros()
        file_to_process_md5 = file_md5(file_to_process)
        result = self.icap_client.icap_process_file(self.target_ip, self.target_service, file_to_process)
        print()
        pprint(result)

    def test_icap_run(self):
        icap_params = ''
        result = self.icap_client.icap_run(icap_params)
        assert result.get('output') == "Connection to 'localhost:1344' failed/timedout\nFailed to connect to icap server.....\n"
        assert result.get('time_object').microsecond < 100 * 1000 # less than 100ms

    def test_image_build(self):
        assert self.icap_client.image_build() is True

    def test_image_exists(self):
        assert self.icap_client.image_exists() is True

    def test_path_folder_with_docker_file(self):
        path       = self.icap_client.path_folder_with_docker_file()
        dockerfile = path_combine(path, 'Dockerfile')
        assert folder_exists(path)
        assert file_exists  (dockerfile)



