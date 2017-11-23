""" Tests against the system paths """
import unittest
from os.path import exists
from system_paths import INSTRUMENT, EPICS, IOC_ROOT, PERL, EPICS_BASE_BUILD, PERL_IOC_GENERATOR, EPICS_SUPPORT, \
    EPICS_MASTER_RELEASE, EMULATORS_ROOT, LEWIS_EMULATORS, CLIENT, CLIENT_SRC, OPI_RESOURCES, IOC_TEST_FRAMEWORK_ROOT, \
    PERL_SUPPORT_GENERATOR

class SystemPathTests(unittest.TestCase):

    def test_GIVEN_system_paths_THEN_all_paths_exist(self):
        # Arrange
        paths = INSTRUMENT, EPICS, IOC_ROOT, PERL, EPICS_BASE_BUILD, PERL_IOC_GENERATOR, EPICS_SUPPORT, \
                EPICS_MASTER_RELEASE, EMULATORS_ROOT, LEWIS_EMULATORS, CLIENT_SRC, CLIENT, OPI_RESOURCES, \
                IOC_TEST_FRAMEWORK_ROOT, PERL_SUPPORT_GENERATOR

        # Assert
        self.assertTrue(all([exists(p) for p in paths]))