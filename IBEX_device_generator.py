""" Contains main method for creating a vanilla IOC from scratch """
import argparse

from run_tests import run_tests
from utils.common_utils import create_component
from utils.gui_utils import create_opi
from utils.emulator_utils import create_emulator
from utils.ioc_utils import create_ioc
from utils.ioc_test_framework_utils import create_test_framework
from utils.support_utils import create_submodule, apply_support_dir_template
from system_paths import CLIENT, IOC_ROOT, EPICS
import logging
from utils.device_info_generator import DeviceInfoGenerator
from utils.requests_utils import create_github_repository


def _configure_logging():
    logging.basicConfig(format="%(asctime)-15s, %(levelname)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)


def generate_device(name, ticket, device_count, use_git, github_token):
    """
    Creates the boilerplate components for an IOC

    Args:
        name: The name of the IOC
        ticket: The ticket number this relates to
        device_count: Number of IOCs to generate
        use_git: use git, if True then create branch, commit and push; if false do nothing with git
        github_token: If set creates GitHub repository
    """

    _configure_logging()

    device_info = DeviceInfoGenerator(name)
    branch = "Ticket{}_Add_IOC_{}".format(ticket, device_info.ioc_name())
    create_component(device_info, branch, device_info.support_master_dir(), create_github_repository,
                     "Create github repository", False, github_token=github_token)
    create_component(device_info, branch, EPICS, create_submodule, "Add support submodule to EPICS", use_git,
                     create_submodule_in_git=use_git)
    create_component(device_info, branch, device_info.support_master_dir(),
                     apply_support_dir_template, "Creating template file structure in support submodule", use_git)
    create_component(device_info, branch, IOC_ROOT, create_ioc, "Add template IOC", use_git, device_count=device_count)
    create_component(device_info, branch, device_info.support_master_dir(), create_test_framework,
                     "Add device to test framework", use_git)
    create_component(device_info, branch, device_info.support_master_dir(), create_emulator, "Add template emulator",
                     use_git)
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
    parser.add_argument("--use_git", action='store_true', help="Use to create relevant branches. Remote repository must exist")
    parser.add_argument("--github_token", type=str, help="GitHub token with \"repo\" scope. Use to create support repository")

    args = parser.parse_args()
    generate_device(args.name, args.ticket, args.device_count, args.use_git, args.github_token)


if __name__ == "__main__":
    main()
