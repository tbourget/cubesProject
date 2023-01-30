import json
import requests
from requests.auth import HTTPBasicAuth


def main():
    entries = get_entries_as_JSON()
    print(json.dumps(entries.json(), indent=2))


def retrieve_api_key(api_name: str):
    """
    Retrieves an API key from a .secrets JSON dict using an API name

    Parameters
    ----------
    api_name : str
        Name of the API to retrieve the key for

    Returns
    -------
    str
        The API key of the corresponding api_name
    """
    with open(".secrets.json") as f:
        data = json.load(f)
        return data[api_name]


def get_entries_as_JSON():
    """
    Retrieves entries from the CUBES project proposal form as a JSON file

    Returns
    -------
    json
        The entries from the CUBES form as a JSON
    """
    # Use a breakpoint in the code line below to debug your script.
    form_url = 'https://tbourget.wufoo.com/api/v3/forms/z1x6vy9k0dlvbjl/entries.json?sort=EntryId&sortDirection=DESC'
    username = retrieve_api_key('tbourget_CUBES')
    password = 'tbourget_CUBES'

    response = requests.get(form_url, auth=HTTPBasicAuth(username, password))
    return response.json()


if __name__ == '__main__':
    main()
