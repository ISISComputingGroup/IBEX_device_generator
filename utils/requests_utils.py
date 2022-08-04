import requests
import logging

ORGANIZATION_NAME = "ISISComputingGroup"
ICP_WRITE_ID = 1709123

def create_github_repository(token : str, name : str) -> None:

    response: requests.Response = requests.post(
        f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}"
        },
        json={
            "name": f"{name}",
            "visibility": "public",
            "team_id": ICP_WRITE_ID,
            "auto_init": True
        }
    )

    if response.status_code == requests.codes["created"]:
        logging.info("Successfully created GitHub repository.")
    else:
        raise Exception(f"Failed to create repository: {response.status_code}: {response.reason}")
