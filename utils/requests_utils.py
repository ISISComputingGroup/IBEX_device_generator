import requests
import logging

ORGANIZATION_NAME = "ISISComputingGroup"

def create_github_repository(use_git : bool, token : str, name : str) -> None:
    """
    Creates a public repo in the ISIS Computing Group organization.

    Args:
        use_git: Use Git, if True try to create the GitHub repository, else continue.
        token: The GitHub authentication token. If a token was not given the script exits.
        name: The name of the GitHub repository.
    """
    if not use_git:
        return

    if token is None:
        logging.critical("If you are using Git, you need to add a GitHub token.")
        exit()

    response: requests.Response = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}"
        },
        json={
            "name": name,
            "visibility": "public",
            "auto_init": True
        }
    )

    if response.status_code == requests.codes["created"]:
        logging.info("Successfully created GitHub repository.")
    else:
        raise Exception(f"Failed to create repository: {response.status_code}: {response.reason}")
