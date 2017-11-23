""" Contains main method for creating a vanilla IOC from scratch """
from run_tests import run_tests
from utils.common_utils import create_component
from utils.gui_utils import create_opi
from utils.emulator_utils import create_emulator
from utils.ioc_utils import create_ioc
from utils.ioc_test_framework_utils import create_test_framework
from utils.support_utils import create_submodule, apply_support_dir_template
from utils.command_line_utils import parse_args
from system_paths import CLIENT, EMULATORS_ROOT, IOC_ROOT, IOC_TEST_FRAMEWORK_ROOT, EPICS, EPICS_SUPPORT
import logging
from os.path import join
from utils.device_info_generator import DeviceInfoGenerator


def _configure_logging():
    logging.basicConfig(format="%(asctime)-15s, %(levelname)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)


def generate_device(name, ticket, device_count):
    """
    Creates the boilerplate components for an IOC

    Args:
        name: The name of the IOC
        ticket: The ticket number this relates to
        device_count: Number of IOCs to generate
    """

    _configure_logging()

    device_info = DeviceInfoGenerator(name)
    branch = "Ticket{}_Add_IOC_{}".format(ticket, device_info.ioc_name())

    create_component(device_info, branch, EPICS, create_submodule, "Add support submodule to EPICS", epics=True)
    create_component(device_info, branch, device_info.support_master_dir(),
                     apply_support_dir_template, "Creating template file structure in support submodule")
    create_component(device_info, branch, IOC_ROOT, create_ioc, "Add template IOC", device_count=device_count)
    create_component(device_info, branch, IOC_TEST_FRAMEWORK_ROOT, create_test_framework,
                     "Add device to test framework")
    create_component(device_info, branch, EMULATORS_ROOT, create_emulator, "Add template emulator")
    create_component(device_info, branch, CLIENT, create_opi, "Add template OPI file")


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
