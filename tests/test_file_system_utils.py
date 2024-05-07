""" Test auxillary methods from File System Utils """
import unittest
from utils.file_system_utils import _add_entry_to_list


class FileSystemUtilsTests(unittest.TestCase):

    def test_GIVEN_entry_and_list_name_WHEN_add_entry_to_list_text_THEN_entry_is_added_at_end_of_list(self):
        # Arrange
        device_name = "NEW_IOC"
        list_name = "IOCDIRS"
        iocdirs_input = [
            "{} += OLD_IOC\n".format(list_name),
            "\n",
        ]

        # Act
        actual_output = _add_entry_to_list(iocdirs_input, list_name, device_name)

        # Assert
        self.assertEqual("{} += {}\n".format(list_name, device_name), actual_output[1])

    def test_GIVEN_entry_list_name_and_realistic_make_text_WHEN_add_entry_to_list_text_THEN_entry_exists_in_list_text(self):
        # Arrange
        device_name = "NEW_IOC"
        list_name = "IOCDIRS"
        iocdirs_input = [
            "BUILDING_SHARED = YES",
            "endif",
            "",
            "## list all valid IOC directories that we may want to build at some point",
            "{} = AG33220A AG3631A AG53220A CCD100 CONEXAGP CONTROLSVCS CRYVALVE",
            "{} += HAMEG8123 HIFIMAG HLG HVCAEN INHIBITR INSTETC INSTRON ISISDAE",
            "{} += MCLEN MERCURY_ITC MK2CHOPR MK3CHOPR NANODAC NEOCERA PDR2000 PIMOT PSCTRL",
            "{} += RUNCTRL SCIMAG3D SDTEST SKFCHOPPER SMC100 SPINFLIPPER306015 STPS350 STSR400",
            "{} += ROTSC AMINT2L SPRLG FERMCHOP SAMPOS RKNPS CYBAMAN EGXCOLIM IEG",
            "",
            "## check on missing directories"
        ]
        iocdirs_input = [l.format(list_name) for l in iocdirs_input]

        # Act
        actual_output = _add_entry_to_list(iocdirs_input, list_name, device_name)

        # Assert
        self.assertTrue(any([device_name in l for l in actual_output]))
    
    def test_GIVEN_entry_list_name_exists_and_realistic_make_text_WHEN_add_entry_to_list_text_THEN_entry_is_not_duplicated_in_list_text(self):
        # Arrange
        device_name = "MCLEN"
        list_name = "IOCDIRS"
        iocdirs_input = [
            "BUILDING_SHARED = YES",
            "endif",
            "",
            "## list all valid IOC directories that we may want to build at some point",
            "{} = AG33220A AG3631A AG53220A CCD100 CONEXAGP CONTROLSVCS CRYVALVE",
            "{} += HAMEG8123 HIFIMAG HLG HVCAEN INHIBITR INSTETC INSTRON ISISDAE",
            "{} += MCLEN MERCURY_ITC MK2CHOPR MK3CHOPR NANODAC NEOCERA PDR2000 PIMOT PSCTRL",
            "{} += RUNCTRL SCIMAG3D SDTEST SKFCHOPPER SMC100 SPINFLIPPER306015 STPS350 STSR400",
            "{} += ROTSC AMINT2L SPRLG FERMCHOP SAMPOS RKNPS CYBAMAN EGXCOLIM IEG",
            "",
            "## check on missing directories"
        ]
        iocdirs_input = [l.format(list_name) for l in iocdirs_input]

        # Act
        actual_output = _add_entry_to_list(iocdirs_input, list_name, device_name)

        # Assert
        self.assertEquals(iocdirs_input, actual_output)
