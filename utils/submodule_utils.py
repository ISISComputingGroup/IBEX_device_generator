""" Utilities for adding a template emulator for a new IBEX device"""
from system_paths import EPICS_SUPPORT, PERL, PERL_SUPPORT_GENERATOR, EPICS
from templates.paths import SUPPORT_SUBMODULE_MAKEFILE
from common_utils import run_command, replace_in_file, rmtree, get_input
from os import path, mkdir, remove
from shutil import copyfile
import git
import logging
from git_utils import RepoWrapper


def _create_remote_repo(device):
    """
    :param device: Name of the device
    """
    message = """Please create the repo repo on github (https://github.com/organizations/ISISComputingGroup/repositories
    /new) and enter the name here. Leave it blank to use the default ({}) """.format("EPICS-"+device)
    requested_repo_name = get_input(message)
    return requested_repo_name if len(requested_repo_name)>0 else "EPICS-{}".format(device)


def _add_to_makefile(device):
    makefile = path.join(EPICS_SUPPORT, "Makefile")
    with open(makefile) as f:
        old_lines = f.readlines()
    new_lines = []
    last_line = ""
    marker = "SUPPDIRS += "
    for line in old_lines:
        if marker in last_line and marker not in line:
            new_lines.append(marker + device)
        new_lines.append(line)

    with open(makefile, "w") as f:
        f.writelines(new_lines)


def create_submodule(device):
    """
    Creates a submodule and links it into the main EPICS repo
    :param device: Name of the device
    """
    submodule_path = path.join(EPICS_SUPPORT, device)
    if path.exists(submodule_path):
        raise OSError("Submodule directory {} already exists".format(submodule_path))
    else:
        mkdir(submodule_path)
    copyfile(SUPPORT_SUBMODULE_MAKEFILE, path.join(submodule_path, "Makefile"))
    repo_name = _create_remote_repo(device)
    repo_url = "https://github.com/ISISComputingGroup/{}.git".format(repo_name)
    epics_repo = RepoWrapper(EPICS)._repo
    epics_repo.clone_from(url=repo_url, to_path=path.join(submodule_path, "master"))
    if not path.exists(path.join(submodule_path, "master", ".git")):
        support_repo = RepoWrapper(path.join(submodule_path, "master"))._repo
        support_repo.init()
        support_repo.add(A=True)
        support_repo.commit(m="Initial commit")
        support_repo.push(u="origin")
    epics_repo.create_submodule(repo_url, path.join(submodule_path, "master"))
    _add_to_makefile(device)


def set_up_template_support_directory(device):
    """

    :param device:
    :return:
    """
    master = path.join(EPICS_SUPPORT, device, "master")
    run_command([PERL, PERL_SUPPORT_GENERATOR, "-t", "streamSCPI", device], master)
    remove(path.join(master, "{}Sup".format(device), "dev{}.db".format(device)))