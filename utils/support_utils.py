""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS, EPICS_MASTER_RELEASE
from templates.paths import SUPPORT_MAKEFILE
from common_utils import run_command
from file_system_utils import mkdir, add_to_makefile_list, get_input
from os import path, remove
from shutil import copyfile
import logging
from git_utils import RepoWrapper


def _add_to_makefile(name):
    """
    Args:
        name: Name of the device
    """
    add_to_makefile_list(EPICS_SUPPORT, "SUPPDIRS", name)


def _add_macro(device_info):
    """
    Adds a macro to MASTER_RELEASE

    Args:
        device_info: Name-based device information
    """
    logging.info("Adding macro to MASTER_RELEASE")
    with open(EPICS_MASTER_RELEASE, "a") as f:
        f.write("# Auto-generated macro for {}\n".format(device_info.log_name()))
        f.write("{macro}=$(SUPPORT)/{name}/master\n".format(
            macro=device_info.ioc_name(), name=device_info.support_app_name()))


def create_submodule(device_info):
    """
    Creates a submodule and links it into the main EPICS repo

    Args:
        device_info: Provides name-based information about the device
    """
    mkdir(device_info.support_dir())
    copyfile(SUPPORT_MAKEFILE, path.join(device_info.support_dir(), "Makefile"))
    master_dir = device_info.support_master_dir()
    get_input("Attempting to create repository using remote {}. Press return to confirm it exists"
              .format(device_info.support_repo_url()))
    epics_repo = RepoWrapper(EPICS)
    if epics_repo.contains_support_submodule(device_info.support_repo_url()):
        get_input("Submodule already exists. Confirm this is as expected and press return to continue")
    else:
        RepoWrapper(EPICS).create_submodule(device_info.support_app_name(), device_info.support_repo_url(), master_dir)
    logging.info("Initializing device support repository {}".format(master_dir))
    _add_to_makefile(device_info.support_app_name())
    _add_macro(device_info)


def apply_support_dir_template(device_info):
    """
    Args:
        device_info: Provides name-based information about the device
    """
    cmd = [PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device_info.support_app_name()]
    run_command(cmd, device_info.support_master_dir())
    if not path.exists(device_info.support_db_path()):
        logging.warning("The makeSupport.pl didn't run correctly. It's very temperamental. "
                        "Please run the following command manually from an EPICS terminal")
        logging.warning("cd {} && {}".format(device_info.support_master_dir(), " ".join(cmd)))
        get_input("Press return to continue...")
    remove(device_info.support_db_path())
