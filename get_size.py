import os
import argparse
from sys_tools import SysTools


def init_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-d', '--dir', type=str, nargs='+',
                       required=True, help='Optional. Name of the directory of whose child '
                                           'directory which you want to get the size of.')
    parse.add_argument('-f', '--factor', required=True, type=str, choices=['GB', 'MB', 'KB', 'B'],
                       help='Required. GB|MB|KB|B')

    # del with space in directory or file names
    _args = parse.parse_args()
    _args.dir = ' '.join(_args.dir)
    return _args


class GetSize(SysTools):
    def __init__(self, directories, factor):
        super(GetSize, self).__init__(directories=directories, factor=factor)
        self._postfixes = []

    def process(self):
        lists = open(os.path.join(os.getcwd(), 'lists.txt'), mode='w', encoding='UTF-8')
        total_size = 0
        for path in self._all_pathes.keys():
            # get all file types
            if path.split('.')[-1] not in self._postfixes:
                self._postfixes.append(path.split('.')[-1])

            total_size += self._all_pathes[path][0]

            # save file name and it's size in lists.txt
            lists.write(path + '\t' + self._all_pathes[path][1] + '\t' +
                        str((self._all_pathes[path][0] / self._factor).__format__('.2f')) + '\t' +
                        self._str_factor+'\n')

        print('Size of Total file is', total_size / self._factor, self._str_factor + '.\n')
        for i in self._postfixes:
            lists.write(i + '\n')
        lists.close()
        return


if __name__ == '__main__':
    args = init_args()
    if args.dir is None:
        directory = [os.getcwd()]
    else:
        directory = args.dir.split(',')

    getsize = GetSize(directory, factor=args.factor)
    getsize.process()
