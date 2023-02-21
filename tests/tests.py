import json

import pytest
import DatabaseFunctions
import ApiFunctions
import GuiManager
import GuiWindows



def test_get_entries_as_json():
    """
    Tests get_entries_as_json(), our API json retrieval function
        - Test 1: Asserts we retrieve 10 or more entries
    """
    entries_json = ApiFunctions.get_entries_as_json()

    # Test 1
    entry_count = 0
    for entry in entries_json['Entries']:
        entry_count += 1

    assert entry_count >= 10


def test_parse_json_into_entries_table():
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

def test_other():
    print("ok")
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

    data = GuiManager.retrieve_entry_data_from_database()
    data.sort(key=GuiManager.get_key)
    test_window = GuiWindows.EntryDataWindow(data)
    widget = test_window.findChildren("email_display")
    print("ok")
    assert widget.text() == "testcase@gmail.com"
    # widget = test_window.findChildren("opp_course_proj_display")
    # assert widget.isChecked()