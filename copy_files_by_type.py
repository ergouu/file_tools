import os
import shutil
import time as T
import argparse

from sys_tools import SysTools


def init_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-s', '--source_dir', nargs='+', type=str, required=True,
                       help='Required. Specify the source files.')
    parse.add_argument('-d', '--dst_dir', nargs='+', type=str, required=True,
                       help='Required. Specify the destination directory')
    parse.add_argument('--del_flag', default=False, type=bool,
                       help='Optional. Remove files after finishing copy.')
    parse.add_argument('-f', '--factor', required=True, type=str, choices=['GB', 'MB', 'KB', 'B'],
                       help='Required. GB|MB|KB|B')
    parse.add_argument('-t', '--type', type=str, help='Optional. Specified list of which type of file to be copy.'
                                                      'For example, txt,jpg,rmvb')
    # del with space in directory or file names
    _args = parse.parse_args()
    _args.source_dir = ' '.join(_args.source_dir)
    _args.dst_dir = ' '.join(_args.dst_dir)
    return _args


class CopyFilesByType(SysTools):
    def __init__(self, directories, factor, dst_dir, del_flag, type_flag):
        super(CopyFilesByType, self).__init__(directories=directories, factor=factor)

        assert dst_dir is not None, 'Destination directory must be specifed!'
        self._dst_dir = dst_dir

        self._file_types = {
            'media': [
                ['AVI', 'MP4', 'MKV', 'RM', 'RMVB', 'MOV', '3GP', 'WMV', 'FLV', 'MPG', 'JPG', 'PNG', 'JPEG', 'BMP',
                 'JPG2', 'JPGQM', 'GIT', 'JFIF', 'IMG'], [os.path.join(self._dst_dir, 'media')]],
            'text': [['TXT', 'XLSX', 'XLS', 'WD', 'DOC', 'DOCX', 'LOG', 'CSV', 'CHM', 'PPT', 'PDF', 'PPTX', 'TXTQM'],
                     [os.path.join(self._dst_dir, 'text')]],
            'zipped': [['RAR', 'ZIP', 'ZP', 'GZ', '7Z', 'ISO', 'TAR', 'Z', 'GZIP'],
                       [os.path.join(self._dst_dir, 'zipped')]],
            'executable': [['EXE', 'BAT', 'BIN'], [os.path.join(self._dst_dir, 'executable')]],
            'others': [['OTHERS'], [os.path.join(self._dst_dir, 'others')]]
        }
        if del_flag is not None:
            self._del_flag = del_flag
        else:
            self._del_flag = False
        self._type_flags = self._get_type_flag(type_flag) if type_flag is not None else None

    def process(self):
        total_size = 0
        total_files = 0
        if not os.path.exists(self._dst_dir):
            os.mkdir(self._dst_dir)

        # make all types directories
        if os.path.exists(self._dst_dir):
            for k in self._file_types.keys():
                if not os.path.exists(self._file_types[k][-1][0]):
                    os.mkdir(self._file_types[k][-1][0])

        # new file name is old_dir_old_file_name
        for path in self._all_pathes.keys():
            start = T.time()
            f_type = self._get_file_type(path)
            f_postfix = path.split('.')[-1] if f_type != 'others' else 'OTHERS'
            # if type flags were specified and the file type is not in the list then skip to the next one
            if (self._type_flags is not None) and (f_postfix.upper() not in self._type_flags):
                continue

            f_new_name = self._all_pathes[path][2]

            # if there was a ':' in f_new_name the dst_path would be incorrectly joined
            dst_path = os.path.join(self._file_types[f_type][-1][0], f_new_name)
            print('Copying ', path, 'to', dst_path, (self._all_pathes[path][0] / self._factor).__format__('.2f'),
                  self._str_factor, '...')
            try:
                shutil.copy(path, dst_path)
                total_files += 1
                if self._del_flag:
                    os.remove(path)
                    if not os.listdir(self._all_pathes[path][1]):
                        os.rmdir(self._all_pathes[path][1])
                total_size += self._all_pathes[path][0]
                stop = T.time()
                print('Done! Duration:' + str(stop - start) + 's.\n')
            except Exception as e:
                stop = T.time()
                print('Failed!', e, '! Duration:' + str(stop - start) + 's.\n')

        print(total_files, 'files have(has) been moved.', 'Total size:' +
              str((total_size / self._factor).__format__('.2f')) + self._str_factor + '.\n')
        return

    def _get_file_type(self, path):
        """
        to get the file's type :media ,text, executable, zipped or others
        :param path:
        :return:
        """
        f_postfix = path.split('.')[-1].upper()
        for k in self._file_types.keys():
            if f_postfix in self._file_types[k][0]:
                return k
        return 'others'

    def _get_type_flag(self, type_flag):
        """
        to get all the specified types which to be copied
        :param type_flag:
        :return:
        """
        res = []
        type_list = type_flag.split(',')
        for t in type_list:
            if t.lower() in self._file_types.keys():
                res += self._file_types[t.lower()][0]
            else:
                res += [t.upper()]
        return res


if __name__ == '__main__':
    args = init_args()
    if args.source_dir is None:
        d = [os.getcwd()]
    else:
        d = list(args.source_dir.split(','))
    cpfile = CopyFilesByType(d, factor=args.factor, dst_dir=args.dst_dir,
                             del_flag=args.del_flag, type_flag=args.type)
    cpfile.process()
