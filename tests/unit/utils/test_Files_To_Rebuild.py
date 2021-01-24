from pprint import pprint
from unittest import TestCase

from k8_kubectl.utils.Files_To_Rebuild import Files_To_Rebuild


class test_Files_To_Rebuild(TestCase):

    def setUp(self) -> None:
        self.files_to_rebuild = Files_To_Rebuild()
        print()

    def test_file_word_with_macros(self):
        file = self.files_to_rebuild.file_word_with_macros()

        pprint(file)