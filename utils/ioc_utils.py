""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import IOC_ROOT, PERL, PERL_IOC_GENERATOR, EPICS_BASE_BUILD, EPICS
from templates.paths import DB, CONFIG_XML
from common_utils import run_command
from file_system_utils import replace_in_file, rmtree, get_input, mkdir
from os import path, walk
from shutil import copyfile
import logging
from device_info_generator import DeviceInfoGenerator


def _run_ioc_template_setup(info_generator, device_count):
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
        app_name = info_generator.ioc_app_name(i)
        logging.info("Generating IOC {}".format(app_name))
        run_command([PERL, PERL_IOC_GENERATOR, "-t", "ioc", app_name], info_generator.ioc_path())
        run_command([PERL, PERL_IOC_GENERATOR, "-i", "-t", "ioc", "-a", "IBEX", "-p", app_name, app_name],
                    info_generator.ioc_path())

    rmtree(ibex_bin)


def _add_template_db(info_generator):
    db_dir = path.join(info_generator.ioc_path(), "{}App".format(info_generator.ioc_app_name(1)), "Db")
    logging.info("Copying basic Db file to {}".format(db_dir))
    if not path.exists(db_dir):
        raise AssertionError("Tried creating basic Db file before IOC creation. Db folder {} does not exist"
                             .format(db_dir))
    copyfile(DB, path.join(db_dir, "{}.db".format(info_generator.ioc_name())))

    # Make sure Db is included in the build
    replace_in_file(path.join(db_dir, "Makefile"), [("#DB += xxx.db", "DB += {}.db".format(info_generator.ioc_name()))])


def _add_template_config_xml(info_generator, device_count):
    for i in range(1, device_count+1):
        copyfile(CONFIG_XML,
                 path.join(info_generator.ioc_path(), "iocBoot", info_generator.ioc_app_name(i), "config.xml"))
    run_command(["make", "iocstartups"], EPICS)


def _replace_macros(info_generator, device_count):
    for i in range(1, device_count+1):
        st_cmd_file = path.join(info_generator.ioc_path(), "iocBoot", info_generator.ioc_app_name(i), "st.cmd")
        if not path.exists(st_cmd_file):
            AssertionError("Attempting to replace macros before command file has been created")
        replace_in_file(st_cmd_file, [("_SUPPORT_MACRO_", info_generator.ioc_name()),
                                      ("_DB_NAME_", info_generator.ioc_name())])


def _clean_up(ioc_path):
    logging.info("Removing unnecessary files from {}".format(ioc_path))
    for root, dirs, files in walk(ioc_path):
        for d in dirs:
            if d == "protocol":
                rmtree(path.join(root, d))


def _build(ioc_path):
    run_command(["make"], ioc_path)


def _add_to_ioc_makefile(info_generator):
    ioc_makefile = path.join(IOC_ROOT, "Makefile")
    with open(ioc_makefile) as f:
        old_lines = f.readlines()

    new_lines = []
    last_line = ""
    marker = "IOCDIRS += "
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + info_generator.ioc_name())
        new_lines.append(line)

    with open(ioc_makefile, "w") as f:
        f.writelines(new_lines)


def create_ioc(device, device_count):
    """
    Creates a vanilla IOC in the EPICS IOC submodule
    :param device: Name of the device to create the emulator for
    :param device_count: Number of IOCs to generate
    """
    while not 1 <= device_count <= 9:
        try:
            device_count = int(get_input("{} IOCs currently requested. The current script requires a number"
                                         " between 1 and 9. Please enter a new value: ".format(device_count)))
        except (ValueError, TypeError) as e:
            logging.warning("That was not a valid input, please try again: {}".format(e))

    info_generator = DeviceInfoGenerator(device)
    mkdir(info_generator.ioc_path())

    _run_ioc_template_setup(info_generator, device_count)
    _add_template_db(info_generator)
    _add_template_config_xml(info_generator, device_count)
    _replace_macros(info_generator, device_count)
    _clean_up(info_generator.ioc_path())
    _build(info_generator.ioc_path())
    _add_to_ioc_makefile(info_generator)
