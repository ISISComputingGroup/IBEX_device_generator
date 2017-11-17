""" Classes and methods associated with logging """
import logging


def logger(name):
    """
    Generates a logger object

    :param name: The name of the logger
    :return: a logging.logger object
    """
    logging.basicConfig(format="'%(asctime)-15s, " + name + ": %(message)s'")
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.INFO)
    return new_logger
