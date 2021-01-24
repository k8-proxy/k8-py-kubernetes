from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp
from osbot_utils.utils.Files import file_md5, file_size
from osbot_utils.utils.Http                      import GET_bytes_to_file


class Files_To_Rebuild:

    def __init__(self):
        pass

    @cache_on_tmp(reload_data=False)
    def file_word_with_macros(self):
        file_name = "MacroRunCalculator.docm"
        url_file   = f'https://gw-demo-sample-files-eu1.s3-eu-west-1.amazonaws.com/{file_name}'
        file_local = GET_bytes_to_file(url_file)
        return {    "url_file"   : url_file ,
                    "local_path" : file_local ,
                    "file_name"  : 'MacroRunCalculator.docm'                           ,
                    "file_sizes" : { "original" : 39233                                ,
                                     "rebuilt"  : 31076                               },
                    "md5s"       : { "original" : '3c1aecd38ad1caf4d2f0571957def43a'   ,
                                     "rebuilt"  : 'ad57b0cf78fb135a23d6416169c38ed7'  }}