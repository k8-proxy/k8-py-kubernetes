from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp
from osbot_utils.utils.Http                      import GET_bytes_to_file


class Files_To_Rebuild:

    def __init__(self):
        pass

    @cache_on_tmp()
    def file_word_with_macros(self):
        url_file = 'https://gw-demo-sample-files-eu1.s3-eu-west-1.amazonaws.com/MacroRunCalculator.docm'
        return GET_bytes_to_file(url_file)