import requests
from requests.auth import HTTPBasicAuth

import secrets


def get_entries_as_dict() -> str:  # comment to test workflow
    """
    Retrieves entries from the CUBES project proposal form on Wufoo.com using Wufoo's API. The data is returned as a
    dictionary.

    Returns
    -------
    json
        The entries from the CUBES form as a JSON
    """

    form_url = 'https://tbourget.wufoo.com/api/v3/forms/z1x6vy9k0dlvbjl/entries.json?sort=EntryId&sortDirection=DESC'
    username = secrets.wufoo_key
    password = 'tbourget_CUBES'

    response = requests.get(form_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        print(f"GET Request succeeded: {response.status_code} {response.reason}")
    else:
        print(f"GET Request failed: {response.status_code} {response.reason}")

    return response.json()
