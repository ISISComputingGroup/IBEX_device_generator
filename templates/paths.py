""" Paths to use for template files """
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
BLANK_OPI = join(ROOT, "blank.opi")
TEMPLATE_EMULATOR = join(ROOT, "emulator")
BASIC_DB = join(ROOT, "ioc", "basic.db")
BASIC_CONFIG_XML = join(ROOT, "ioc", "config.xml")
TEMPLATE_TESTS = join(ROOT, "tests.py")
SUPPORT_SUBMODULE_MAKEFILE = join(ROOT, "Makefile")
README = join(ROOT, "README.md")