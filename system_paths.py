""" Standard system paths used in the IBEX distribution """
from os import path

INSTRUMENT = path.join("C:\\", "Instrument")
EPICS = path.join(INSTRUMENT, "Apps", "EPICS")

IOC_ROOT = path.join(EPICS, "IOC", "master")
PERL = path.join("C:\\", "Strawberry", "perl", "bin", "perl.exe")
EPICS_BASE_BUILD = path.join(EPICS, "base", "master", "bin")
PERL_IOC_GENERATOR = path.join(EPICS_BASE_BUILD, "windows-x64", "makeBaseApp.pl")

EPICS_SUPPORT = path.join(EPICS, "support")

EMULATORS_ROOT = path.join(EPICS_SUPPORT, "DeviceEmulator", "master")
LEWIS_EMULATORS = path.join(EMULATORS_ROOT, "lewis_emulators")

CLIENT = path.join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = path.join(CLIENT, "base")
OPI_RESOURCES = path.join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")

IOC_TEST_FRAMEWORK_ROOT = path.join(EPICS_SUPPORT, "IocTestFramework", "master")