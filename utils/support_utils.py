""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS, EPICS_MASTER_RELEASE
from templates.paths import SUPPORT_MAKEFILE, SUPPORT_GITIGNORE, SUPPORT_LICENCE, DB
from common_utils import run_command
from file_system_utils import mkdir, add_to_makefile_list, replace_in_file, copy_file
from command_line_utils import get_input
from os import path, remove
import logging
from git_utils import RepoWrapper


def _build(device_info):
    logging.info("Running Make command in directory {}".format(device_info.support_master_dir()))
    run_command(["make"], device_info.support_master_dir())


def _add_submodule_directory(device_info):
    logging.info("Creating support directory {0}".format(device_info.support_dir()))
    mkdir(device_info.support_dir())
    return device_info.support_dir()


def _add_submodule_makefile(device_info):
    makefile = path.join(device_info.support_dir(), "Makefile")
    copy_file(SUPPORT_MAKEFILE, makefile)
    return makefile


def _add_submodule_to_makefile(device_info):
    return add_to_makefile_list(EPICS_SUPPORT, "SUPPDIRS", device_info.support_app_name())


def _add_submodule_to_git(device_info):
    get_input("Attempting to create repository using remote {}. Press return to confirm it exists".format(
        device_info.support_repo_url()))
    logging.info("Creating submodule at {}".format(device_info.support_master_dir()))
    RepoWrapper(EPICS).create_submodule(device_info.support_app_name(), device_info.support_repo_url(),
                                        device_info.support_master_dir())
    return path.join(EPICS, ".gitmodules")


def _run_support_template_setup(device_info):
    logging.info("Creating files in support directory {0}".format(device_info.support_master_dir()))
    #mkdir(device_info.support_master_dir())
    cmd = [PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device_info.support_app_name()]
    run_command(cmd, device_info.support_master_dir())
    if not path.exists(device_info.support_db_path()):
        logging.warning("Folder not found: {0}".format(device_info.support_db_path()))
        logging.warning("Please run the following command manually from an EPICS terminal:\n"
                        "cd {} && {}".format(device_info.support_master_dir(), " ".join(cmd)))
        get_input("Press return to continue...")
    return device_info.support_master_dir()


def _add_support_makefile_db_entry(device_info):
    makefile = path.join(device_info.support_app_path(), "Makefile")
    logging.info("Adding .db entry into {}".format(makefile))
    replace_in_file(makefile, [("#DB += xxx.db", "DB += {}.db".format(device_info.support_app_name()))])
    return makefile


def _add_support_db(device_info):
    remove(device_info.support_db_path())  # Remove existing template
    db = path.join(device_info.support_app_path(), "{}.db".format(device_info.support_app_name()))
    logging.info("Copying .db file to {}".format(db))
    copy_file(DB, db)
    return db


def _add_support_makefile_proto_entry(device_info):
    makefile = path.join(device_info.support_app_path(), "Makefile")
    replace_in_file(makefile, [("DB += {}.proto".format(device_info.support_app_name()), "")])
    logging.info("Adding .proto entry into {}".format(makefile))
    return makefile


def _add_support_licence(device_info):
    licence = path.join(device_info.support_master_dir(), "LICENCE")
    logging.info("Copying licence file to {}".format(licence))
    copy_file(SUPPORT_LICENCE, licence)
    return licence


def _add_support_gitignore(device_info):
    gitignore = path.join(device_info.support_master_dir(), ".gitignore")
    logging.info("Copying .gitignore file to {}".format(gitignore))
    copy_file(SUPPORT_GITIGNORE, gitignore)
    return gitignore


def create_submodule(device_info, create_submodule_in_git):
    """
    Creates a device submodule and links it into the main EPICS repo

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
        create_submodule_in_git (bool): True then create submodule in git; False do not do this operation
    Returns:
        files_changed (list[Str]): List of unique files that have been changed/created
    """
    files_changed = [_add_submodule_directory(device_info),
                     _add_submodule_makefile(device_info),
                     _add_submodule_to_makefile(device_info)]

    if create_submodule_in_git:
        files_changed.append(_add_submodule_to_git(device_info))
    else:
        logging.warning("You have chosen not to create the submodule in git for your ioc support module. "
                        "If files are added they will be added to EPICS not a submodule of it.")

    return list(set(files_changed))


def create_support(device_info):
    """
    Creates a devices support directory using template files

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        files_changes (list[Str]): List of unique files that have been changed/created
    """
    files_changed = [_run_support_template_setup(device_info),
                     _add_support_gitignore(device_info),
                     _add_support_licence(device_info),
                     _add_support_makefile_proto_entry(device_info),
                     _add_support_db(device_info),
                     _add_support_makefile_db_entry(device_info)]

    _build(device_info)

    return list(set(files_changed))
