import requests
import logging
from utils.device_info_generator import DeviceInfoGenerator

ORGANIZATION_NAME = "ISISComputingGroup"


def create_github_repository(device_info: DeviceInfoGenerator, github_token: str) -> None:
    """
    Creates a public repo in the ISIS Computing Group organization.

    Args:
        device_info: Provides name-based information about the device
        github_token: The GitHub authentication token.
    """
    if github_token is None:
        raise Exception("Token not specified, unable to create support repository")

    response: requests.Response = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {github_token}"
        },
        json={
            "name": device_info.support_repo_name(),
            "visibility": "public",
            "auto_init": True
        }
    )

    if response.status_code == requests.codes["created"]:
        logging.info(f"Repository {response.json().get('html_url')} created successfully.")
    else:
        raise Exception(f"Failed to create repository: {response.status_code}: {response.reason}")
