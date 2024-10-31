import os


def get_list_of_files(base_path: str, format_strs: list):
    """
    Get a list of file paths in the given dir that end with given
    list of format strs. Eg. ['.txt', '.csv']
    """

    list_of_files = []
    for f in os.listdir(base_path):
        for format in format_strs:
            if any(f.endswith(format)):
                list_of_files.append(f)

    return list_of_files
