""" Helper to generate information about the device based on the name used in device setup """
from os.path import join
from system_paths import OPI_RESOURCES, EPICS, EPICS_SUPPORT
from utils.command_line_utils import get_input


class DeviceInfoGenerator(object):
    """
    Generates info used in setting up a device under IBEX based on the name
    """

    def __init__(self, raw_name):
        """
        Args:
            raw_name: The raw input name of the device
        """
        self._name = raw_name
        self._ioc_name = None

        while True:
            proposed_name = self.ioc_name()
            if self._is_valid_ioc_name(proposed_name):
                break
            self._name = get_input(
                "Device name, {}, is invalid and produces an invalid IOC name {}. Please enter a valid device name: ".
                format(self._name, proposed_name))

    def _lower_case_underscore_separated_name(self):
        """
        Returns: The name in lower case with spaces replaced by underscores
        """
        return self._name.lower().replace(" ", "_")

    def _title_case_with_spaces(self):
        """
        Returns: The name of the device in title case with spaces left in
        """
        return self._name.title()

    def _title_case_no_spaces(self):
        """
        Returns: The name of the device in title case with spaces removed
        """
        return self._name.title().replace(" ", "")

    def _upper_case_spaces_removed_no_truncation(self):
        """
        Returns: The name of the device in upper case but not shortened in any other way
        """
        return self._name.upper().replace(" ", "")

    def _original_case_no_spaces(self):
        """
        Returns: The name of the device in its original case with spaces removed
        """
        return self._name.replace(" ", "")

    def opi_file_name(self):
        """
        Returns: The name of the OPI file for this device
        """
        return "{}.opi".format(self._lower_case_underscore_separated_name())

    def opi_file_path(self):
        """
        Returns: The path to the opi file for this device
        """
        return join(OPI_RESOURCES, self.opi_file_name())

    def opi_key(self):
        """
        Returns: The key used for identifying the OPI in the GUI
        """
        return self._upper_case_spaces_removed_no_truncation()

    def log_name(self):
        """
        Returns: The name of the device used to identify it in the logs
        """
        return self._name

    @staticmethod
    def _is_valid_ioc_name(name):
        """
        Args:
            name: Name to check for validity

        Returns: True is name valid, else False
        """
        return name.isalnum() and name.upper() == name and 1 <= len(name) <= 8

    def _auto_generated_ioc_name(self):
        """
        Returns: An auto-generated valid IOC name
        """
        import re
        name = re.sub(r'\W+', '', self._name)  # Make alphanumeric
        name = name.upper()
        name = name.replace(' ', '')
        name = name[:8]
        assert self._is_valid_ioc_name(name)
        return name

    def ioc_name(self):
        """
        Returns: The name of the IOC based on the input name. Must be between 1 and 8 characters
        """
        return self._upper_case_spaces_removed_no_truncation()

    def emulator_dir(self):
        """
        Returns: The directory of the Lewis emulator for the device
        """
        return join(self.support_master_dir(), "system_tests", "lewis_emulators", self._lower_case_underscore_separated_name())

    def emulator_name(self):
        """
        Returns: The device name used for the lewis emulator
        """
        return self._title_case_no_spaces()

    def ioc_path(self):
        """
        Args:
            auto: Accept the auto-generated IOC name by default

        Returns: The path to the IOC
        """
        return join(EPICS, "ioc", "master", self.ioc_name())

    def ioc_app_name(self, index, auto=False):
        """
        Args:
            auto: Accept the auto-generated IOC name by default
            index: The IOC application name for the given index

        Returns: The name of the application
        """
        return "{}-IOC-{:02d}".format(self.ioc_name(), index)

    def support_dir(self):
        """
        Returns: The path to the support directory for the device
        """
        return join(EPICS_SUPPORT, self.support_app_name())

    def support_master_dir(self):
        """
        Returns: The path to the support submodule "master" submodule folder
        """
        return join(self.support_dir(), "master")

    def support_repo_name(self):
        """
        Returns: The name of the support repo for the device
        """
        return "EPICS-{}".format(self._title_case_no_spaces())

    def support_repo_url(self):
        """
        Returns: The URL to the support repo
        """
        return "https://github.com/ISISComputingGroup/{}.git".format(self.support_repo_name())

    def ioc_test_framework_device_name(self):
        """
        Returns: The name used to identify the device in the IOC test framework
        """
        return self._lower_case_underscore_separated_name()

    def ioc_test_framework_file_path(self):
        """
        Returns: The path to the IOC test framework test case file
        """
        return join(self.support_master_dir(), "system_tests", "tests", "{}.py".format(self.ioc_test_framework_device_name()))

    def ioc_test_framework_folder_path(self):
        """
        Returns: The path to the IOC system tests folder
        """
        return join(self.support_master_dir(), "system_tests", "tests")

    def ioc_test_framework_run_script_path(self):
        """
        Returns: The path to the IOC system tests run script
        """
        return join(self.support_master_dir(), "system_tests", "run_tests.bat")

    def test_class_identifier(self):
        """
        Returns: The name prepended to the IOC test framework test class
        """
        return self._title_case_no_spaces()

    def support_app_name(self):
        """
        Returns: The name used to identify the device within the support submodule
        """
        return self._lower_case_underscore_separated_name()

    def support_app_path(self):
        """
        Returns: Path to the support application in device submodule
        e.g. C:\Instrument\Apps\EPICS\support\gemorc\master\gemorcSup
        """
        return join(self.support_master_dir(), "{}Sup".format(self.support_app_name()))

    def support_db_path(self):
        """
        Returns: Path to the support DB generated by the makeSupport.pl script
        """
        return join(self.support_app_path(), "{}.db".format(self.support_app_name()))

    def ioc_boot_path(self, index):
        """
        Args:
            index: Index of the IOC

        Returns: Path to the iocboot directory
        """
        return join(self.ioc_path(), "iocBoot", "ioc{}".format(self.ioc_app_name(index)))

    def ioc_src_path(self, index):
        """
        Args:
            index: Index of the IOC

        Returns: Path to the ioc source directory
        """
        return join(self.ioc_path(), "{}App".format(self.ioc_app_name(index)), "src")
