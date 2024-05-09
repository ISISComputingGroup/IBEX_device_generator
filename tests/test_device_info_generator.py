""" Tests for the device info generator """
import unittest

from utils.device_info_generator import DeviceInfoGenerator, InvalidIOCNameError

IOC_NAME = "ioc_name"
DEVICE_NAME = "device_name"
OPI_FILE = "opi_file"
OPI_KEY = "opi_key"
LOG = "log"
IOC = "ioc"
IOC_APP = "ioc_app"
EMULATOR = "emulator"
SUPPORT = "support"
REPO = "repo"
TESTS = "test_framework"


class DeviceInfoGeneratorTests(unittest.TestCase):

    def setUp(self):
        self.test_cases = dict()
        self.test_cases["short_no_spaces"] = {
            IOC_NAME: "MYIOC",
            DEVICE_NAME: "MyIoc",
            OPI_FILE: "myioc.opi",
            OPI_KEY: "MYIOC",
            LOG: "MYIOC",
            IOC: "MYIOC",
            IOC_APP: "MYIOC-IOC-01",
            EMULATOR: "Myioc",
            SUPPORT: "myioc",
            REPO: "EPICS-MyIoc",
            TESTS: "myioc"
        }

        self.test_cases["short_spaces"] = {
            IOC_NAME: "MYIOC2",
            DEVICE_NAME: "MyIoc 2",
            OPI_FILE: "myioc2.opi",
            OPI_KEY: "MYIOC2",
            LOG: "MYIOC2",
            IOC: "MYIOC2",
            IOC_APP: "MYIOC2-IOC-01",
            EMULATOR: "Myioc2",
            SUPPORT: "myioc_2",
            REPO: "EPICS-MyIoc_2",
            TESTS: "myioc_2"
        }

        self.test_cases["short_incorrect"] = {
            IOC_NAME: "short",
            DEVICE_NAME: "short",
        }

        self.test_cases["long_incorrect"] = {
            IOC_NAME: "super_long_name",
            DEVICE_NAME: "super_long_name",
        }

        self.test_cases["with_long_name"] = {
            IOC_NAME: "MYIOC",
            DEVICE_NAME: "My Custom Device with Decription",
            OPI_FILE: "myioc.opi",
            OPI_KEY: "MYIOC",
            LOG: "MYIOC",
            IOC: "MYIOC",
            IOC_APP: "MYIOC-IOC-01",
            EMULATOR: "Myioc",
            SUPPORT: "my_custom_device_with_decription",
            REPO: "EPICS-My_Custom_Device_with_Decription",
            TESTS: "my_custom_device_with_decription"
        }

    def _test_case(self, case):
        info = DeviceInfoGenerator(case[IOC_NAME], case[DEVICE_NAME])
        self.assertEqual(case[OPI_FILE], info.opi_file_name())
        self.assertEqual(case[OPI_KEY], info.opi_key())
        self.assertEqual(case[LOG], info.log_name())
        self.assertEqual(case[IOC], info.ioc_name)
        self.assertEqual(case[IOC_APP], info.ioc_app_name(1))
        self.assertEqual(case[EMULATOR], info.emulator_name())
        self.assertEqual(case[SUPPORT], info.support_app_name())
        self.assertEqual(case[REPO], info.support_repo_name())
        self.assertEqual(case[TESTS], info.ioc_test_framework_device_name())

    def test_GIVEN_an_ioc_shorter_than_8_characters_without_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self._test_case(self.test_cases["short_no_spaces"])

    def test_GIVEN_an_ioc_shorter_than_8_characters_with_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self._test_case(self.test_cases["short_spaces"])

    def test_GIVEN_an_ioc_shorter_than_8_characters_with_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self._test_case(self.test_cases["with_long_name"])

    def test_GIVEN_an_ioc_longer_than_8_characters_with_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self.assertRaises(InvalidIOCNameError, self._test_case, self.test_cases["short_incorrect"])
        self.assertRaises(InvalidIOCNameError, self._test_case, self.test_cases["long_incorrect"])
