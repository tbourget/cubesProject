import json
import sqlite3
import requests
from requests.auth import HTTPBasicAuth


def main():
    # Initialize the connection to the 'cubes_project' SQLite database
    with initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        # Initialize the 'entries' table in our database
        initialize_entries_table(db_cursor)

        # Retrieve the entries as a JSON from our Wufoo.com form using Wufoo API
        entries_json = get_entries_as_json()

        # Parse the data from the entries JSON into our entries table
        parse_json_into_entries_table(entries_json, db_cursor)

        # Write the entries JSON to a file
        write_json_to_file(entries_json, 'entries')

        # Commit changes to the SQlite connection and close the cursor
        commit_connection_close_cursor(db_connection, db_cursor)


# RETRIEVAL / API FUNCTIONS


def retrieve_api_key_from_secrets(api_name: str) -> str:
    """
    Retrieves an API key from a .secrets JSON dictionary using an API name as the dictionary key.

    Parameters
    ----------
    api_name: str
        Name of the API to retrieve the key for

    Returns
    -------
    str
        The API key of the corresponding api_name
    """

    with open(".secrets.json") as f:
        data = json.load(f)
        return data[api_name]


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
    username = retrieve_api_key_from_secrets('tbourget_CUBES')
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


# DATABASE FUNCTIONS


def initialize_connection() -> sqlite3.Connection:
    """
    Connects to local SQLite CUBES entries database 'cubes_project.db', creates the database if it doesn't exist yet.

    Returns
    -------
    sqlite3.Connection
        The active connection to the 'cubes_project' database
    """

    db_connection = None
    try:
        # Connect to a sqlite database - create it if it does not exist
        db_connection = sqlite3.connect('cubes_project.db')
        return db_connection

    except sqlite3.Error as db_error:
        print(f'A Database Error has occurred: {db_error}')


def initialize_entries_table(db_cursor: sqlite3.Cursor):
    """
    Creates the 'entries' table in the database 'cube_project.db' if it does not exist yet. Initializes column names
    and data types.

    Parameters
    ----------
    db_cursor: sqlite3.Connection
        The cursor for the active connection to the 'cubes_project' database
    """
    try:
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
                                        entry_id INT,
                                        prefix TEXT,
                                        first_name TEXT,
                                        last_name TEXT,
                                        title TEXT,
                                        organization_name TEXT,
                                        email TEXT,
                                        organization_website TEXT,
                                        phone_number TEXT,
                                        opportunity_course_project BIT,
                                        opportunity_guest_speaker BIT,
                                        opportunity_site_visit BIT,
                                        opportunity_job_shadow BIT,
                                        opportunity_internships BIT,
                                        opportunity_career_panel BIT,
                                        opportunity_networking_event BIT,
                                        proposed_time_summer22 BIT,
                                        proposed_time_fall22 BIT,
                                        proposed_time_spring23 BIT,
                                        proposed_time_summer23 BIT,
                                        proposed_time_other BIT,
                                        permission_to_use_org_name TEXT,
                                        updated_by INT
                                        );''')
    except sqlite3.Error as db_error:
        print(f'A Database Error has occurred: {db_error}')


def commit_connection_close_cursor(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor):
    """
    Commits any changes to the connection, closes the cursor

    Parameters
    ----------
    db_connection : sqlite3.Connection
        Connection to commit changes to
    db_cursor : sqlite3.Cursor
        Cursor of the connection to close
    """

    db_connection.commit()
    db_cursor.close()


def parse_json_into_entries_table(entries_json, db_cursor: sqlite3.Connection):
    """
    Parses the entries JSON dictionary into a SQLite database.

    Parameters
    ----------
    entries_json
        JSON object to parse entries from
    db_cursor: sqlite3.Connection
        The cursor for the active connection to the 'cubes_project' database
    """

    for entry in entries_json['Entries']:
        print(json.dumps(entry, indent=2))
        print('\n\n\n')


if __name__ == '__main__':
    main()
