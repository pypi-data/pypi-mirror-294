import os

def is_ignored(path, ignore_list, is_directory=False):
    for ignore in ignore_list:
        ignore = ignore.rstrip('/')
        
        if ignore.startswith('*.') and path.endswith(ignore.lstrip('*')):
            return True

        if os.path.basename(path) == ignore:
            return True
        
        if ignore.endswith('/*'):
            ignore_dir = ignore.rstrip('/*')
            if os.path.abspath(path).startswith(os.path.abspath(ignore_dir)):
                return True

        if ignore.endswith('/*') and is_directory:
            ignore_dir = ignore.rstrip('/*')
            if os.path.abspath(path).startswith(os.path.abspath(ignore_dir)):
                return True

    return False


def is_text_file(file_path):
    try:
        with open(file_path, 'tr', encoding='utf-8') as check_file:
            check_file.read()
        return True
    except:
        return False

def should_split(current_size, additional_size, split_size):
    return split_size and (current_size + additional_size > split_size)

def get_path(path, use_absolute_paths, current_directory):
    if use_absolute_paths:
        return os.path.abspath(path)
    else:
        return os.path.relpath(path, current_directory)
