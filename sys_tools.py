import os
import re

from math import pow


class SysTools:
    def __init__(self, directories, factor):
        for _d in directories:
            assert os.path.exists(_d), 'Directories does not exist!'
        assert factor.upper() == 'GB' or 'MB' or 'KB' or 'B', 'Factor is required and must be GB|MB|KB|B.'
        self._dirs = directories
        self._str_factor = factor.upper()
        self._factor = self._get_factor()
        self._all_pathes = {}
        self._get_all_file_names()

    def _get_all_file_names(self):
        for _dir in self._dirs:
            if os.path.isdir(_dir):
                for root, d, files in os.walk(_dir):
                    for file in files:
                        path = os.path.join(root, file)
                        if os.path.isfile(path):
                            self._all_pathes[path] = [os.path.getsize(path), root,
                                                      list(filter(None, re.split(r'[:\\]', root)))[-1] + '_' + file]
            elif os.path.isfile(_dir):
                # to erase ':' in name of the upper directory of the files
                self._all_pathes[_dir] = [os.path.getsize(_dir), os.path.dirname(_dir),
                                          list(filter(None, re.split(r'[:\\]', _dir)))[-2] + '_' +
                                          re.split(r'[:\\]', _dir)[-1]]
        return

    def _get_factor(self):
        factors = {
            'GB': 1.0 * pow(2, 30),
            'MB': 1.0 * pow(2, 20),
            'KB': 1.0 * pow(2, 10),
            'B': 1.0

        }
        return factors[self._str_factor]
