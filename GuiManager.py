import sqlite3
import DatabaseFunctions
import PySide6.QtWidgets
import sys
from GuiWindows import StartupWindow, EntryListWindow


class GuiManager():
    def __init__(self):
        qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
        self.current_window = StartupWindow(self)
        self.current_user = None
        sys.exit(qt_app.exec())

    def launch_database_view(self):
        self.current_window = EntryListWindow(self)

    def set_current_user(self, bsu_email:str):
        self.current_user = bsu_email

def get_key(value:dict):
    return value['entry_id']
