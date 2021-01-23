import base64
import csv
import os
import re
import warnings
from io import StringIO
from dotenv import load_dotenv
from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.fluent.Fluent_Dict import Fluent_Dict
from osbot_utils.utils.Files import file_open
from osbot_utils.utils.Http import GET, port_is_open
from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes
from osbot_utils.fluent.Fluent_List import Fluent_List

# todo: add units tests to these methods when refactoring to OSBot_Utils project
def env_value(var_name):
    return env_vars().get(var_name, None)

# requires python-dotenv to be added to OSBot_Utils requirements.txt
def env_vars():
    """
    reload data from .env file and return dictionary with current environment variables
    :return:
    """
    load_dotenv()
    vars = os.environ
    data = {}
    for key in vars:
        data[key] = vars[key]
    return data

def env_vars_list():
    return list_set(env_vars())

def flist(target):
    return Fluent_List(target)

@index_by
@group_by
def load_csv_from_file(file_path, delimiter=','):
    iterable = file_open(file_path)
    return load_csv_from_iterable(iterable, delimiter=delimiter)

@index_by
@group_by
def load_csv_from_str(csv_data, delimiter=','):
    iterable = StringIO(csv_data)
    return load_csv_from_iterable(iterable, delimiter=delimiter)

@index_by
@group_by
def load_csv_from_url(url, headers, delimiter=','):
    csv_data = GET(url=url, headers=headers)
    return load_csv_from_str(csv_data=csv_data, delimiter=delimiter)


def list_index_by(values, index_by):
    results = {}
    for item in values:
        results[item.get(index_by)] = item
    return Fluent_Dict(results)

def list_group_by(values, group_by):
    results = {}
    for item in values:
        value = item.get(group_by)
        if results.get(value) is None: results[value] = []
        results[value].append(item)
    return results

def list_set(target):
    return sorted(list(set(target)))

@index_by
@group_by
def load_csv_from_iterable(iterable, delimiter=','):
    csv_reader = csv.DictReader(iterable, delimiter=delimiter)
    return [row for row in csv_reader]

def base64_to_str(target):
    return bytes_to_str(base64_to_bytes(target))

def bytes_to_str(target, encoding='ascii'):
    return target.decode(encoding=encoding)

def ignore_warning__unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

def lower(target : str):
    if target:
        return target.lower()
    return ""

def remove_multiple_spaces(target):
    return re.sub(' +', ' ', target)

def str_to_base64(target):
    return bytes_to_base64(str_to_bytes(target))

def str_to_bytes(target):
    return target.encode()

def split_spaces(target):
    return remove_multiple_spaces(target).split(' ')


def is_port_open(host, port, timeout=0.5):
    return port_is_open(host=host, port=port, timeout=timeout)
