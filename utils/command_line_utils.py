""" Utilities for running scripts from the command line """


def ask_do_step(name):
    """
    Ask the user whether to do a step

    Args:
        name: Name of the step

    Returns: True or False on whether to perform the step
    """
    while True:
        reply = input(f"Should I do step: {name} (Y/N) ").upper()
        if reply == "Y":
            return True
        elif reply == "N":
            return False
        else:
            print(f"Invalid response: {reply}.")
