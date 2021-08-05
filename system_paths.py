""" Standard system paths used in the IBEX distribution """
from os.path import join

INSTRUMENT = join("C:\\", "Instrument")
EPICS = join(INSTRUMENT, "Apps", "EPICS")

IOC_ROOT = join(EPICS, "IOC", "master")
PERL = join("C:\\", "Strawberry", "perl", "bin", "perl.exe")
EPICS_BASE_BUILD = join(EPICS, "base", "master", "bin")
ARCHITECTURE = "windows-x64"
PERL_IOC_GENERATOR = join(EPICS_BASE_BUILD, ARCHITECTURE, "makeBaseApp.pl")

EPICS_SUPPORT = join(EPICS, "support")
EPICS_MASTER_RELEASE = join(EPICS, "configure", "MASTER_RELEASE")

CLIENT = join(INSTRUMENT, "Dev", "ibex_gui")
CLIENT_SRC = join(CLIENT, "base")
OPI_RESOURCES = join(CLIENT_SRC, "uk.ac.stfc.isis.ibex.opis", "resources")

PERL_SUPPORT_GENERATOR = join(EPICS_SUPPORT, "asyn", "master", "bin", ARCHITECTURE, "makeSupport.pl")
