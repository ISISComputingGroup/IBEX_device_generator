""" Paths to use for template files """
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
OPI = join(ROOT, "gui", "blank.opi")
EMULATOR_TEMPLATE = join(ROOT, "support", "system_tests", "lewis_emulators")
DB = join(ROOT, "ioc", "basic.db")
CONFIG_XML = join(ROOT, "ioc", "config.xml")
CONFIG_XML_NOT_0 = join(ROOT, "ioc", "config_not_0.xml")
TESTS_TEMPLATE = join(ROOT, "support", "system_tests", "tests", "tests.py")
TESTS_RUN_SCRIPT = join(ROOT, "support", "system_tests", "run_tests.bat")
SUPPORT_MAKEFILE = join(ROOT, "support", "Makefile")
SUPPORT_README = join(ROOT, "support", "README.md")
SUPPORT_GITIGNORE = join(ROOT, "support", ".gitignore")
SUPPORT_GITATTRIBUTES = join(ROOT, "support", ".gitattributes")
SUPPORT_LICENCE = join(ROOT, "support", "LICENCE")
