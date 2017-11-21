""" Contains main method for creating a vanilla IOC from scratch """
from run_tests import run_tests
from utils.common_utils import create_component
from utils.gui_utils import create_opi
from utils.emulator_utils import create_emulator
from utils.ioc_utils import create_ioc
from utils.ioc_test_framework_utils import create_test_framework
from utils.submodule_utils import create_submodule, set_up_template_support_directory
from utils.command_line_utils import parse_args
from system_paths import CLIENT, EMULATORS_ROOT, IOC_ROOT, IOC_TEST_FRAMEWORK_ROOT, EPICS, EPICS_SUPPORT
import logging
from os.path import join

def _configure_logging():
    logging.basicConfig(format="%(asctime)-15s, %(levelname)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)


def generate_device(name, ticket, device_count, submodule=True, opi=True, tests=True, emulator=True):
    """
    Creates the boilerplate components for an IOC
    :param name: The name of the IOC
    :param ticket: The ticket number this relates to
    :param device_count: Number of IOCs to generate
    :param submodule: Whether to create a support submodule
    :param opi: Whether to create an empty OPI
    :param tests: Whether to create IOC system tests
    :param emulator: Whether to create a device emulator
    """

    _configure_logging()

    underscore_separated_name = name.lower().replace(" ", "_")
    camel_case_name = name.title().replace(" ", "")
    capitals_name = name.upper().replace(" ", "")
    branch = "Ticket{}_Add_IOC_{}".format(ticket, camel_case_name)

    # create_component(capitals_name, branch, IOC_ROOT, create_ioc, "Add template IOC", device_count=device_count)
    if submodule:
        create_component(underscore_separated_name, branch, EPICS, create_submodule, "Add support submodule to EPICS", epics=True)
        create_component(underscore_separated_name, branch, join(EPICS_SUPPORT, underscore_separated_name, "master"),
                         set_up_template_support_directory, "Creating support submodule template")
    #if tests:
    #    create_component(underscore_separated_name, branch, IOC_TEST_FRAMEWORK_ROOT, create_test_framework,
    #                     "Add device to test framework")
    # if emulator:
    #     create_component(camel_case_name, branch, EMULATORS_ROOT, create_emulator, "Add template emulator")
    # if opi:
    #     create_component(underscore_separated_name, branch, CLIENT, create_opi, "Add template OPI file")


def main():
    """
    Routine to run when script executed from the command line
    """
    if not run_tests():
        raise AssertionError("IOC generator failed its unit tests. Please fix before running")

    args = parse_args(
        "Generate boilerplate code for IBEX device support",
        [{"name": "name", "type": str, "description": "Name of the device"},
         {"name": "ticket", "type": int, "description": "Ticket number"},
         {"name": "device_count", "type": int, "description": "Number of duplicate IOCs to generate", "default": 2}]
    )
    generate_device(args.name, args.ticket, args.device_count)


if __name__ == "__main__":
    main()
