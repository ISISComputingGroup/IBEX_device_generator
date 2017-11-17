""" Contains main method for creating a vanilla IOC from scratch """
from logging_utils import logger
from run_tests import run_tests
from utils import gui_utils

LOGGER = logger("IOC generator")


def build_ioc(name, ticket, submodule=True, opi=True, tests=True, emulator=True):
    """
    Creates the boilerplate components for an IOC
    :param name: The name of the IOC
    :param ticket: The ticket number this relates to
    :param submodule: Whether to create a support submodule
    :param opi: Whether to create an empty OPI
    :param tests: Whether to create IOC system tests
    :param emulator: Whether to create a device emulator
    """
    if not run_tests():
        raise AssertionError("IOC generator failed its unit tests. Please fix before running")

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
