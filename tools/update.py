import os
import datetime
import re
import shutil


def get_file_update_time(file_path):
    """Gets the update time of the file.

    Args:
      file_path: The path to the file.

    Returns:
      The update time of the file as a datetime object.
    """
    file_stat = os.stat(file_path)
    return datetime.datetime.fromtimestamp(file_stat.st_mtime)


def scan_directory_and_check_update_time(directory_path):
    """Scans a directory and checks the update time of all files in the directory.

    Args:
      directory_path: The path to the directory.

    Returns:
      A list of tuples, where each tuple contains the file path and the update time of the file.
    """
    cursor = index = 0

    targets = {0: directory_path}
    file_update_times = {}
    while cursor in targets:

        directory_path = targets[cursor]

        file_paths = os.listdir(directory_path)

        for file_path in file_paths:
            if '__pycache__' in file_path:
                continue
            fp = os.path.join(directory_path, file_path)
            if os.path.isdir(fp):

                index += 1
                targets[index] = fp
                continue
            file_update_time = get_file_update_time(fp)
            file_update_times[fp] = file_update_time
        cursor += 1

    return file_update_times


pt = re.compile(r'^/')


def compaire_file_update(target_directries):
    update_bases = {}
    for target_directory in target_directries:
        updates = scan_directory_and_check_update_time(target_directory)
        for path, update in updates.items():

            _path = pt.sub('', path.replace(target_directory, ''))
            if not _path in update_bases:
                update_bases[_path] = dict(
                    path=path, update=update, uppercount=0, checkcount=1)
                continue
            update_base = update_bases[_path]
            update_base['checkcount'] += 1

            if update_base['update'] != update:

                update_base['uppercount'] += 1
            if update_base['update'] < update:
                update_base['path'] = path

    return update_bases


def copy_updates(target_directories):
    check_counts = len(target_directories)
    update_bases = compaire_file_update(target_directries=target_directories)

    for _path, update_base in update_bases.items():

        if update_base['uppercount'] == 0 and update_base['checkcount'] == check_counts:

            continue
        copy_from = update_base['path']

        for target_directory in target_directories:
            if target_directory in copy_from:

                continue
            copy_to = target_directory + _path

            if os.path.exists(copy_to) == False:
                dirname = os.path.dirname(copy_to)
                if os.path.isdir(dirname) == False:
                    os.makedirs(dirname)

            shutil.copy2(copy_from, copy_to)


if __name__ == "__main__":
    print('start', datetime.datetime.now())
    updates = [
        ['api_server/db', 'processer/db'],
        ['api_server/data_types', 'processer/data_types']
    ]
    for update in updates:
        copy_updates(update)
    print('done', datetime.datetime.now())
