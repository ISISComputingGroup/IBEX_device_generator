""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS, EPICS_MASTER_RELEASE
from templates.paths import SUPPORT_MAKEFILE, SUPPORT_GITIGNORE, SUPPORT_LICENCE, DB
from utils.common_utils import run_command, get_year
from utils.file_system_utils import append_to_file, mkdir, add_to_makefile_list, replace_in_file, copy_file
from utils.command_line_utils import get_input
from os import path, remove, linesep
from shutil import copyfile
import logging
from utils.git_utils import RepoWrapper
import datetime

def _add_to_makefile(name):
    """
    Args:
        name: Name of the device
    """
    add_to_makefile_list(EPICS_SUPPORT, "SUPPDIRS", name)


def create_submodule(device_info, create_submodule_in_git):
    """
    Creates a submodule and links it into the main EPICS repo

    Args:
        device_info: Provides name-based information about the device
        create_submodule_in_git: True then create submodule in git; False do not do this operation
    """
    mkdir(device_info.support_dir())
    copyfile(SUPPORT_MAKEFILE, path.join(device_info.support_dir(), "Makefile"))
    master_dir = device_info.support_master_dir()
    if create_submodule_in_git:
        if path.isdir(path.join(master_dir, ".git")):
            logging.error("A git repository (not submodule) already exists at {0}."
                          "Remove this to be able to creat the submodule correctly".format(master_dir))
            exit()
        get_input("Attempting to create repository using remote {}. Press return to confirm it exists".format(
            device_info.support_repo_url()))
        RepoWrapper(EPICS).create_submodule(device_info.support_app_name(), device_info.support_repo_url(), master_dir)
    else:
        logging.warning("Because you have chosen no-git the submodule has not been added for your ioc support module. "
                        "If files are added they will be added to EPICS not a submodule of it.")

    logging.info("Initializing device support repository {}".format(master_dir))
    _add_to_makefile(device_info.support_app_name())


def apply_support_dir_template(device_info):
    """
    Args:
        device_info: Provides name-based information about the device
    """
    mkdir(device_info.support_master_dir())
    cmd = [PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device_info.support_app_name()]
    run_command(cmd, device_info.support_master_dir())
    if not path.exists(device_info.support_db_path()):
        logging.warning("The makeSupport.pl didn't run correctly. It's very temperamental. "
                        "Please run the following command manually from an EPICS terminal")
        logging.warning("cd {} && {}".format(device_info.support_master_dir(), " ".join(cmd)))
        get_input("Press return to continue...")

    # Some manual tweaks to the auto template
    remove(device_info.support_db_path())
    copyfile(SUPPORT_GITIGNORE, path.join(device_info.support_master_dir(), ".gitignore"))

    copied_license_filepath =  path.join(device_info.support_master_dir(), "LICENCE")
    copyfile(SUPPORT_LICENCE, copied_license_filepath)
    replace_in_file(copied_license_filepath, [("_YEAR_", get_year())])
    replace_in_file(path.join(device_info.support_app_path(), "Makefile"),
                    [("DB += {}.proto".format(device_info.support_app_name()), "")])
    _add_template_db(device_info)
    append_to_file(
        path.join(device_info.support_master_dir(), "Makefile"),
        [linesep + "ioctests:", linesep + "\t.\\system_tests\\run_tests.bat", linesep]
    )

    run_command(["make"], device_info.support_master_dir())


def _add_template_db(device_info):
    """
    Add the basic DB file to the support module

    Args:
        device_info: Name-based information about the device
    """
    db_dir = path.join(device_info.support_app_path())
    logging.info("Copying basic Db file to {}".format(db_dir))
    copy_file(DB, path.join(db_dir, "{}.db".format(device_info.support_app_name())))

    # Make sure Db is included in the build
    replace_in_file(path.join(db_dir, "Makefile"), [("#DB += xxx.db", "DB += {}.db".format(device_info.support_app_name()))])


