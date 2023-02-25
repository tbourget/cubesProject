import json
import sqlite3

import pytestqt
import PySide6.QtTest
import PySide6.QtCore
import PySide6.QtWidgets

import DatabaseFunctions
import ApiFunctions
import GuiManager
import GuiWindows
import mock


def test_get_entries_as_json():
    """
    Tests get_entries_as_json(), our API json retrieval function
        - Test 1: Asserts we retrieve 10 or more entries
    """
    entries_json = ApiFunctions.get_entries_as_dict()

    # Test 1
    entry_count = 0
    for entry in entries_json['Entries']:
        entry_count += 1

    assert entry_count >= 10


def test_entry_table_data_population():
    """
    Tests parse_json_into_entries_table(), our function that parses a retrieved entries JSON into an SQLite database
        - Test 1: Asserts that a sample entry appears in the database
    """

    # Create a temporary database with a test entry
    with DatabaseFunctions.initialize_connection() as db_connection:
        db_cursor = db_connection.cursor()
        DatabaseFunctions.initialize_entries_table(db_cursor)
        test_entry = \
            """{
                "Entries": [
                    {
                        "EntryId": "1",
                        "Field2": "",
                        "Field4": "Test",
                        "Field5": "Entry",
                        "Field6": "Pytest Expert",
                        "Field7": "Python",
                        "Field8": "testcase@gmail.com",
                        "Field9": "python.com",
                        "Field10": "1112223333",
                        "Field11": "Course Project",
                        "Field12": "",
                        "Field13": "",
                        "Field14": "",
                        "Field15": "",
                        "Field16": "",
                        "Field17": "",
                        "Field111": "",
                        "Field112": "",
                        "Field113": "",
                        "Field114": "",
                        "Field115": "",
                        "Field211": "",
                        "DateCreated": "2023-01-31 11:32:20",
                        "CreatedBy": "tbourget",
                        "DateUpdated": "",
                        "UpdatedBy": null
                    }
                ]
            }"""

        test_entry_json = json.loads(test_entry)
        DatabaseFunctions.parse_json_into_entries_table(test_entry_json, db_cursor)

        db_cursor.execute("SELECT first_name FROM entries WHERE first_name=?", ('Test',))
        data = db_cursor.fetchall()
        db_cursor.close()

        assert data != []


def test_database_exists():
    """
    Tests parse_json_into_entries_table(), our function that parses a retrieved entries JSON into an SQLite database
        - Test 1: Asserts that a sample entry appears in the database
    """
    # Create a temporary database with a test entry
    try:
        connection = DatabaseFunctions.initialize_connection()
    except sqlite3.Error as db_error:
        assert 2 == 1

    assert 1 == 1


def test_entry_data_window_data_population(qtbot):
    # Create a temporary database with a test entry
    with DatabaseFunctions.initialize_connection() as db_connection:
        db_cursor = db_connection.cursor()
        DatabaseFunctions.initialize_entries_table(db_cursor)
        test_entry = \
            """{
                "Entries": [
                    {
                        "EntryId": "1",
                        "Field2": "",
                        "Field4": "Test",
                        "Field5": "Entry",
                        "Field6": "Pytest Expert",
                        "Field7": "Python",
                        "Field8": "testcase@gmail.com",
                        "Field9": "python.com",
                        "Field10": "1112223333",
                        "Field11": "Course Project",
                        "Field12": "",
                        "Field13": "",
                        "Field14": "",
                        "Field15": "",
                        "Field16": "",
                        "Field17": "",
                        "Field111": "",
                        "Field112": "",
                        "Field113": "",
                        "Field114": "",
                        "Field115": "",
                        "Field211": "",
                        "DateCreated": "2023-01-31 11:32:20",
                        "CreatedBy": "tbourget",
                        "DateUpdated": "",
                        "UpdatedBy": null
                    }
                ]
            }"""

        test_entry_json = json.loads(test_entry)
        DatabaseFunctions.parse_json_into_entries_table(test_entry_json, db_cursor)

        db_cursor.execute('''SELECT * FROM entries''')

        raw_data = db_cursor.fetchall()

        DatabaseFunctions.commit_connection_close_cursor(db_connection, db_cursor)

    with mock.patch.object(PySide6.QtWidgets.QApplication, "exit"):
        data = GuiManager.retrieve_entry_data_from_database()
        for entry_record in data:
            data = entry_record

        test_window = GuiWindows.EntryDataWindow(data)

        widget = test_window.findChildren(PySide6.QtWidgets.QLineEdit, "email_display")
        print(widget)
        assert widget[0].text() == "testcase@gmail.com"
