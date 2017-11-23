""" Helper to generate information about the device based on the name used in device setup """
from os.path import join
from system_paths import OPI_RESOURCES, EPICS, EPICS_SUPPORT, IOC_TEST_FRAMEWORK_ROOT
from command_line_utils import get_input
from system_paths import LEWIS_EMULATORS


class DeviceInfoGenerator(object):
    """
    Generates info used in setting up a device under IBEX based on the name
    """

    def __init__(self, raw_name):
        """
        :param raw_name: The raw input name of the device
        """
        self._name = raw_name
        self._ioc_name = None

    def _lower_case_underscore_separated_name(self):
        """
        :return: The name in lower case with spaces replaced by underscores
        """
        return self._name.lower().replace(" ", "_")

    def _title_case_with_spaces(self):
        """
        :return: The name of the device in title case with spaces left in
        """
        return self._name.title()

    def _title_case_no_spaces(self):
        """
        :return: The name of the device in title case with spaces removed
        """
        return self._name.title().replace(" ", "")

    def _upper_case_spaces_removed_no_truncation(self):
        """
        :return: The name of the device in upper case but not shortened in any other way
        """
        return self._name.upper().replace(" ", "")

    def _original_case_no_spaces(self):
        """
        :return: The name of the device in its original case with spaces removed
        """
        return self._name.replace(" ", "")

    def opi_file_name(self):
        """
        :return: The name of the OPI file for this device
        """
        return "{}.opi".format(self._lower_case_underscore_separated_name())

    def opi_file_path(self):
        """
        :return: The path to the opi file for this device
        """
        return join(OPI_RESOURCES, self.opi_file_name())

    def opi_key(self):
        """
        :return: The key used for identifying the OPI in the GUI
        """
        return self._upper_case_spaces_removed_no_truncation()

    def log_name(self):
        """
        :return: The name of the device used to identify it in the logs
        """
        return self._name

    @staticmethod
    def _is_valid_ioc_name(name, auto=False):
        """
        :param name: Name to check for validity
        :param auto: Accept the default name automatically
        :return: True is name valid, else False
        """
        return name.isalnum() and name.upper() == name and 1 <= len(name) <= 8

    def _auto_generated_ioc_name(self):
        """
        :return: An auto-generated valid IOC name
        """
        import re
        name = re.sub(r'\W+', '', self._name)  # Make alphanumeric
        name = name.upper()
        name = name.replace(' ', '')
        name = name[:8]
        assert self._is_valid_ioc_name(name)
        return name


    def ioc_name(self, auto=False):
        """
        :param auto: Accept the auto-generated name
        :return: The name of the IOC based on the input name. Must be between 1 and 8 characters
        """
        if self._ioc_name is None:
            default_ioc_name = self._upper_case_spaces_removed_no_truncation()
            if self._is_valid_ioc_name(default_ioc_name):
                proposed_name = default_ioc_name
            elif auto:
                proposed_name = self._auto_generated_ioc_name()
            else:
                proposed_name = default_ioc_name
                while not self._is_valid_ioc_name(proposed_name):
                    proposed_name = get_input(
                        "Device name, {}, is invalid. Please enter a valid IOC name: ".format(self._ioc_name))
            self._ioc_name = proposed_name
        return self._ioc_name

    def emulator_dir(self):
        """
        :return: The directory of the Lewis emulator for the device
        """
        return join(LEWIS_EMULATORS, self._lower_case_underscore_separated_name())

    def emulator_name(self):
        """
        :return: The device name used for the lewis emulator
        """
        return self._title_case_no_spaces()

    def ioc_path(self, auto=False):
        """
        :param auto: Accept the auto-generated IOC name by default
        :return: The path to the IOC
        """
        return join(EPICS, "ioc", "master", self.ioc_name(auto))

    def ioc_app_name(self, index, auto=False):
        """
        :param auto: Accept the auto-generated IOC name by default
        :param index: The IOC application name for the given index
        :return: The name of the application
        """
        return "{}-IOC-{:02d}".format(self.ioc_name(auto), index)

    def support_dir(self):
        """
        :return: The path to the support directory for the device
        """
        return join(EPICS_SUPPORT, self.support_app_name())

    def support_master_dir(self):
        """
        :return: The path to the support submodule "master" submodule folder
        """
        return join(self.support_dir(), "master")

    def support_repo_name(self):
        """
        :return: The name of the support repo for the device
        """
        return "EPICS-{}".format(self._title_case_no_spaces())

    def support_repo_url(self):
        """
        :return: The URL to the support repo
        """
        return "https://github.com/ISISComputingGroup/{}.git".format(self.support_repo_name())

    def ioc_test_framework_device_name(self):
        """
        :return: The name used to identify the device in the IOC test framework
        """
        return self._lower_case_underscore_separated_name()

    def ioc_test_framework_file_path(self):
        """
        :return: The path to the IOC test framework test case file
        """
        return join(IOC_TEST_FRAMEWORK_ROOT, "tests", "{}.py".format(self.ioc_test_framework_device_name()))

    def test_class_identifier(self):
        """
        :return: The name prepended to the IOC test framework test class
        """
        return self._title_case_no_spaces()

    def support_app_name(self):
        """
        :return: The name used to identify the device within the support submodule
        """
        return self._lower_case_underscore_separated_name()

    def support_db_path(self):
        """
        :return: Path to the support DB generated by the makeSupport.pl script
        """
        return join(self.support_master_dir(), "{}Sup".format(self.support_app_name()),
                    "dev{}.db".format(self.support_app_name()))

    def ioc_boot_path(self, index):
        """
        :param index: Index of the IOC
        :return: Path to the iocboot directory
        """
        return join(self.ioc_path(), "iocBoot", "ioc{}".format(self.ioc_app_name(index)))