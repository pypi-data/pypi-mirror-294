import shutil
import sys

from ok.logging.Logger import get_logger

logger = get_logger(__name__)

import os
import fnmatch


def delete_files(blacklist_patterns=None, whitelist_patterns=None, root_dir='.'):
    """
    Delete files matching the given patterns in all directories starting from root_dir,
    except those matching the whitelist patterns.

    :param blacklist_patterns: List of file names or patterns to match.
    :param whitelist_patterns: List of file names or patterns to exclude from deletion.
    :param root_dir: Root directory to start the search from.
    """
    if whitelist_patterns is None:
        whitelist_patterns = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if blacklist_patterns is None:
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if any(fnmatch.fnmatch(filename, wp) for wp in whitelist_patterns):
                    print(f"Skipped (whitelisted): {file_path}")
                    continue
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted: {file_path}")
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting {file_path}", e)
                    print(f"Error deleting {file_path}", e)
        else:
            for pattern in blacklist_patterns:
                for filename in fnmatch.filter(filenames, pattern):
                    file_path = os.path.join(dirpath, filename)
                    if any(fnmatch.fnmatch(filename, wp) for wp in whitelist_patterns):
                        print(f"Skipped (whitelisted): {file_path}")
                        continue
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted: {file_path}")
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        logger.error(f"Error deleting {file_path}", e)
                        print(f"Error deleting {file_path}", e)


def find_line_in_requirements(file_path, search_term, encodings=['utf-16', 'utf-8', 'ISO-8859-1', 'cp1252']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                for line in file:
                    if search_term in line:
                        return line.strip()
            return None
        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error with encoding {encoding}: {e}")
    return None


def get_base_python_exe():
    # Check if running inside a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Get the path to the virtual environment's pyvenv.cfg file
        venv_cfg_path = os.path.join(sys.prefix, 'pyvenv.cfg')

        if os.path.exists(venv_cfg_path):
            with open(venv_cfg_path, 'r') as file:
                for line in file:
                    if line.startswith('home = '):
                        parent_python_path = line.split('=')[1].strip()
                        parent_python_exe = os.path.join(parent_python_path, 'python.exe')
                        return parent_python_exe
        else:
            print("pyvenv.cfg not found.")
    else:
        # Return the current Python executable location
        return sys.executable


def copy_python_files(python_dir, destination_dir):
    # Define the files to copy
    files_to_copy = ['python.exe', 'python3.dll', 'python311.dll']

    # Create the destination directory
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the files
    for file_name in files_to_copy:
        source_file = os.path.join(python_dir, file_name)
        if os.path.exists(source_file):
            shutil.copy(source_file, destination_dir)
            print(f"Copied {file_name} to {destination_dir}")
        else:
            print(f"{file_name} not found in {python_dir}")


if __name__ == '__main__':
    print(find_line_in_requirements('requirements.txt', 'ok-script'))
    delete_files(
        ['opencv_videoio_ffmpeg', 'opengl32sw.dll', 'Qt6Quick.dll', 'Qt6Pdf.dll', 'Qt6Qml.dll', 'Qt6OpenGL.dll',
         'Qt6OpenGL.pyd', '*.chm', '*.pdf', 'QtOpenGL.pyd',
         'Qt6Network.dll', 'Qt6QmlModels.dll', 'Qt6VirtualKeyboard.dll', 'QtNetwork.pyd',
         'Qt6Designer.dll'
            , 'openvino_pytorch_frontend.dll', 'openvino_tensorflow_frontend.dll', 'NEWS.txt',
         'py_tensorflow_frontend.cp311-win_amd64.pyd', 'py_pytorch_frontend.cp311-win_amd64.pyd',
         '*.exe'], 'adb.exe', 'python-launcher-lib')
