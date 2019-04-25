""" Test the GUI utilities """
import unittest

from mock import patch
from utils.device_info_generator import DeviceInfoGenerator
from utils.gui_utils import _generate_opi_entry, create_opi
from lxml import etree
import os


class GuiUtilsTests(unittest.TestCase):
    def setUp(self):
        self.test_device = DeviceInfoGenerator("DEVICE")

    def test_GIVEN_test_device_WHEN_an_opi_is_generated_THEN_the_output_matches_the_standard_format(self):
        # Arrange
        expected = "<entry><key>DEVICE</key><value><categories/><type>UNKNOWN</type><path>device.opi</path>" \
                   "<description>The OPI for the DEVICE</description><macros><macro><name>DEVICE</name>" \
                   "<description>The DEVICE PV prefix (e.g. DEVICE_01)</description></macro></macros></value>" \
                   "</entry>"

        # Act
        actual = etree.tostring(_generate_opi_entry(self.test_device))

        # Assert
        self.assertEqual(actual, expected)

    @patch('utils.gui_utils.copyfile')
    @patch('utils.gui_utils.replace_in_file')
    @patch('utils.gui_utils.etree')
    @patch("utils.gui_utils.open", create=True)
    def test_GIVEN_test_device_WHEN_an_opi_is_generated_THEN_created_files_returned(self, *args):
        expected_files = ['device.opi']
        opi_files = create_opi(self.test_device)

        self.assertListEqual(expected_files, [p.split(os.path.sep)[-1] for p in opi_files])
