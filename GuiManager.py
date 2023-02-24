import sqlite3
import DatabaseFunctions
import PySide6.QtWidgets
import sys
from GuiWindows import EntryListWindow


def display_data(data: list):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
    my_window = EntryListWindow(data)
    sys.exit(qt_app.exec())


def retrieve_entry_data_from_database() -> list[dict]:
    with DatabaseFunctions.initialize_connection() as db_connection:

        db_connection.row_factory = sqlite3.Row

        # Create cursor for the database
        db_cursor = db_connection.cursor()

        db_cursor.execute('''SELECT * FROM entries''')

        raw_data = db_cursor.fetchall()
        final_data = []

        for row in raw_data:

            record = dict_from_row(row)
            final_data.append(record)

        DatabaseFunctions.commit_connection_close_cursor(db_connection, db_cursor)

    return final_data

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def get_key(value:dict):
    return value['entry_id']

def launch_gui():
    data = retrieve_entry_data_from_database()
    data.sort(key=get_key)
    display_data(data)
