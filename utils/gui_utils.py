""" Utilities for modifying the gui for a new IOC """
from templates.paths import OPI
from system_paths import OPI_RESOURCES
from shutil import copyfile
from os import path
from lxml import etree
import logging


def _generate_opi_entry(opi_key, opi_file_name, descriptive_device_name):
    """
    Generates an ElementTree entry for opi info based on a device name
    :param opi_key: Key to identify to OPI to the GUI
    :param opi_file_name: File name to the device's opi
    :param descriptive_device_name: Human readable device name
    :return: ElementTree template based on the device name
    """
    entry = etree.Element("entry")

    key = etree.Element("key")
    key.text = opi_key

    value = etree.Element("value")
    value.append(etree.Element("categories"))

    type_ = etree.Element("type")
    type_.text = "UNKNOWN"
    value.append(type_)

    path_ = etree.Element("path")
    path_.text = opi_file_name
    value.append(path_)

    description = etree.Element("description")
    description.text = "The OPI for the {}".format(descriptive_device_name)
    value.append(description)

    value.append(etree.Element("macros"))

    entry.append(key)
    entry.append(value)

    return entry


def _update_opi_info(opi_key, opi_file_name, descriptive_device_name):
    """
    Add some basic template information to the opi_info.xml file
    :param opi_key: Key to identify to OPI to the GUI
    :param opi_file_name: File name to the device's opi
    :param descriptive_device_name: Human readable device name
    """
    logging.info("Adding template information to opi info")
    opi_info_path = path.join(OPI_RESOURCES, "opi_info.xml")
    with open(opi_info_path) as f:
        # Remove blank on input or pretty printing won't work later
        opi_xml = etree.parse(f, etree.XMLParser(remove_blank_text=True))

    opis = opi_xml.find("opis")
    if any(entry.find("key").text == opi_key for entry in opis):
        raise RuntimeWarning("OPI with default name already exists")

    opis.append(_generate_opi_entry(opi_key, opi_file_name, descriptive_device_name))
    with open(opi_info_path, "w") as f:
        f.write(
            etree.tostring(opi_xml, pretty_print=True, encoding='UTF-8', xml_declaration=True, standalone="yes"))


def create_opi(device_info):
    """
    Creates a blank OPI as part of the GUI and add it to the OPI info
    :param device_info: Provides name-based information about the device
    """
    logging.info("Copying template OPI file to {}".format(device_info.opi_file_path()))
    copyfile(OPI, device_info.opi_file_path())
    _update_opi_info(device_info.opi_key(), device_info.opi_file_name(), device_info.log_name())
