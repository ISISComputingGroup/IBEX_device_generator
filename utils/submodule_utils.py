""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS
from templates.paths import SUPPORT_MAKEFILE, SUPPORT_README
from common_utils import run_command, replace_in_file, rmtree, get_input, mkdir
from os import path, remove
from shutil import copyfile
import logging
from git_utils import RepoWrapper
from device_info_generator import DeviceInfoGenerator


def _add_to_makefile(device):
    makefile = path.join(EPICS_SUPPORT, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()
    new_lines = []
    last_line = ""
    marker = "SUPPDIRS += "
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + device)
        new_lines.append(line)

    with open(makefile, "w") as f:
        f.writelines(new_lines)


def create_submodule(device):
    """
    Creates a submodule and links it into the main EPICS repo
    :param device: Name of the device
    """
    device_info = DeviceInfoGenerator(device)
    mkdir(device_info.support_dir())
    copyfile(SUPPORT_MAKEFILE, path.join(device_info.support_dir(), "Makefile"))
    RepoWrapper(EPICS).clone_from(device_info.support_repo_url())
    try:
        RepoWrapper(device_info.support_master_dir()).init()
    except RuntimeError as e:
        logging.error(str(e))
    else:
        RepoWrapper(EPICS).create_submodule(device_info.support_repo_url(), device_info.support_master_dir())
        _add_to_makefile(device)


def apply_support_dir_template(device):
    """
    :param device:
    :return:
    """
    device_info = DeviceInfoGenerator(device)
    run_command([PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device_info.support_app_name()],
                device_info.support_master_dir())
    remove(device_info.support_db_path())
