import logging
import os
from distutils.core import setup
from Cython.Build import cythonize

from config import EXCLUDE_FILES


def get_py_files(directory, exclude_files):
    module_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file not in exclude_files:
                module_list.append(os.path.join(root, file))
    return module_list


def build_py(directory, exclude_files):
    module_list = get_py_files(directory, exclude_files)
    if module_list:
        try:
            setup(
                ext_modules=cythonize(
                    module_list,
                    compiler_directives={'language_level': "3"}
                ),
                script_args=["build_ext", "-i"]
            )
        except Exception as e:
            print(e)


def clear_file(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".c") or (file.endswith(".py") and file not in EXCLUDE_FILES):
                try:
                    os.remove(os.path.join(root, file))
                except OSError:
                    logging.error(f"删除文件{os.path.join(root, file)}报错")


def main(directory):
    build_py(directory, EXCLUDE_FILES)
    clear_file(directory)


if __name__ == '__main__':
    directory = r"F:\pythonProjects\hc-python-build"
    try:
        main(directory)
    except Exception as e:
        print(e)
