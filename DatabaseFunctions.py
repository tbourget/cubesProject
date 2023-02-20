import sqlite3

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
                                        entry_id INT PRIMARY KEY,
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
                                        date_created TEXT,
                                        created_by TEXT,
                                        date_updated TEXT,
                                        updated_by TEXT
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

        entry_tuple = list(entry.values())

        try:
            db_cursor.execute('''INSERT OR IGNORE INTO entries VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', entry_tuple)
        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')
