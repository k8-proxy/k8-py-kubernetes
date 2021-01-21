import re
import warnings

from osbot_utils.fluent.Fluent_List import Fluent_List


def flist(target):
    return Fluent_List(target)

def list_set(target):
    return list(set(target))

def remove_multiple_spaces(target):
    return re.sub(' +', ' ', target)

def split_spaces(target):
    return remove_multiple_spaces(target).split(' ')

def ignore_warning__unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

def lower(target : str):
    if target:
        return target.lower()
    return ""