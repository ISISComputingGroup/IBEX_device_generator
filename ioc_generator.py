""" Contains main method for creating a vanilla IOC from scratch """
import os
from logging_utils import logger
from run_tests import run_tests

LOGGER = logger("IOC generator")


class IocGenerator(object):
    """
    Generator for the data for a basic IOC
    - IOC
    - Startup files
    - Support module
    - IOCTestFramework
    - DeviceEmulator
    - OPI information
    """
    INSTRUMENT_DIR = os.path.join("C:\\", "Instrument")
    EPICS_DIR = os.path.join(INSTRUMENT_DIR, "Apps", "EPICS")
    CLIENT_DEV_SOURCE_DIR = os.path.join(INSTRUMENT_DIR, "Dev", "base")

    def __init__(self, branch_name):

        run_tests()
        self.branch = branch_name
