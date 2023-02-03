import pytest
from main import *


def test_get_entries_as_json():
    """
    Tests get_entries_as_json(), our API json retrieval function
        - Test 1: Asserts we retrieve 10 or more entries
    """
    entries_json = get_entries_as_json()

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

    # Test 1
    with initialize_connection() as db_connection:

        db_cursor = db_connection.cursor()
        initialize_entries_table(db_cursor)

        with open('test_entry.json') as test_entry:
            test_entry_json = json.load(test_entry)
            parse_json_into_entries_table(test_entry_json, db_cursor)
            db_cursor.execute("SELECT first_name FROM entries WHERE first_name=?", ('Test',))
            data = db_cursor.fetchall()
            db_cursor.execute("DELETE FROM entries")
            db_cursor.close()

            assert data != []

