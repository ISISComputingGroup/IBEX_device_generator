""" Utilities for modifying the gui for a new IOC """
from templates.paths import BLANK_OPI
from system_paths import OPI_RESOURCES
from shutil import copyfile
from os import path
from lxml import etree
import logging
from device_info_generator import DeviceInfoGenerator


def _add_new_opi_file(info_generator):
    """
    :param name: Device name
    """
    dst = info_generator.opi_file_path()
    logging.info("Copying template OPI file to {}".format(dst))
    copyfile(BLANK_OPI, dst)


def _generate_opi_entry(info_generator):
    """
    Generates an ElementTree entry for opi info based on a device name
    :param name: Name of the device
    :return: ElementTree template based on the device name
    """
    entry = etree.Element("entry")

    key = etree.Element("key")
    key.text = info_generator.opi_key()

    value = etree.Element("value")
    value.append(etree.Element("categories"))

    type_ = etree.Element("type")
    type_.text = "UNKNOWN"
    value.append(type_)

    path_ = etree.Element("path")
    path_.text = info_generator.opi_file_name()
    value.append(path_)

    description = etree.Element("description")
    description.text = "The OPI for the {}".format(info_generator.log_name())
    value.append(description)

    value.append(etree.Element("macros"))

    entry.append(key)
    entry.append(value)

    return entry


def _update_opi_info(info_generator):
    """
    Add some basic template information to the opi_info.xml file
    :param name: Name of the device
    """
    logging.info("Adding template information to opi info")
    opi_info_path = path.join(OPI_RESOURCES, "opi_info.xml")
    with open(opi_info_path) as f:
        # Remove blank on input or pretty printing won't work later
        opi_xml = etree.parse(f, etree.XMLParser(remove_blank_text=True))

    opis = opi_xml.find("opis")
    if any(entry.find("key").text == info_generator.opi_key() for entry in opis):
        raise RuntimeWarning("OPI with default name already exists")

    opis.append(_generate_opi_entry(info_generator))
    with open(opi_info_path, "w") as f:
        f.write(
            etree.tostring(opi_xml, pretty_print=True, encoding='UTF-8', xml_declaration=True, standalone="yes"))


def create_opi(device):
    """
    Creates a blank OPI as part of the GUI and add it to the OPI info
    :param device: Name of the device to create the GUI for
    """
    info_generator = DeviceInfoGenerator(device)
    _add_new_opi_file(info_generator)
    _update_opi_info(info_generator)
