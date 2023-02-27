import sqlite3
import DatabaseFunctions
import PySide6.QtWidgets
import sys
from GuiWindows import StartupWindow, EntryListWindow

class GuiManager():
    def __init__(self):
        qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
        #my_window = EntryListWindow(data)
        self.current_window = StartupWindow(self)
        sys.exit(qt_app.exec())


    def launch_database_view(self):
        self.current_window = EntryListWindow(self)


def get_key(value:dict):
    return value['entry_id']
