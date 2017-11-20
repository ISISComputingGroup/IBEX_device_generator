""" Contains main method for creating a vanilla IOC from scratch """
from run_tests import run_tests
from utils.common_utils import create_component
from utils.gui_utils import create_opi
from utils.emulator_utils import create_emulator
from utils.command_line_utils import parse_args
from system_paths import CLIENT, EMULATORS_ROOT
import logging


def _configure_logging():
    logging.basicConfig(format="'%(asctime)-15s, %(levelname)s: %(message)s'")
    logging.getLogger().setLevel(logging.INFO)


def generate_device(name, ticket, submodule=True, opi=True, tests=True, emulator=True):
    """
    Creates the boilerplate components for an IOC
    :param name: The name of the IOC
    :param ticket: The ticket number this relates to
    :param submodule: Whether to create a support submodule
    :param opi: Whether to create an empty OPI
    :param tests: Whether to create IOC system tests
    :param emulator: Whether to create a device emulator
    """

    _configure_logging()

    underscore_separated_name = name.lower().replace(" ", "_")
    camel_case_name = name.title().replace(" ", "")
    branch = "Ticket{}_Add_IOC_{}".format(ticket, camel_case_name)

    # Still need to create the IOC directory
    if submodule:
        pass
    if tests:
        pass
    if emulator:
        create_component(camel_case_name, branch, EMULATORS_ROOT, create_emulator, "Add template emulator")
    # if opi:
    #     create_component(underscore_separated_name, branch, CLIENT, create_opi, "Add template OPI file")


def main():
    """
    Routine to run when script executed from the command line
    """
    if not run_tests():
        raise AssertionError("IOC generator failed its unit tests. Please fix before running")

    args = parse_args(
        "Generate boilerplate code for IBEX device support",
        [{"name": "name", "type": str, "description": "Name of the device"},
         {"name": "ticket", "type": int, "description": "Ticket number"}]
    )
    generate_device(args.name, args.ticket)


if __name__ == "__main__":
    main()
