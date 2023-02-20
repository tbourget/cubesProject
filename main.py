import json
import DatabaseFunctions
import requests
import secrets
from requests.auth import HTTPBasicAuth


def main():
    # Initialize the connection to the 'cubes_project' SQLite database, create it if it doesn't exist
    with DatabaseFunctions.initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        # Initialize the 'entries' table in our database
        DatabaseFunctions.initialize_entries_table(db_cursor)

        # Retrieve the entries as a JSON from our Wufoo.com form using Wufoo API
        entries_json = get_entries_as_json()

        # Parse the data from the entries JSON into our entries table
        DatabaseFunctions.parse_json_into_entries_table(entries_json, db_cursor)

        # Write the entries JSON to a file
        write_json_to_file(entries_json, 'cubes_entries')

        # Commit changes to the SQlite connection and close the cursor
        DatabaseFunctions.commit_connection_close_cursor(db_connection, db_cursor)


# DATA RETRIEVAL / API FUNCTIONS


def get_entries_as_json() -> str:
    """
    Retrieves entries from the CUBES project proposal form on Wufoo.com using Wufoo's API. The data is returned as a
    JSON object.

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


def write_json_to_file(json_obj, file_name: str):
    """
    Writes a JSON object 'json_obj' to a file named 'file_name'.

    Parameters
    ----------
    json_obj
        JSON object to write to a file
    file_name: str
        Desired name for JSON file
    """

    with open(file_name + '.json', 'w') as f:
        json.dump(json_obj, f, indent=2)


if __name__ == '__main__':
    main()
