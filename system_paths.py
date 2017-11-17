""" Standard system paths used in the IBEX distribution """
import os

INSTRUMENT = os.path.join("C:\\", "Instrument")
EPICS = os.path.join(INSTRUMENT, "Apps", "EPICS")
EPICS_SUPPORT = os.path.join(EPICS, "support")
CLIENT = os.path.join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = os.path.join(CLIENT, "base")
