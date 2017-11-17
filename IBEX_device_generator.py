""" Contains main method for creating a vanilla IOC from scratch """
from run_tests import run_tests
from utils import gui_utils
from utils.command_line_utils import ArgumentDescriptor, parse_args
from utils.logging_utils import logger

LOGGER = logger("IOC generator")


def generate_device(name, ticket, submodule=True, opi=True, tests=True, emulator=True):
    """
    Creates the boilerplate components for an IOC
    :param name: The name of the IOC
    :param ticket: The ticket number this relates to
    :param submodule: Whether to create a support submodule
    :param opi: Whether to create an empty OPI
    :param tests: Whether to create IOC system tests
    :param emulator: Whether to create a device emulator
    """

    branch = "Ticket{}_Add_IOC_{}".format(ticket, name)

    def create_ioc_directory():
        # Change IOC branch
        # Make the IOC directory
        # Create template IOC
        # Make any file adjustments to the IOC
        # Commit the changes to Git
        pass

    def create_support_submodule():
        # Create submodule in github
        # Change EPICS branch
        # Add repo as submodule
        # Add macro
        # Add submodule to support make file
        pass


        # Create a blank OPI file
        # Add the file to opi_info.xml
        pass

    def create_ioc_system_tests():
        # Change IOC system tests branch
        # Create a blank test directory
        # Add the tests to run_all_tests.bat
        pass

    def create_device_emulator():
        # Change device emulator branch
        pass

    create_ioc_directory()
    if submodule:
        create_support_submodule()
    if tests:
        create_ioc_system_tests()
    if emulator:
        create_device_emulator()
    if opi:
        gui_utils.create_opi(name, branch)


def main():
    """
    Routine to run when script executed from the command line
    """
    if not run_tests():
        raise AssertionError("IOC generator failed its unit tests. Please fix before running")

    args = parse_args(
        "Generate boilerplate code for IBEX device support",
        [ArgumentDescriptor("name", str, "Name of the device"), ArgumentDescriptor("ticket", int, "Ticket number")]
    )
    import utils
    utils.gui_utils.LOCAL = True
    generate_device(args.name, args.ticket)


if __name__ == "__main__":
    main()