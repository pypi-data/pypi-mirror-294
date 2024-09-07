import json
from io import open
import os
import numpy as np
from os.path import basename
from prettytable import PrettyTable
import logging
from pathlib import Path
from itertools import compress
import pandas as pd
from collections.abc import MutableMapping
import astropy.units as u


def flatten_dictionary(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dictionary(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if np.any([isinstance(_v, MutableMapping) for _v in v]):
                for _i, _v in enumerate(v):
                    extra_sep = '' if len(v) == 1 else sep + str(_i)
                    if isinstance(_v, MutableMapping):
                        items.extend(flatten_dictionary(_v, new_key + extra_sep, sep=sep).items())
                    else:
                        items.append((new_key, _v))
            else:
                if len(v) == 1:
                    items.append((new_key, v[0]))
                else:
                    items.append((new_key, v))
        else:
            items.append((new_key, v))
    return dict(items)


class DataLinks(object):
    """
    This class is used to link the parameters associated to each data file as well as the initial and end times to
    to be read
    """

    def __init__(self,
                 parameters: dict = {},
                 parameters_file: str = None,
                 parameters_date: str = '',
                 data_file: str = None,
                 data_header: object = None,
                 data_date: str = '',
                 ini_time=0.0,
                 end_time=None,
                 meta_data: list = [],
                 label: str = None):
        self.parameters_file = parameters_file
        self.parameters_date = parameters_date
        self.data_file = data_file
        self.data_date = data_date
        self.data_header = data_header
        self.ini_time = ini_time
        self.end_time = end_time
        self.measurement_parameters = parameters
        self.meta_data = meta_data
        self.label = label


def match_keywords(key_words: [str] = None, word: str = None, deep_match=False):
    """
    This function matches a list of keywords in an string.
    :param key_words: string list of key words to be matched
    :param word: string variable where words are to be found
    :param deep_match: if True, all keywords must be present to return True
    :return: Bool variable indicating if a match was obtained
    """
    _found = False
    if deep_match:
        if key_words is not None and np.all([_key_word in word for _key_word in key_words]):
            _found = True
    else:
        if key_words is not None and any(
                [_key_word in word for _key_word in key_words]):
            _found = True
    return _found


def get_files_and_meta_files(measurement_path: str = '',
                             filter_key_words_in_path: [str] = None,
                             exclude_key_words_in_path: [str] = None,
                             filter_key_words_in_file: [str] = None,
                             exclude_key_words_in_file: [str] = None,
                             deep_match_in_filter_path: bool = True,
                             deep_match_in_filter_file: bool = True,
                             deep_match_in_exclude_path: bool = True,
                             deep_match_in_exclude_file: bool = True,
                             ignore_meta_file: bool = False,
                             file_types: [str] = ['xlsx'],
                             meta_file_extension: str = 'json',
                             ) -> pd.DataFrame:
    """
    This function search for files which extension is defined by file_types and meta_files associated to each file.
    Each file will be associated to the meta_file in the output dataframe.
    This is, in order to pair a bdf to json file both should have the same name.
    The result is a list of DataLinks object, containing the information that links both files.
    If the meta_file_type is a json file, the json file will be parsed as a dictionary in the DataLinks parameters and
    also in the output dataframe. In this way, the data to be processed can be manipulated using pandas
    functionalities.
    :param measurement_path: the root path to search for pairs of files
    :param filter_key_words_in_path: if provided, the return list will only contain DataLinks object whose paths does
    include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param exclude_key_words_in_path: if provided, the return list will only contain DataLinks object whose paths does
     not include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param filter_key_words_in_file: if provided, the return list will only contain DataLinks object whose file name
     does include
    the filter_key_words_in_file. This is useful to process entire folders with different conditions
    :param exclude_key_words_in_file: if provided, the return list will only contain DataLinks object whose file name
    does not include
    the exclude_key_words_in_path. This is useful to process entire folders with different conditions
    :param deep_match_in_filter_path: if True, all keywords must be present to return True
    :param deep_match_in_filter_file: if True, all keywords must be present to return True
    :param deep_match_in_exclude_path: if True, all keywords must be present to return True
    :param deep_match_in_exclude_file: if True, all keywords must be present to return True
    :param meta_file_extension: if True it will not care whether json file is present or not
    :param file_types: a list of strings indicating the file types to be found, e.g. .bdf, .edf, .txt, .json, etcetera
    The time stamps indicating the beginning and end of eeach block will be passed in  time the ini_time and
    end_time of the DataLinks class.
    :return: a Pandas data frame with DataLinks objects which contain the information linking the files
    """
    data_files = []
    for files in file_types:
        data_files.extend(Path(measurement_path).glob('**/*.{:}'.format(files)))

    # avoid hidden folders
    _to_keep = []
    for _file in data_files:
        _to_keep.append(any([_parts == '.' for _parts in os.path.normpath(str(_file)).split(os.sep)]) is False)
    data_files = list(compress(data_files, _to_keep))

    par_out = pd.DataFrame()
    for i, _full_file_name in enumerate(data_files):
        _data_file_name = _full_file_name.name
        _meta_file_path = ''
        if meta_file_extension:
            _meta_file_path = _data_file_name + '.{:}'.format(meta_file_extension)
        if filter_key_words_in_path is not None and not match_keywords(
                filter_key_words_in_path, str(_full_file_name),
                deep_match=deep_match_in_filter_path):
            continue
        if exclude_key_words_in_path is not None and match_keywords(
                exclude_key_words_in_path, str(_full_file_name),
                deep_match=deep_match_in_exclude_path):
            print('ignoring file: {:}'.format(str(_full_file_name)))
            continue

        if filter_key_words_in_file is not None and \
                not (match_keywords(filter_key_words_in_file, _data_file_name, deep_match=deep_match_in_filter_file) and
                     match_keywords(filter_key_words_in_file, _meta_file_path, deep_match=deep_match_in_filter_file)):
            continue
        if exclude_key_words_in_file is not None and \
                (match_keywords(exclude_key_words_in_file, _data_file_name, deep_match=deep_match_in_exclude_file) or
                 match_keywords(exclude_key_words_in_file, _meta_file_path, deep_match=deep_match_in_exclude_file)):
            print('ignoring file: {:}'.format(_data_file_name))
            continue

        _parameters = {}

        if not ignore_meta_file and os.path.isfile(_meta_file_path) and meta_file_extension == 'json':
            with open(_meta_file_path, 'r') as f:
                try:
                    _parameters = json.load(f)
                except ValueError:
                    print('could not open {:}'.format(_meta_file_path))

        ini_time = [0 * u.s]
        end_time = [None]

        for _ini_time, _end_time, in zip(ini_time, end_time):
            data_links = DataLinks(parameters=_parameters,
                                   parameters_file=_meta_file_path,
                                   data_file=_full_file_name,
                                   ini_time=_ini_time,
                                   end_time=_end_time,
                                   )

            par_out = pd.concat([par_out, pd.DataFrame.from_dict(
                dict({k: [v] for k, v in _parameters.items()},
                     **{'data_links': [data_links]}))],
                                ignore_index=True)
    if par_out.size:
        t = PrettyTable()
        _aux = par_out.data_links.values.astype(np.ndarray)
        t.add_column(fieldname='File name', column=[basename(x.parameters_file) for x in _aux])
        t.add_column(fieldname='File date', column=[basename(x.parameters_date) for x in _aux])
        t.add_column(fieldname='data file name', column=[basename(x.data_file) for x in _aux])
        t.add_column(fieldname='data file date', column=[x.data_date for x in _aux])
        t.add_column(fieldname='Code', column=[x.label for x in _aux])
        t.add_column(fieldname='Ini time', column=[x.ini_time for x in _aux])
        t.add_column(fieldname='End time', column=[x.end_time for x in _aux])
        logging.info(t)
        print(t)
    else:
        print('No files were found')
    return par_out
