""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import IOC_ROOT, PERL, PERL_IOC_GENERATOR, EPICS, ARCHITECTURE
from templates.paths import CONFIG_XML, CONFIG_XML_NOT_0
from utils.common_utils import run_command
from utils.file_system_utils import replace_in_file, rmtree, mkdir, copy_file, add_to_makefile_list
from os import path, walk, remove
import logging


def _run_ioc_template_setup(device_info, device_count):
    """
    Runs the EPICS perl scripts associated with IOC creation. Passes in the IBEX type flag to use our own templates
    found in C:\\Instrument\\Apps\\EPICS\\base\\master\\templates

    Args:
        device_info: Name-based information about the device
        device_count: How many IOC apps to generate
    """
    if device_count > 99:
        raise ValueError("Cannot generate more than 99 IOCs for a single device")

    for i in range(1, device_count+1):
        app_name = device_info.ioc_app_name(i)
        logging.info("Generating IOC {}".format(app_name))
        run_command([PERL, PERL_IOC_GENERATOR, "-a", ARCHITECTURE, "-t", "ioc", app_name], device_info.ioc_path())
        run_command([PERL, PERL_IOC_GENERATOR, "-a", ARCHITECTURE, "-i", "-t", "ioc", "-p", app_name, app_name],
                    device_info.ioc_path())


def _add_template_config_xml(device_info, device_count):
    """
    Add the basic config.xml file to the IOC

    Args:
        device_info: Name-based information about the device
        device_count: How many IOC apps to generate
    """
    copy_file(CONFIG_XML, path.join(device_info.ioc_boot_path(1), "config.xml"))
    for i in range(2, device_count+1):
        copy_file(CONFIG_XML_NOT_0, path.join(device_info.ioc_boot_path(i), "config.xml"))
    run_command(["make", "iocstartups"], EPICS)


def _replace_macros(device_info, device_count):
    """
    Replace a couple of templates in the st.cmd with generated names

    Args:
        device_info: Name-based information about the device
        device_count: How many IOC apps to update
    """
    for i in range(1, device_count+1):
        files_containing_macros = [
            path.join(device_info.ioc_src_path(i), "Makefile"),
            path.join(device_info.ioc_boot_path(i), "st.cmd"),
            path.join(device_info.ioc_boot_path(i), "st-common.cmd"),
            path.join(device_info.ioc_boot_path(i), "config.xml")]

        for file_containing_macros in files_containing_macros:
            if not path.exists(file_containing_macros):
                AssertionError("Attempting to replace macros before command file has been created")
            replace_in_file(file_containing_macros,
                            [("_SUPPORT_MACRO_", device_info.ioc_name()),
                             ("_DB_NAME_", device_info.ioc_name()),
                             ("_NAME_LOWER_", device_info.support_app_name()),
                             ("_01_APP_NAME_", device_info.ioc_app_name(1))])


def _clean_up(device_info, device_count):
    """
    Clean up any files generated by Perl that we don't need (including those that are generated for devices 2+)

    Args:
        device_info: device information
        device_count: number of devices
    """

    logging.info("Removing unnecessary files from {}".format(device_info.ioc_path()))
    for root, dirs, files in walk(device_info.ioc_path()):
        for d in dirs:
            if d == "protocol":
                rmtree(path.join(root, d))

    for i in range(2, device_count + 1):
        remove(path.join(device_info.ioc_boot_path(i), "st-common.cmd"))
        remove(path.join(device_info.ioc_src_path(i), "build.mak"))


def _build(ioc_path):
    """
    Build the IOC

    Args:
        ioc_path: Path to the IOC directory
    """
    run_command(["make"], ioc_path)


def _add_to_ioc_makefile(name):
    """
    Add the IOC to the main IOC makefile repo

    Args:
        name: IOC name
    """
    add_to_makefile_list(IOC_ROOT, "IOCDIRS", name)


def _add_macro_to_release_file(device_info):
    """
    Adds a macro for the support directory to IOC release file

    Args:
        device_info: Name-based device information
    """
    logging.info("Adding macro to RELEASE")
    with open(path.join(device_info.ioc_path(), "configure", "RELEASE"), "a") as f:
        f.write("{macro}=$(SUPPORT)/{name}/master\n".format(
            macro=device_info.ioc_name(), name=device_info.support_app_name()))


def create_ioc(device_info, device_count):
    """
    Creates a vanilla IOC in the EPICS IOC submodule

    Args:
        device_info: Provides name-based information about the device
        device_count: Number of IOCs to generate
    """
    while not 1 <= device_count <= 9:
        try:
            device_count = int(input("{} IOCs currently requested. The current script requires a number"
                                         " between 1 and 9. Please enter a new value: ".format(device_count)))
        except (ValueError, TypeError) as e:
            logging.warning("That was not a valid input, please try again: {}".format(e))

    mkdir(device_info.ioc_path())

    _run_ioc_template_setup(device_info, device_count)
    _add_template_config_xml(device_info, device_count)
    _replace_macros(device_info, device_count)
    _clean_up(device_info, device_count)
    _build(device_info.ioc_path())
    _add_to_ioc_makefile(device_info.ioc_name())
    _add_macro_to_release_file(device_info)
