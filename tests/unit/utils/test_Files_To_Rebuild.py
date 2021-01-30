from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import file_exists

from k8_kubernetes.utils.Files_To_Rebuild import Files_To_Rebuild


class test_Files_To_Rebuild(TestCase):

    def setUp(self) -> None:
        self.files_to_rebuild = Files_To_Rebuild()
        print()

    def test_file_word_with_macros(self):
        target_file = self.files_to_rebuild.file_word_with_macros()

        assert file_exists(target_file.get('local_path'))



