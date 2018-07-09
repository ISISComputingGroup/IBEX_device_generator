""" Contains main method for creating a vanilla IOC from scratch """
import argparse

from run_tests import run_tests
from utils.common_utils import create_component
from utils.gui_utils import create_opi
from utils.emulator_utils import create_emulator
from utils.ioc_utils import create_ioc
from utils.ioc_test_framework_utils import create_test_framework
from utils.support_utils import create_submodule, apply_support_dir_template
from system_paths import CLIENT, EMULATORS_ROOT, IOC_ROOT, IOC_TEST_FRAMEWORK_ROOT, EPICS
import logging
from utils.device_info_generator import DeviceInfoGenerator


def _configure_logging():
    logging.basicConfig(format="%(asctime)-15s, %(levelname)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)


def generate_device(name, ticket, device_count, use_git):
    """
    Creates the boilerplate components for an IOC

    Args:
        name: The name of the IOC
        ticket: The ticket number this relates to
        device_count: Number of IOCs to generate
        use_git: use git, if True create branch commit and pu; if false do nothing with git
    """

    _configure_logging()

    device_info = DeviceInfoGenerator(name)
    branch = "Ticket{}_Add_IOC_{}".format(ticket, device_info.ioc_name())

    create_component(device_info, branch, EPICS, create_submodule, "Add support submodule to EPICS", use_git, use_git)
    create_component(device_info, branch, device_info.support_master_dir(),
                     apply_support_dir_template, "Creating template file structure in support submodule", use_git)
    create_component(device_info, branch, IOC_ROOT, create_ioc, "Add template IOC", use_git, device_count=device_count)
    create_component(device_info, branch, IOC_TEST_FRAMEWORK_ROOT, create_test_framework,
                     "Add device to test framework", use_git)
    create_component(device_info, branch, EMULATORS_ROOT, create_emulator, "Add template emulator", use_git)
    create_component(device_info, branch, CLIENT, create_opi, "Add template OPI file", use_git)


def main():
    """
    Routine to run when script executed from the command line
    """
    if not run_tests():
        raise AssertionError("IOC generator failed its unit tests. Please fix before running")

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Generate boilerplate code for IBEX device support")
    parser.add_argument("--name", type=str, help="Name of the device", required=True)
    parser.add_argument("--ticket", type=int, help="Ticket number", required=True)
    parser.add_argument("--device_count", type=int, help="Number of duplicate IOCs to generate", default=2)
    parser.add_argument("--no_git", action='store_true', help="Use to not create a branch or push to git")

    args = parser.parse_args()
    generate_device(args.name, args.ticket, args.device_count, not args.no_git)


if __name__ == "__main__":
    main()
