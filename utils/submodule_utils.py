""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS
from templates.paths import SUPPORT_MAKEFILE
from common_utils import run_command
from file_system_utils import mkdir
from os import path, remove
from shutil import copyfile
import logging
from git_utils import RepoWrapper


def _add_to_makefile(name):
    """
    :param name: Name of the device
    """
    makefile = path.join(EPICS_SUPPORT, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()
    new_lines = []
    last_line = ""
    marker = "SUPPDIRS += "
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + name)
        new_lines.append(line)

    with open(makefile, "w") as f:
        f.writelines(new_lines)


def create_submodule(device_info):
    """
    Creates a submodule and links it into the main EPICS repo
    :param device_info: Provides name-based information about the device
    """
    mkdir(device_info.support_dir())
    copyfile(SUPPORT_MAKEFILE, path.join(device_info.support_dir(), "Makefile"))
    master_dir = device_info.support_master_dir()
    RepoWrapper(EPICS).create_submodule(device_info.support_app_name(), device_info.support_repo_url(), master_dir)
    logging.info("Initializing device support repository {}".format(master_dir))
    _add_to_makefile(device_info.support_app_name())


def apply_support_dir_template(device_info):
    """
    :param device_info: Provides name-based information about the device
    :return:
    """
    run_command([PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device_info.support_app_name()],
                device_info.support_master_dir())
    remove(device_info.support_db_path())
