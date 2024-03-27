""" Tests for the device info generator """
import unittest

from mock import patch

from utils.device_info_generator import DeviceInfoGenerator

RAW = "raw"
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
        self.test_cases["short_no_spaces"] =\
            {RAW: "MyIoc", OPI_FILE: "myioc.opi", OPI_KEY: "MYIOC", LOG: "MyIoc", IOC: "MYIOC",
             IOC_APP: "MYIOC-IOC-01", EMULATOR: "Myioc", SUPPORT: "myioc", REPO: "EPICS-Myioc",
             TESTS: "myioc"}

        self.test_cases["short_spaces"] =\
            {RAW: "MyIoc 2", OPI_FILE: "myioc_2.opi", OPI_KEY: "MYIOC2", LOG: "MyIoc 2", IOC: "MYIOC2",
             IOC_APP: "MYIOC2-IOC-01", EMULATOR: "Myioc2", SUPPORT: "myioc_2", REPO: "EPICS-Myioc2",
             TESTS: "myioc_2"}

        self.test_cases["long_spaces"] =\
            {RAW: "super_long_name", OPI_FILE: "short.opi", OPI_KEY: "SHORT",
             LOG: "short", IOC: "SHORT", IOC_APP: "SHORT-IOC-01", EMULATOR: "Short",
             SUPPORT: "short", REPO: "EPICS-Short", TESTS: "short"}

    def _test_case(self, case):
        info = DeviceInfoGenerator(case[RAW], False)
        self.assertEqual(case[OPI_FILE], info.opi_file_name())
        self.assertEqual(case[OPI_KEY], info.opi_key())
        self.assertEqual(case[LOG], info.log_name())
        self.assertEqual(case[IOC], info.ioc_name())
        self.assertEqual(case[IOC_APP], info.ioc_app_name(1, auto=True))
        self.assertEqual(case[EMULATOR], info.emulator_name())
        self.assertEqual(case[SUPPORT], info.support_app_name())
        self.assertEqual(case[REPO], info.support_repo_name())
        self.assertEqual(case[TESTS], info.ioc_test_framework_device_name())

    def test_GIVEN_an_ioc_shorter_than_8_characters_without_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self._test_case(self.test_cases["short_no_spaces"])

    def test_GIVEN_an_ioc_shorter_than_8_characters_with_spaces_THEN_info_names_match_values_as_defined_in_test_case(self):
        self._test_case(self.test_cases["short_spaces"])

    @patch("utils.device_info_generator.input")
    def test_GIVEN_an_ioc_longer_than_8_characters_with_spaces_THEN_info_names_match_values_as_defined_in_test_case(self, input):
        input.return_value = "short"
        self._test_case(self.test_cases["long_spaces"])
