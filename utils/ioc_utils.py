""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import IOC_ROOT, PERL, PERL_IOC_GENERATOR, EPICS_BASE_BUILD, EPICS
from templates.paths import DB, CONFIG_XML
from common_utils import run_command
from file_system_utils import replace_in_file, rmtree, get_input, mkdir, copy_file, add_to_makefile_list
from os import path, walk
import logging


def _run_ioc_template_setup(device_info, device_count):
    """
    Runs the EPICS perl scripts associated with IOC creation. Passes in the IBEX type flag to use our own templates
    found in C:\\Instrument\\Apps\\EPICS\\base\\master\\templates
    """
    if device_count > 99:
        raise ValueError("Cannot generate more than 99 IOCs for a single device")

    # Needed or makeBaseApp.pl won't permit use of the IBEX templates in IOCBOOT
    ibex_bin = path.join(EPICS_BASE_BUILD, "IBEX")
    if not path.exists(ibex_bin):
        mkdir(ibex_bin)

    for i in range(1, device_count+1):
        app_name = device_info.ioc_app_name(i)
        logging.info("Generating IOC {}".format(app_name))
        run_command([PERL, PERL_IOC_GENERATOR, "-t", "ioc", app_name], device_info.ioc_path())
        run_command([PERL, PERL_IOC_GENERATOR, "-i", "-t", "ioc", "-a", "IBEX", "-p", app_name, app_name],
                    device_info.ioc_path())

    rmtree(ibex_bin)


def _add_template_db(device_info):
    db_dir = path.join(device_info.ioc_path(), "{}App".format(device_info.ioc_app_name(1)), "Db")
    logging.info("Copying basic Db file to {}".format(db_dir))
    copy_file(DB, path.join(db_dir, "{}.db".format(device_info.ioc_name())))

    # Make sure Db is included in the build
    replace_in_file(path.join(db_dir, "Makefile"), [("#DB += xxx.db", "DB += {}.db".format(device_info.ioc_name()))])


def _add_template_config_xml(device_info, device_count):
    for i in range(1, device_count+1):
        copy_file(CONFIG_XML, path.join(device_info.ioc_boot_path(i), "config.xml"))
    run_command(["make", "iocstartups"], EPICS)


def _replace_macros(device_info, device_count):
    for i in range(1, device_count+1):
        st_cmd_file = path.join(device_info.ioc_boot_path(i), "st.cmd")
        if not path.exists(st_cmd_file):
            AssertionError("Attempting to replace macros before command file has been created")
        replace_in_file(st_cmd_file, [("_SUPPORT_MACRO_", device_info.ioc_name()),
                                      ("_DB_NAME_", device_info.ioc_name())])


def _clean_up(ioc_path):
    logging.info("Removing unnecessary files from {}".format(ioc_path))
    for root, dirs, files in walk(ioc_path):
        for d in dirs:
            if d == "protocol":
                rmtree(path.join(root, d))


def _build(ioc_path):
    run_command(["make"], ioc_path)


def _add_to_ioc_makefile(device_info):
    add_to_makefile_list(IOC_ROOT, "IOCDIRS", device_info.ioc_name())


def create_ioc(device_info, device_count):
    """
    Creates a vanilla IOC in the EPICS IOC submodule
    :param device_info: Provides name-based information about the device
    :param device_count: Number of IOCs to generate
    """
    while not 1 <= device_count <= 9:
        try:
            device_count = int(get_input("{} IOCs currently requested. The current script requires a number"
                                         " between 1 and 9. Please enter a new value: ".format(device_count)))
        except (ValueError, TypeError) as e:
            logging.warning("That was not a valid input, please try again: {}".format(e))

    mkdir(device_info.ioc_path())

    _run_ioc_template_setup(device_info, device_count)
    _add_template_db(device_info)
    _add_template_config_xml(device_info, device_count)
    _replace_macros(device_info, device_count)
    _clean_up(device_info.ioc_path())
    _build(device_info.ioc_path())
    _add_to_ioc_makefile(device_info)
