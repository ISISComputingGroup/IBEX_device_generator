""" Utilities for adding a template emulator for a new IBEX device"""
from git_utils import RepoWrapper
from system_paths import CLIENT
from templates.paths import BLANK_OPI
from system_paths import OPI_RESOURCES
from shutil import copyfile
from os import path
from lxml import etree
from logging_utils import logger

LOGGER = logger("Emulators")


def _get_opi_file_name(name):
    """
    Generate the opi file name for a given device name
    :param name: The name of the device
    :return: The opi file name
    """
    return "{}.opi".format(name.lower().replace(" ", "_"))


def _add_new_opi_file(name):
    """
    :param name: Device name
    """
    dst = path.join(OPI_RESOURCES, _get_opi_file_name(name))
    LOGGER.info("Copying template OPI file to {}".format(dst))
    copyfile(BLANK_OPI, dst)


def _generate_opi_entry(name):
    """
    Generates an ElementTree entry for opi info based on a device name
    :param name: Name of the device
    :return: ElementTree template based on the device name
    """
    entry = etree.Element("entry")

    key = etree.Element("key")
    key.text = name

    value = etree.Element("value")
    value.append(etree.Element("categories"))

    type_ = etree.Element("type")
    type_.text = "UNKNOWN"
    value.append(type_)

    path_ = etree.Element("path")
    path_.text = _get_opi_file_name(name)
    value.append(path_)

    description = etree.Element("description")
    description.text = "The OPI for the {}".format(name)
    value.append(description)

    value.append(etree.Element("macros"))

    entry.append(key)
    entry.append(value)

    return entry


def _push_changes(repo):
    """
    :param repo: GUI git repository
    """
    LOGGER.info("Pushing changes to branch")
    repo.push_all_changes("Add template OPI file")


def create_opi(name, branch):
    """
    Creates a blank OPI as part of the GUI
    :param name: Name of the IOC to create the GUI for
    :param branch: Name of the branch to put the changes on
    """
    try:
        repo = RepoWrapper(CLIENT)
        _prepare_branch(repo, branch)
        _update_opi_info(name)
        _push_changes(repo)
    except (RuntimeError, IOError) as e:
        LOGGER.error(str(e))
        return
    except Exception as e:
        LOGGER.error("Encountered unknown error: {}".format(e))
        return
    except RuntimeWarning as e:
        LOGGER.warning(str(e))

