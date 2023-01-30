# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
from requests.auth import HTTPBasicAuth


def main():

    form_url = 'https://tbourget.wufoo.com/api/v3/forms/z1x6vy9k0dlvbjl/entries.json?sort=EntryId&sortDirection=DESC'
    username = retrieve_api_key('tbourget_CUBES')
    password = 'tjbourget'

    response = requests.get(form_url, auth=HTTPBasicAuth(username, password))

    print(json.dumps(response.json(), indent=2))

def retrieve_api_key(username):
    with open(".secrets.json") as f:

        data = json.load(f)
        return data[username]

#def get_entries_as_JSON():
    # Use a breakpoint in the code line below to debug your script.
    # GET http://{subdomain}.wufoo.com/api/v3/forms/{identifier}/entries.{format}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
