import os
import subprocess

from ok.gui.launcher.shrink import copy_python_files, get_base_python_exe, find_line_in_requirements, delete_files
from ok.logging.Logger import config_logger, get_logger

logger = get_logger(__name__)

# python -m ok.gui.launcher.init_lenv
if __name__ == '__main__':
    config_logger()
    python_exe = get_base_python_exe()
    logger.info(f'get_base_python_exe {python_exe}')
    copy_python_files(os.path.dirname(python_exe), 'python')
    mini_python_exe = 'python\\python.exe'
    lenv_path = 'python\\lenv'
    try:
        # Execute the command to create a virtual environment
        result = subprocess.run([mini_python_exe, '-m', 'venv', lenv_path], check=True, capture_output=True, text=True)
        logger.info("Virtual environment 'lenv' created successfully.")
        logger.info(result.stdout)
        lenv_python_exe = os.path.join(lenv_path, 'Scripts', 'python.exe')
        params = [lenv_python_exe, "-m", "pip", "install", "PySide6-Fluent-Widgets>=1.5.5", '--no-deps',
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install PySide6-Fluent-Widgets success")
        logger.info(result.stdout)

        params = [lenv_python_exe, "-m", "pip", "install", find_line_in_requirements('requirements.txt', 'ok-script'),
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install ok-script success")
        logger.info(result.stdout)
        delete_files(
            ['opencv_videoio_ffmpeg*.dll', 'opengl32sw.dll', 'Qt6Quick.dll', 'Qt6Pdf.dll', 'Qt6Qml.dll',
             'Qt6OpenGL.dll',
             'Qt6OpenGL.pyd', '*.chm', '*.pdf', 'QtOpenGL.pyd',
             'Qt6Network.dll', 'Qt6QmlModels.dll', 'Qt6VirtualKeyboard.dll', 'QtNetwork.pyd',
             'Qt6Designer.dll'
                , 'openvino_pytorch_frontend.dll', 'openvino_tensorflow_frontend.dll', 'NEWS.txt',
             'py_tensorflow_frontend.cp311-win_amd64.pyd', 'py_pytorch_frontend.cp311-win_amd64.pyd',
             '*.exe'], ['adb.exe', 'python.exe', 'pip*.exe'], 'python')
    except subprocess.CalledProcessError as e:
        logger.error("An error occurred while creating the virtual environment.")
        logger.error(e.stderr)
