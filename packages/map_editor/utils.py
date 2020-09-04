from collections import Counter
from os import listdir
from os.path import join
import logging

logger = logging.getLogger('root')


def count_elements(data): return Counter(data)


def get_list_dir(dir_path):
    try:
        entries = listdir(dir_path)
        return entries
    except FileNotFoundError as e:
        logger.warning(e)
        return []


def get_list_dir_with_path(dir_path): return [(filename, join(dir_path, filename)) for filename in get_list_dir(dir_path)]


def get_available_translations(lang_dir_path): return {filename[len('lang_'):-len('.qm')]: path  for filename, path in get_list_dir_with_path(lang_dir_path)}
