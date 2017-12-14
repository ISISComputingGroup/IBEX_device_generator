""" Test the GUI utilities """
import unittest
from utils.gui_utils import _generate_opi_entry
from lxml import etree


class GuiUtilsTests(unittest.TestCase):

    def test_GIVEN_simple_opi_properties_WHEN_an_opi_is_generated_THEN_the_output_matches_the_standard_format(self):
        # Arrange
        expected = "<entry><key>RING</key><value><categories/><type>UNKNOWN</type><path>sauron.opi</path>" \
                   "<description>The OPI for the the one ring</description><macros><macro><name>RING</name>" \
                   "<description>The the one ring PV prefix (e.g. RING_01)</description></macro></macros></value>" \
                   "</entry>"

        # Act
        actual = etree.tostring(_generate_opi_entry("RING", "sauron.opi", "the one ring", "RING"))

        # Assert
        self.assertEqual(actual, expected)
