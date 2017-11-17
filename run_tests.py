""" Runs tests associated with the IOC generation script """
import os
import sys
import unittest
from xmlrunner import XMLTestRunner
from utils.command_line_utils import parse_args

DEFAULT_TEST_LOCATION = "test-reports\\"


def run_tests(test_reports_path=DEFAULT_TEST_LOCATION):
    """
    Runs the test suite

    :param test_reports_path: Path to test reports
    :return: True if the tests passed, false otherwise
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for case in []:
        suite.addTests(loader.loadTestsFromTestCase(case))

    return XMLTestRunner(output=str(os.path.join(test_reports_path)), stream=sys.stdout).run(suite).wasSuccessful()


def main():
    """
    Routine to run when script executed from the command line
    """
    args = parse_args(
        "Runs tests for the IOC generation script",
        [{"name": "reports_path", "type": str, "description": "The folder in which test reports should be stored",
          "default": DEFAULT_TEST_LOCATION}]
    )
    run_tests(args.reports_path)


if __name__ == "__main__":
    main()
