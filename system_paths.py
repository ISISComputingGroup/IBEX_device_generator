""" Standard system paths used in the IBEX distribution """
import os

INSTRUMENT = os.path.join("C:\\", "Instrument")
EPICS = os.path.join(INSTRUMENT, "Apps", "EPICS")
EPICS_SUPPORT = os.path.join(EPICS, "support")
EMULATORS = os.path.join(EPICS_SUPPORT, "DeviceEmulator", "master", "lewis_emulators")
CLIENT = os.path.join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = os.path.join(CLIENT, "base")
OPI_RESOURCES = os.path.join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")
