import sqlite3
import ApiFunctions

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


def initialize_tables(db_cursor: sqlite3.Cursor):
    """
    Creates the 'entries' and 'teachers' tables in the database 'cube_project.db' if it does not exist yet. Initializes
    column names and data types.

    Parameters
    ----------
    db_cursor: sqlite3.Connection
        The cursor for the active connection to the 'cubes_project' database
    """
    try:
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS teachers(
                                        bsu_email INT PRIMARY KEY,
                                        first_name TEXT,
                                        last_name TEXT,
                                        title TEXT,
                                        department TEXT
                                        );''')

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
                                        updated_by TEXT,
                                        claimed_by TEXT,
                                        FOREIGN KEY(claimed_by) REFERENCES teachers(bsu_email)
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


def parse_dict_into_entries_table(entries_dict, db_cursor: sqlite3.Connection):
    """
    Parses the entries dictionary into a SQLite database.

    Parameters
    ----------
    entries_dict
        Dict to parse entries from
    db_cursor: sqlite3.Connection
        The cursor for the active connection to the 'cubes_project' database
    """

    for entry in entries_dict['Entries']:

        entry_tuple = list(entry.values())
        entry_tuple.append(None)

        try:
            db_cursor.execute('''INSERT OR IGNORE INTO entries VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', entry_tuple)
        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')


def retrieve_entry_data_from_database() -> list[dict]:
    with initialize_connection() as db_connection:

        db_connection.row_factory = sqlite3.Row

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        db_cursor.execute('''SELECT * FROM entries''')

        raw_data = db_cursor.fetchall()
        final_data = []

        for row in raw_data:

            record = dict_from_row(row)
            final_data.append(record)

        commit_connection_close_cursor(db_connection, db_cursor)

    return final_data


def lookup_teacher(bsu_email:str):
    with initialize_connection() as db_connection:

        db_connection.row_factory = sqlite3.Row

        # Create cursor for the database
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute("SELECT * FROM teachers WHERE bsu_email=?", (bsu_email,))
            raw_data = db_cursor.fetchall()
            if raw_data == []:
                return False
            else:
                return dict_from_row(raw_data)

        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')

        commit_connection_close_cursor(db_connection, db_cursor)


def is_entry_claimed(bsu_email:str):
    with initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute("SELECT * FROM entries WHERE claimed_by=?", (bsu_email,))
            raw_data = db_cursor.fetchall()
            if raw_data == []:
                return False
            else:
                return True

        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')

        commit_connection_close_cursor(db_connection, db_cursor)


def accept_claim(teacher_data:dict, selected_data:dict):
    with initialize_connection() as db_connection:
        print(teacher_data.keys())
        # Create cursor for the database
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute('''UPDATE entries SET claimed_by = ? WHERE entry_id = ?;''',
                              (teacher_data['bsu_email'], selected_data['entry_id'],))
            raw_data = db_cursor.fetchall()
            if raw_data == []:
                return False
            else:
                return True

        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')

        commit_connection_close_cursor(db_connection, db_cursor)

def add_teacher_row(teacher_data):
    with initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        try:
            db_cursor.execute('''INSERT OR IGNORE INTO teachers VALUES(?, ?, ?, ?, ?)''', teacher_data)

        except sqlite3.Error as db_error:
            print(f'A Database Error has occurred: {db_error}')

        commit_connection_close_cursor(db_connection, db_cursor)


def dict_from_row(row):
    return dict(zip(row.keys(), row))


def update_entries_database():
    # Initialize the connection to the 'cubes_project' SQLite database, create it if it doesn't exist
    with initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        # Initialize the 'entries' table in our database
        initialize_tables(db_cursor)

        # Retrieve the entries as a dictionary from our Wufoo.com form using Wufoo API
        entries_dict = ApiFunctions.get_entries_as_dict()

        # Parse the data from the entries dict into our entries table
        parse_dict_into_entries_table(entries_dict, db_cursor)

        # Commit changes to the SQlite connection and close the cursor
        commit_connection_close_cursor(db_connection, db_cursor)
