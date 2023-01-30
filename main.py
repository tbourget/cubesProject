import json
import requests
from requests.auth import HTTPBasicAuth


def main():
    entries = get_entries_as_json()
    print(json.dumps(entries, indent=2))
    write_json_to_file(entries, 'entries')


def retrieve_api_key_from_secrets(api_name: str):
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


def get_entries_as_json():
    """
    Retrieves entries from the CUBES project proposal form as a JSON file

    Returns
    -------
    json
        The entries from the CUBES form as a JSON
    """
    form_url = 'https://tbourget.wufoo.com/api/v3/forms/z1x6vy9k0dlvbjl/entries.json?sort=EntryId&sortDirection=DESC'
    username = retrieve_api_key_from_secrets('tbourget_CUBES')
    password = 'tbourget_CUBES'

    response = requests.get(form_url, auth=HTTPBasicAuth(username, password))
    return response.json()


def write_json_to_file(json: str, file_name: str):
    """
    Writes a JSON object 'json' to a file named 'file_name'

    Parameters
    ----------
    json : str
        JSON object to write to a file
    file_name
        Desired name for JSON file
    """
    with open(file_name + '.json', 'w') as f:
        json.dump(json, f)


if __name__ == '__main__':
    main()
