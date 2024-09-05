import importlib
import json
import locale
import math
import os
import re
import shutil
import subprocess
import sys
from functools import cmp_to_key

import git

from ok.config.Config import Config
from ok.gui.Communicate import communicate
from ok.logging.Logger import get_logger
from ok.util.Handler import Handler
from ok.util.path import get_path_relative_to_exe, delete_if_exists

logger = get_logger(__name__)

repo_path = get_path_relative_to_exe(os.path.join('update', "repo"))


class GitUpdater:

    def __init__(self, app_config, exit_event):
        self.config = app_config.get('git_update')
        self.version = app_config.get('version')
        self.debug = app_config.get('debug')
        self.repo = None
        self.handler = Handler(exit_event, self.__class__.__name__)
        self.url = self.get_current_source()['git_url']
        self.launcher_configs = []
        self.launcher_config = Config('launcher', {'profile_name': 'CPU', 'source': self.get_default_source()})

    def install_package(self, package_name):
        try:
            # Run pip install command
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Print the stdout and stderr in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logger.info(output.strip())

            # Print any remaining stderr
            stderr = process.communicate()[1]
            if stderr:
                logger.error(stderr.strip())

            # Check if the installation was successful
            if process.returncode == 0:
                logger.info(f"Package '{package_name}' installed successfully.")
            else:
                logger.error(f"Failed to install package '{package_name}'.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def update_to_version(self, version):
        self.handler.post(lambda: self.do_update_to_version(version))

    def read_launcher_config(self, path):
        with open(os.path.join(path, 'launcher.json'), 'r') as file:
            launches = json.load(file)
            logger.info(f'read launcher config success, {launches}')
            return launches

    def install_dependencies(self, launch_config):
        pass

    def do_update_to_version(self, version):
        try:
            path = os.path.join('repo', version)
            logger.info(f'start cloning repo {path}')
            delete_if_exists(path)
            repo = git.Repo.clone_from(self.url, path, branch=version, depth=1)
            self.launcher_config = logger.info(f'clone repo success {path}')
            self.read_launcher_config(path)
            self.install_package("pySide6==6.6.1")
            communicate.clone_version.emit(None)
            communicate.launcher_configs.emit(self.launcher_config)
        except Exception as e:
            logger.error('do_update_to_version error', e)
            communicate.clone_version.emit(str(e))

    # def ensure_repo(self):
    #     if self.repo is None:
    #         if os.path.exists(repo_path):
    #             if not is_valid_repo(repo_path):
    #                 # Delete the invalid repository directory
    #                 shutil.rmtree(repo_path)
    #                 # Clone the repository (shallow clone)
    #                 self.repo = git.Repo.clone_from(self.url, repo_path, depth=1)
    #             else:
    #                 # Open the existing valid repository
    #                 self.repo = git.Repo(repo_path)
    #                 # Set the origin to the remote repository URL
    #         else:
    #             # Clone the repository (shallow clone)
    #             self.repo = git.Repo.clone_from(self.url, repo_path, depth=1)
    #         origin = self.repo.remotes.origin
    #         if origin is not None and origin.url != self.url:
    #             logger.info(f'update url for repo {origin.url} to {self.url}')
    #             origin.set_url(self.url)
    #             # Force pull with depth=1 to get the latest changes
    #             origin.fetch(depth=1, force=True)
    #             # Determine the default branch
    #             default_branch = origin.refs[0].remote_head
    #             self.repo.git.reset('--hard', f'origin/{default_branch}')

    def list_all_versions(self):
        self.handler.post(self.do_list_all_versions)

    def do_list_all_versions(self):
        try:
            logger.info(f'start fetching remote version {self.url}')
            remote_refs = git.cmd.Git().ls_remote(self.url, tags=True)

            # Parse the output to get tag names
            tags = []
            for line in remote_refs.splitlines():
                if 'refs/tags/' in line:
                    tag = line.split('refs/tags/')[1]
                    if '^{}' not in tag and is_valid_version(tag):
                        tags.append(tag)
            tags = sorted(tags, key=cmp_to_key(is_newer_or_eq_version), reverse=True)
            logger.info(f'done fetching remote version size {len(tags)}')
            communicate.versions.emit(tags)
        except Exception as e:
            logger.error('fetch remote version error', e)
            communicate.versions.emit(None)
        # Print tag names
        # for tag in tags:
        #     print(tag)

    def get_sources(self):
        return self.config['sources']

    def get_current_source(self):
        return self.get_default_source()

    def get_default_source(self):
        if 'cn' in locale.getdefaultlocale()[0].lower():
            for source in self.config['sources']:
                if source['name'] == 'China':
                    return source
        return self.config['sources'][0]


def is_valid_version(tag):
    pattern = r'^v\d+\.\d+\.\d+$'
    return bool(re.match(pattern, tag))


def is_valid_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def move_file(src, dst_folder):
    # Get the file name from the source path
    file_name = os.path.basename(src)
    # Construct the full destination path
    dst = os.path.join(dst_folder, file_name)

    # Check if the destination file already exists
    if os.path.exists(dst):
        os.remove(dst)  # Remove the existing file
    shutil.move(src, dst)  # Move the file


def is_newer_or_eq_version(v1, v2):
    try:
        v1_parts = list(map(int, v1.lstrip('v').split('.')))
        v2_parts = list(map(int, v2.lstrip('v').split('.')))
        return (v1_parts > v2_parts) - (v1_parts < v2_parts)
    except Exception as e:
        logger.error(f'is_newer_or_eq_version error {v1} {v2}', e)
        return False


def get_updater_exe_local():
    if sys.version_info < (3, 9):
        context = importlib.resources.path("ok.binaries", "__init__.py")
    else:
        ref = importlib.resources.files("ok.binaries") / "__init__.py"
        context = importlib.resources.as_file(ref)
    with context as path:
        pass
    # Return the dir. We assume that the data files are on a normal dir on the fs.
    return str(path.parent) + '.exe'


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


if __name__ == '__main__':
    print(get_updater_exe_local())
