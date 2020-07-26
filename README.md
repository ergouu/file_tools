# file_tools

some scripts to copy , move or get size of files.

## get size

> Function : Get every single file in the specified directories.
> 
> Usage:
>
> `python get_size.py [-d|--dir] DIR_TO_GET_SIZE_OF [-f|--factor] {GB|MB|KB|B}`
>
> DIR_TO_OPERATE can be a list of directories or files, like *-s E:xxx,E:\xxx\yyy z\zzz\d.type*. After executed the 
> script, a file named **'lists.txt'** would be generated under the current working_dir, with the format of each line as
> *'abusolute_path  upper_dir_path  file_size   factor'*.
>

## delete file

> Function : Delete the type of file specified by file types or size.
>
> Usage:
>
> `python del_files.py [-d|--dir] DIR_TO_OPERATE [-p|--del_postfix] TYPES_TO_DELETE [-s|--del_size] THRESHOLD_SIZE 
> --larger {*} [-f|--factor] {GB|MB|KB|B}`
>
> DIR_TO_OPERATE can be a list of directories or files, like *-s E:xxx,E:\xxx\yyy z\zzz\d.type*. If TYPES_TO_DELETE was 
> specified, file of this type would be delete. TYPES_TO_DELETE can be specified both ambiguous and explicit,for an 
> example, -p|--postfix txt for deleting the txt files exactly, or -p|--del_postfix text for deleting
> all text file sush as txt,doc,docx,chm,pdf etc.
>
> If THRESHOLD_SIZE was specified , any file ,whose size is smaller than THRESHOLD_SIZE by default, would be deleted,
> or by using **--larger** flag to delete those larger than THRESHOLD_SIZE.
>
> TODO:
>
> *Delete file according to a list of file path.*

## copy files by type

> Function: Copy files to the specified direcotry.
>
> Usage:
>
> `python copy_files_by_type.py [-d|--dst_dir] DST_DIR [-f|factor] {GB|MB|KB|B} [-s|--source_dir] SRC_DIR --del_flag 
> DEL_FLAG [-t|--type] TYPE_TO_BE_COPIED`
>
> SRC_DIR can be a list of directories or files, like *-s E:xxx,E:\xxx\yyy z\zzz\d.type*. DST_DIR is a single 
> path of directory. If **--del_flag** was specified, the files would be deleted after finished copying.
>
> TODO:
>
> *Inverse all copy or move operations.*
