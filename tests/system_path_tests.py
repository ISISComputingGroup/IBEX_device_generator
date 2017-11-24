""" Tests against the system paths """
import unittest
import logging
from os.path import exists
from system_paths import *


class SystemPathTests(unittest.TestCase):

    def test_GIVEN_immutable_system_paths_THEN_all_paths_exist(self):
        # Arrange
        paths = (
            INSTRUMENT, EPICS, IOC_ROOT, PERL, EPICS_BASE_BUILD, PERL_IOC_GENERATOR, EPICS_SUPPORT,
            EPICS_MASTER_RELEASE, EMULATORS_ROOT, LEWIS_EMULATORS, CLIENT_SRC, CLIENT, OPI_RESOURCES,
            IOC_TEST_FRAMEWORK_ROOT, PERL_SUPPORT_GENERATOR
        )

        # Assert
        missing_paths = 0
        for p in paths:
            if not exists(p):
                logging.error("Expected path {} does not exist. Please check the path and update the configuration in "
                              "'system_paths.py' if necessary")
                missing_paths += 1
        self.assertEqual(missing_paths, 0)
