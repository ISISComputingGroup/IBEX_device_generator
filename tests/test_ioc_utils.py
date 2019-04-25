""" Tests for the ioc utils """
import unittest

from mock import patch, mock_open
from utils.device_info_generator import DeviceInfoGenerator
from utils.ioc_utils import create_ioc
import os


class IocUtilsTest(unittest.TestCase):
    def setUp(self):
        self.test_device = DeviceInfoGenerator("DEVICE")

    @patch("utils.ioc_utils.run_command")
    @patch("utils.ioc_utils.copy_file")
    @patch("utils.ioc_utils.path.exists")
    @patch("utils.ioc_utils.replace_in_file")
    @patch("utils.ioc_utils.rmtree")
    @patch("utils.ioc_utils.remove")
    @patch("utils.ioc_utils.mkdir")
    @patch("utils.ioc_utils.open", create=True)
    def test_GIVEN_a_device_WHEN_create_single_ioc_THEN_single_ioc_created_and_ioc_files_returned(self, *args):
        no_of_devices = 1
        ioc_files = create_ioc(self.test_device, no_of_devices)

        self.assertEqual(len(ioc_files), 7)

    @patch("utils.ioc_utils.run_command")
    @patch("utils.ioc_utils.copy_file")
    @patch("utils.ioc_utils.path.exists")
    @patch("utils.ioc_utils.replace_in_file")
    @patch("utils.ioc_utils.rmtree")
    @patch("utils.ioc_utils.remove")
    @patch("utils.ioc_utils.mkdir")
    @patch("utils.ioc_utils.open", create=True)
    def test_GIVEN_a_device_WHEN_create_two_iocs_THEN_two_iocs_created_and_ioc_files_returned(self, *args):
        no_of_devices = 2
        ioc_files = create_ioc(self.test_device, no_of_devices)

        self.assertEqual(len(ioc_files), 8)
