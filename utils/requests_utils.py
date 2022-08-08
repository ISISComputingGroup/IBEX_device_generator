import requests
import logging

ORGANIZATION_NAME = "ISISComputingGroup"

def create_github_repository(github_token : str, name : str) -> None:
    """
    Creates a public repo in the ISIS Computing Group organization.

    Args:
        github_token: The GitHub authentication token.
        name: The name of the GitHub repository.
    """
    if github_token is None:
        return

    response: requests.Response = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {github_token}"
        },
        json={
            "name": name,
            "visibility": "public",
            "auto_init": True
        }
    )

    if response.status_code == requests.codes["created"]:
        logging.info(f"Repository {response.json().get('html_url')} created successfully.")
    else:
        raise Exception(f"Failed to create repository: {response.status_code}: {response.reason}")
