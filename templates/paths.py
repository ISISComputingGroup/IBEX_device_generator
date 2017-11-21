""" Paths to use for template files """
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
BLANK_OPI = os.path.join(ROOT, "blank.opi")
TEMPLATE_EMULATOR = os.path.join(ROOT, "emulator")
BASIC_DB = os.path.join(ROOT, "ioc", "basic.db")
BASIC_CONFIG_XML = os.path.join(ROOT, "ioc", "config.xml")
TEMPLATE_TESTS = os.path.join(ROOT, "tests.py")