""" Standard system paths used in the IBEX distribution """
from os import path

INSTRUMENT = path.join("C:\\", "Instrument")
EPICS = path.join(INSTRUMENT, "Apps", "EPICS")
EPICS_SUPPORT = path.join(EPICS, "support")
EMULATORS_ROOT = path.join(EPICS_SUPPORT, "DeviceEmulator", "master")
LEWIS_EMULATORS = path.join(EMULATORS_ROOT, "lewis_emulators")
CLIENT = path.join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = path.join(CLIENT, "base")
OPI_RESOURCES = path.join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")
