""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import IOC_ROOT, PERL, PERL_IOC_GENERATOR, EPICS_BASE_BUILD, EPICS
from templates.paths import BASIC_DB, BASIC_CONFIG_XML
from common_utils import run_command, replace_in_file, rmtree, get_input
from os import path, mkdir, rmdir, walk
from shutil import copyfile
import logging


def _get_path(device):
    return path.join(IOC_ROOT, device)


def _check_for_ioc_dir(ioc_path):
    if path.exists(ioc_path):
        if get_input("IOC path {} already exists. Shall I try and delete it? (Y/N) ".format(ioc_path)).upper() == "Y":
            rmtree(ioc_path)
        else:
            raise RuntimeError("IOC directory {} already exists. Aborting".format(ioc_path))


def _make_ioc_dir(ioc_path):
    try:
        mkdir(ioc_path)
    except OSError as e:
        raise OSError("Unable to create directory for IOC {}: {}".format(ioc_path, e))


def _run_ioc_template_setup(device, device_count):
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
        app_name = "{}-IOC-{:02d}".format(device, i)
        logging.info("Generating IOC {}".format(app_name))
        run_command([PERL, PERL_IOC_GENERATOR, "-t", "ioc", app_name], _get_path(device))
        run_command([PERL, PERL_IOC_GENERATOR, "-i", "-t", "ioc", "-a", "IBEX", "-p", app_name, app_name],
                    _get_path(device))

    rmdir(ibex_bin)


def _add_template_db(device):
    db_dir = path.join(_get_path(device), "{}-IOC-01App".format(device), "Db")
    logging.info("Copying basic Db file to {}".format(db_dir))
    if not path.exists(db_dir):
        raise AssertionError("Tried creating basic Db file before IOC creation. Db folder {} does not exist"
                             .format(db_dir))
    copyfile(BASIC_DB, path.join(db_dir, "{}.db".format(device)))

    # Make sure Db is included in the build
    replace_in_file(path.join(db_dir, "Makefile"), [("#DB += xxx.db", "DB += {}.db".format(device))])


def _add_template_config_xml(device, device_count):
    for i in range(1, device_count+1):
        copyfile(BASIC_CONFIG_XML,
                 path.join(_get_path(device), "iocBoot", "ioc{}-IOC-{:02d}".format(device, i), "config.xml"))
    run_command(["make", "iocstartups"], EPICS)


def _replace_macros(device, device_count):
    for i in range(1, device_count+1):
        st_cmd_file = path.join(_get_path(device), "iocBoot", "ioc{}-IOC-{:02d}".format(device, i), "st.cmd")
        if not path.exists(st_cmd_file):
            AssertionError("Attempting to replace macros before command file has been created")
        replace_in_file(st_cmd_file, [("_SUPPORT_MACRO_", device), ("_DB_NAME_", device)])


def _clean_up(ioc_path):
    logging.info("Removing unnecessary files from {}".format(ioc_path))
    for root, dirs, files in walk(ioc_path):
        for d in dirs:
            if d == "protocol":
                rmtree(path.join(root, d))


def _build(ioc_path):
    run_command(["make"], ioc_path)


def _add_to_ioc_makefile(device):
    ioc_makefile = path.join(IOC_ROOT, "Makefile")
    with open(ioc_makefile) as f:
        old_lines = f.readlines()

    new_lines = []
    last_line = ""
    marker = "IOCDIRS += "
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + device)
        new_lines.append(line)

    with open(ioc_makefile, "w") as f:
        f.writelines(new_lines)


def create_ioc(device, device_count):
    """
    Creates a vanilla IOC in the EPICS IOC submodule
    :param device: Name of the device to create the emulator for
    :param device_count: Number of IOCs to generate
    """
    _check_for_ioc_dir(_get_path(device))
    _make_ioc_dir(_get_path(device))
    _run_ioc_template_setup(device, device_count)
    _add_template_db(device)
    _add_template_config_xml(device, device_count)
    _replace_macros(device, device_count)
    _clean_up(_get_path(device))
    _build(_get_path(device))
    _add_to_ioc_makefile(device)
