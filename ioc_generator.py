""" Contains main method for creating a vanilla IOC from scratch """
from logging_utils import logger
from run_tests import run_tests

LOGGER = logger("IOC generator")


def build_ioc(name, ticket=None, submodule=True, opi=True, tests=True, emulator=True):
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

    def create_opi():
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
        create_opi()