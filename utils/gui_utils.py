""" Utilities for modifying the gui for a new IOC """
from git_utils import RepoWrapper
from system_paths import CLIENT
from templates.paths import BLANK_OPI
from system_paths import OPI_RESOURCES
from shutil import copyfile
from os import path
from lxml import etree
from logging_utils import logger

LOGGER = logger("GUI utils")


def create_opi(name, branch):
    """
    Creates a blank OPI as part of the GUI
    :param name: Name of the IOC to create the GUI for
    :param branch: Name of the branch to put the changes on
    :return:
    """

    LOGGER.info("Preparing GUI branch {}".format(branch))
    repo = RepoWrapper(CLIENT)
    repo.prepare_new_branch(branch)

    new_opi_file_name = "{}.opi".format(name)
    dst = path.join(OPI_RESOURCES, new_opi_file_name)
    LOGGER.info("Copying template OPI file to {}".format(dst))
    copyfile(BLANK_OPI, dst)

    # Put the OPI in OPI_info.xml
    LOGGER.info("Adding basic information to opi info")
    opi_info_path = path.join(OPI_RESOURCES, "opi_info.xml")
    with open(opi_info_path) as f:
        # Remove blank on input or pretty printing won't work later
        opi_xml = etree.parse(f, etree.XMLParser(remove_blank_text=True))

    opis = opi_xml.find("opis")
    if any(entry.find("key").text == name for entry in opis):
        LOGGER.warn("OPI with default name already exists")
    else:
        new_entry = etree.Element("entry")

        key = etree.Element("key")
        key.text = name

        value = etree.Element("value")
        value.append(etree.Element("categories"))

        type_ = etree.Element("type")
        type_.text = "UNKNOWN"
        value.append(type_)

        path_ = etree.Element("path")
        path_.text = new_opi_file_name
        value.append(path_)

        description = etree.Element("description")
        description.text = "The OPI for the {}".format(name)
        value.append(description)

        value.append(etree.Element("macros"))

        new_entry.append(key)
        new_entry.append(value)
        opis.append(new_entry)

        with open(opi_info_path, "w") as f:
            f.write(etree.tostring(opi_xml, pretty_print=True, encoding='UTF-8', xml_declaration=True, standalone="yes"))

    # Add changes to git
    LOGGER.info("Pushing changes to branch")
    repo.push_all_changes("Add template OPI file")

