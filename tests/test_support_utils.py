""" Tests for the support utils """
import unittest

from mock import patch
from utils.device_info_generator import DeviceInfoGenerator
from utils.support_utils import create_submodule, create_support
import os


class SupportUtilsTest(unittest.TestCase):
    def setUp(self):
        self.test_device = DeviceInfoGenerator("DEVICE")

    @patch("utils.support_utils.mkdir")
    @patch("utils.support_utils.copy_file")
    @patch("utils.file_system_utils.open")
    def test_GIVEN_a_device_WHEN_create_submodule_and_create_submodules_false_THEN_submodule_files_returned(self, *args):
        submodule_files = create_submodule(self.test_device, create_submodule_in_git=False)
        expected_files = ['device', 'Makefile', 'Makefile']

        self.assertEqual(len(submodule_files), 3)
        self.assertListEqual(expected_files, [p.split(os.path.sep)[-1] for p in submodule_files])

    @patch("utils.support_utils.mkdir")
    @patch("utils.support_utils.copy_file")
    @patch("utils.support_utils.get_input")
    @patch("utils.file_system_utils.open")
    @patch("utils.git_utils.RepoWrapper.create_submodule")
    def test_GIVEN_a_device_WHEN_create_submodule_and_create_submodules_true_THEN_submodule_files_returned(self, *args):
        submodule_files = create_submodule(self.test_device, create_submodule_in_git=True)
        expected_files = ['.gitmodules', 'device', 'Makefile', 'Makefile']

        self.assertEqual(len(submodule_files), 4)
        self.assertListEqual(expected_files, [p.split(os.path.sep)[-1] for p in submodule_files])

    @patch("utils.support_utils.mkdir")
    @patch("utils.support_utils.copy_file")
    @patch("utils.support_utils.run_command")
    @patch("utils.support_utils.replace_in_file")
    @patch("utils.support_utils.remove")
    @patch("utils.support_utils.path.exists")
    def test_GIVEN_a_device_WHEN_apply_support_dir_template_THEN_submodule_files_returned(self, *args):
        submodule_files = create_support(self.test_device)
        expected_files = ['Makefile', '.gitignore', 'master', 'LICENCE', 'device.db']

        self.assertEqual(len(submodule_files), 5)
        self.assertListEqual(expected_files, [p.split(os.path.sep)[-1] for p in submodule_files])
