""" Utilities for modifying the gui for a new IOC """
from templates.paths import OPI
from system_paths import OPI_RESOURCES
from file_system_utils import replace_in_file
from shutil import copyfile
from os import path
from lxml import etree
import logging


def _generate_opi_entry(device_info):
    """
    Generates an ElementTree entry for opi info based on a device name
    
    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    
    Returns:
        entry (etree.Element): ElementTree template based on the device name
    """
    entry = etree.Element("entry")

    key = etree.Element("key")
    key.text = device_info.opi_key()

    value = etree.Element("value")
    value.append(etree.Element("categories"))

    type_ = etree.Element("type")
    type_.text = "UNKNOWN"
    value.append(type_)

    path_ = etree.Element("path")
    path_.text = device_info.opi_file_name()
    value.append(path_)

    description = etree.Element("description")
    description.text = "The OPI for the {}".format(device_info.log_name())
    value.append(description)

    macros = etree.Element("macros")
    macro = etree.Element("macro")
    name = etree.Element("name")
    name.text = device_info.ioc_name()
    description = etree.Element("description")
    description.text = "The {} PV prefix (e.g. {}_01)".format(device_info.log_name(), device_info.ioc_name())
    macro.append(name)
    macro.append(description)
    macros.append(macro)
    value.append(macros)

    entry.append(key)
    entry.append(value)

    return entry


def _update_opi_info(device_info):
    """
    Add some basic template information to the opi_info.xml file

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device

    Returns:
        opi_info_path (Str): Path of the opi_info.xml
    """
    logging.info("Adding template information to opi info")
    opi_info_path = path.join(OPI_RESOURCES, "opi_info.xml")
    with open(opi_info_path) as f:
        # Remove blank on input or pretty printing won't work later
        opi_xml = etree.parse(f, etree.XMLParser(remove_blank_text=True))

    opis = opi_xml.find("opis")
    if any(entry.find("key").text == device_info.opi_key() for entry in opis):
        raise RuntimeWarning("OPI with default name already exists")

    opis.append(_generate_opi_entry(device_info))
    with open(opi_info_path, "w") as f:
        f.write(
            etree.tostring(opi_xml, pretty_print=True, encoding='UTF-8', xml_declaration=True, standalone="yes"))

    return opi_info_path


def _add_opi_file(device_info):
    opi_path = device_info.opi_file_path()
    logging.info("Copying template OPI file to {}".format(opi_path))
    copyfile(OPI, opi_path)
    replace_in_file(device_info.opi_file_path(), [("$(DEVICE)", "$({})".format(device_info.ioc_name()))])
    return opi_path


def create_opi(device_info):
    """
    Creates a blank OPI as part of the GUI and add it to the OPI info

    Args:
        device_info (DeviceInfoGenerator): Provides name-based information about the device
    Returns:
        files_changes (list[Str]): List of unique files that have been changed/created
    """
    files_changed = [_add_opi_file(device_info)]

    _update_opi_info(device_info)

    return list(set(files_changed))
