from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_utils.utils.Http import GET, GET_bytes_to_file


class Files_To_Rebuild:

    def __init__(self):
        pass

    @cache_on_self
    def file_word_with_macros(self):
        url_file = 'https://gw-demo-sample-files-eu1.s3-eu-west-1.amazonaws.com/MacroRunCalculator.docm'
        return GET_bytes_to_file(url_file)