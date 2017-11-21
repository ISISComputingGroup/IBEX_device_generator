""" Helper to generate information about the device based on the name used in device setup """
from os.path import join
from system_paths import OPI_RESOURCES
from common_utils import get_input
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
        self._user_supplied_ioc_name = None

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
        return self._title_case_with_spaces()

    @staticmethod
    def _is_valid_ioc_name(name):
        """
        :param name: Name to check for validity
        :return: True is name valid, else False
        """
        return name.isalnum() and name.upper() == name and 1 <= name <= 8

    def ioc_name(self):
        """
        :return: The name of the IOC based on the input name. Must be between 1 and 8 characters
        """
        if self._is_valid_ioc_name(self._upper_case_spaces_removed_no_truncation()):
            ioc_name = self._upper_case_spaces_removed_no_truncation()
        elif self._user_supplied_ioc_name is not None:
            ioc_name = self._user_supplied_ioc_name
        else:
            self._user_supplied_ioc_name = self._name
            while self._is_valid_ioc_name(self._user_supplied_ioc_name):
                self._user_supplied_ioc_name = get_input(
                    "Device name, {}, is invalid. Please enter a valid IOC name: ".format(self._user_supplied_ioc_name))
            ioc_name = self._user_supplied_ioc_name
        return ioc_name

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
