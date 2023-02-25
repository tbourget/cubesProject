import json
import DatabaseFunctions
import ApiFunctions
import GuiManager


def main():
    # Initialize the connection to the 'cubes_project' SQLite database, create it if it doesn't exist
    with DatabaseFunctions.initialize_connection() as db_connection:

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        # Initialize the 'entries' table in our database
        DatabaseFunctions.initialize_entries_table(db_cursor)

        # Retrieve the entries as a dictionary from our Wufoo.com form using Wufoo API
        entries_dict = ApiFunctions.get_entries_as_dict()

        # Parse the data from the entries dict into our entries table
        DatabaseFunctions.parse_json_into_entries_table(entries_dict, db_cursor)

        # Commit changes to the SQlite connection and close the cursor
        DatabaseFunctions.commit_connection_close_cursor(db_connection, db_cursor)

    # Launch the GUI Window for Database display
    GuiManager.launch_gui()


if __name__ == '__main__':
    main()
