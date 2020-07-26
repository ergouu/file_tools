import os
import argparse

from sys_tools import SysTools


def init_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-d', '--dir', type=str, nargs='+',
                       help='Optional. A list of names of the directory of whose child '
                            'directory which you want to get the size of.')
    parse.add_argument('-p', '--del_postfix', type=str, help='Optional. The kind of postfix to be delete.')
    parse.add_argument('-s', '--del_size', type=float, help='Required if size_flag was specified. Any file larger or '
                                                            'smaller than del_size would be deleted. Examples, '
                                                            ' 100.')
    parse.add_argument('--larger', dest='size_flag', type=bool, default=False,
                       help='When specified ,size_flag is True. True is larger, False is smaller.')
    parse.add_argument('-f', '--factor', required=True, type=str, choices=['GB', 'MB', 'KB', 'B'],
                       help='Required. GB|MB|KB|B')
    _args = parse.parse_args()
    _args.dir = ' '.join(_args.dir)
    return _args


class DelFiles(SysTools):
    def __init__(self, directories, factor, del_postfix, del_size, size_flag):
        super(DelFiles, self).__init__(directories=directories, factor=factor)
        self._del_postfix = del_postfix
        self._del_size = del_size
        self._size_flag = size_flag
        print(self._size_flag)

    def process(self):
        total_size = 0
        dels = open(os.path.join(os.getcwd(), 'dels.txt'), mode='w', encoding='UTF-8')
        for path in self._all_pathes.keys():
            # get the size of the file
            file_size = self._all_pathes[path][0]
            file_size = file_size / self._factor

            # delete the files having the specified postfix
            if self._del_postfix is not None:
                postfix = path.split('.')[-1].upper()
                if postfix == self._del_postfix.upper():
                    dels.write(path + '\n')
                    os.remove(path)
                    total_size += file_size
                    root = self._all_pathes[path][1]
                    if not os.listdir(root):
                        os.rmdir(root)
                        dels.write(root + '\n')

            # delete the size bigger or smaller than del_size
            if (self._del_size is not None) and ((self._size_flag and file_size > self._del_size) or (
                    (not self._size_flag) and file_size < self._del_size)):
                dels.write(path + '\n')
                os.remove(path)
                total_size += file_size

        print(
            str(total_size) + self._str_factor + ' have been deleted! List of those files was save in \'dels.txt\'\n')
        dels.close()


if __name__ == '__main__':
    args = init_args()
    if args.dir is None:
        d = [os.getcwd()]
    else:
        d = list(args.dir.split(','))

    getsize = DelFiles(d, factor=args.factor, del_postfix=args.del_postfix, del_size=args.del_size,
                       size_flag=args.size_flag)
    getsize.process()
