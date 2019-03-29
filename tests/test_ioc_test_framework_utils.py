""" Tests for the ioc test framework utils """
import unittest

from mock import patch
from utils.device_info_generator import DeviceInfoGenerator
from utils.ioc_test_framework_utils import create_test_framework
import os


class IocTestFrameworkTest(unittest.TestCase):
    def setUp(self):
        self.test_device = DeviceInfoGenerator("DEVICE")

    @patch("utils.ioc_test_framework_utils.copy_file")
    @patch('utils.ioc_test_framework_utils.replace_in_file')
    def test_GIVEN_a_device_WHEN_create_ioc_test_framework_files_THEN_files_created_and_test_files_returned(self, *args):
        expected_file = ['device.py']
        test_framework_files = create_test_framework(self.test_device)

        self.assertEqual(len(test_framework_files), 1)
        self.assertListEqual(expected_file, [p.split(os.path.sep)[-1] for p in test_framework_files])
