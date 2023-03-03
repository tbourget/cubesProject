import sys
import DatabaseFunctions
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QLabel, \
    QLineEdit, QCheckBox, QComboBox
from PySide6.QtGui import QCloseEvent


class StartupWindow(QWidget):
    def __init__(self, gui_manager):
        super().__init__()
        self.gm = gui_manager
        self.setup_window()
        self.show()

    def setup_window(self):
        self.setWindowTitle("CUBES Project Database Viewer")
        self.setGeometry(200, 100, 345, 75)
        view_data_button = QPushButton("View Data", self)
        view_data_button.resize(100, 25)
        view_data_button.move(60, 25)
        view_data_button.clicked.connect(self.view_button)
        update_data_button = QPushButton("Update Data", self)
        update_data_button.resize(100, 25)
        update_data_button.move(200, 25)
        update_data_button.clicked.connect(self.update_button)

    def update_button(self):
        DatabaseFunctions.update_entries_database()
        reply = QMessageBox.information(
            self,
            'INFO',
            'Database updated',
            QMessageBox.Ok)

    def view_button(self):
        self.gm.launch_database_view()


class EntryListWindow(QWidget):
    def __init__(self, gui_manager):
        super().__init__()
        self.data = DatabaseFunctions.retrieve_entry_data_from_database()
        self.selected_data = None
        self.gm = gui_manager
        self.list_control = None
        self.data_window = None
        self.current_list_item = None
        self.claim_login_window = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("CUBES Project Database Viewer")
        display_list = QListWidget(self)
        self.list_control = display_list
        self.populate_display_list(self.data)
        display_list.resize(400, 700)
        display_list.currentItemChanged.connect(self.list_item_selected)
        self.setGeometry(50, 50, 400, 750)
        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(50, 713)
        claim_button = QPushButton("Claim Submission", self)
        claim_button.clicked.connect(self.list_item_claimed)
        claim_button.resize(115, 25)
        claim_button.move(150, 713)
        self.show()

    def populate_display_list(self, data: list[dict]):
        for entries in data:
            display_text = f"{entries['entry_id']}\t{entries['organization_name']}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)

    def find_full_data_record(self, entry_id):
        for entry_record in self.data:
            if entry_record['entry_id'] == int(entry_id):
                return entry_record

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        entry_id = current.data(0).split("\t")[0]
        self.selected_data = self.find_full_data_record(entry_id)
        self.data_window = EntryDataWindow(self.selected_data, self)
        self.data_window.show()

    def list_item_claimed(self):
        self.claim_login_window = ClaimEntryLoginWindow(self, self.selected_data)

    def close_claim_login_window(self):
        self.claim_login_window = None

    def update_data(self):
        self.data = DatabaseFunctions.retrieve_entry_data_from_database()
        entry_id = self.list_control.currentItem().data(0).split("\t")[0]
        self.selected_data = self.find_full_data_record(entry_id)
        self.data_window = EntryDataWindow(self.selected_data, self)
        self.data_window.show()

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class EntryDataWindow(QWidget):
    def __init__(self, entry_data:dict, entry_list_window:QWidget):
        super().__init__()
        self.entry_list_window = entry_list_window
        self.data = entry_data
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle(f"{self.data['organization_name']}")
        self.setGeometry(450, 50, 500, 750)  # put the new window next to the original one wider than it is tall

        # Claimed by
        label = QLabel(self)
        label.setText(f"Claimed by: {self.data['claimed_by']}")
        label.move(50, 25)

        label = QLabel("Prefix: ", self)

        label.move(50, 50)
        prefix_display = QComboBox(self)
        prefix_display.addItems([" ", "Dr.", "Mrs.","Ms.","Mr."])
        prefix_display.move(200, 50)
        prefix_display.setEnabled(False)

        prefix = self.data['prefix']
        if prefix == "Dr.":
            prefix_display.setCurrentIndex(1)
        elif prefix == "Mrs.":
            prefix_display.setCurrentIndex(2)
        elif prefix == "Ms.":
            prefix_display.setCurrentIndex(3)
        elif prefix == "Mr.":
            prefix_display.setCurrentIndex(4)
        else:
            prefix_display.setCurrentIndex(0)

        # First name
        label = QLabel("First Name: ", self)
        label.move(50, 80)

        first_name_display = QLineEdit(self.data['first_name'], self)
        first_name_display.move(200, 80)
        first_name_display.setReadOnly(True)

        # Last name
        label = QLabel("Last Name: ", self)
        label.move(50, 110)

        last_name_display = QLineEdit(self.data['last_name'], self)
        last_name_display.move(200, 110)
        last_name_display.setReadOnly(True)

        # Title
        label = QLabel("Title: ", self)
        label.move(50, 140)

        title_display = QLineEdit(self.data['title'], self)
        title_display.move(200, 140)
        title_display.setReadOnly(True)

        # Organization Name
        label = QLabel("Organization: ", self)
        label.move(50, 170)

        organization_name_display = QLineEdit(self.data['organization_name'], self)
        organization_name_display.move(200, 170)
        organization_name_display.setReadOnly(True)

        # Organization Email
        label = QLabel("Email: ", self)
        label.move(50, 200)

        email_display = QLineEdit(self.data['email'], self)
        email_display.setObjectName("email_display")
        email_display.move(200, 200)
        email_display.setReadOnly(True)

        # Organization Website
        label = QLabel("Website: ", self)
        label.move(50, 230)

        organization_website_display = QLineEdit(self.data['organization_website'], self)
        organization_website_display.move(200, 230)
        organization_website_display.setReadOnly(True)

        # Organization Phone Number
        label = QLabel("Phone Number: ", self)
        label.move(50, 260)

        phone_number_display = QLineEdit(self.data['phone_number'], self)
        phone_number_display.move(200, 260)
        phone_number_display.setReadOnly(True)

        # Opportunities interested in
        label = QLabel("Opportunities interested in: ", self)
        label.move(50, 300)

        label = QLabel("Course Project", self)
        label.move(70, 340)
        opp_course_proj_display = QCheckBox(self)
        opp_course_proj_display.move(180, 342)
        if self.data['opportunity_course_project'] != "":
            opp_course_proj_display.setChecked(1)
        opp_course_proj_display.setEnabled(False)

        label = QLabel("Guest Speaker", self)
        label.move(240, 340)
        opp_guest_speak_display = QCheckBox(self)
        opp_guest_speak_display.move(340, 342)
        if self.data['opportunity_guest_speaker'] != "":
            opp_guest_speak_display.setChecked(1)
        opp_guest_speak_display.setEnabled(False)

        label = QLabel("Site Visit", self)
        label.move(70, 370)
        opp_site_visit_display = QCheckBox(self)
        opp_site_visit_display.move(180, 372)
        if self.data['opportunity_site_visit'] != "":
            opp_site_visit_display.setChecked(1)
        opp_site_visit_display.setEnabled(False)

        label = QLabel("Job Shadow", self)
        label.move(240, 370)
        opp_job_shadow_display = QCheckBox(self)
        opp_job_shadow_display.move(340, 372)
        if self.data['opportunity_job_shadow'] != "":
            opp_job_shadow_display.setChecked(1)
        opp_job_shadow_display.setEnabled(False)

        label = QLabel("Internships", self)
        label.move(70, 400)
        opp_internships_display = QCheckBox(self)
        opp_internships_display.move(180, 402)
        if self.data['opportunity_internships'] != "":
            opp_internships_display.setChecked(1)
        opp_internships_display.setEnabled(False)

        label = QLabel("Career Panel", self)
        label.move(240, 400)
        opp_career_panel_display = QCheckBox(self)
        opp_career_panel_display.move(340, 402)
        if self.data['opportunity_career_panel'] != "":
            opp_career_panel_display.setChecked(1)
        opp_career_panel_display.setEnabled(False)

        label = QLabel("Networking Event", self)
        label.move(70, 430)
        opp_network_event_display = QCheckBox(self)
        opp_network_event_display.move(180, 432)
        if self.data['opportunity_networking_event'] != "":
            opp_network_event_display.setChecked(1)
        opp_network_event_display.setEnabled(False)

        # Proposed collaboration time
        label = QLabel("Proposed collaboration time:", self)
        label.move(50, 470)

        label = QLabel("Summer 2022 (June 2022 - August 2022)", self)
        label.move(70, 510)
        collab_time_sum22_display = QCheckBox(self)
        collab_time_sum22_display.move(330, 512)
        if self.data['proposed_time_summer22'] != "":
            collab_time_sum22_display.setChecked(1)
        collab_time_sum22_display.setEnabled(False)

        label = QLabel("Fall 2022 (September 2022 - December 2022)", self)
        label.move(70, 540)
        collab_time_fall22_display = QCheckBox(self)
        collab_time_fall22_display.move(330, 542)
        if self.data['proposed_time_fall22'] != "":
            collab_time_fall22_display.setChecked(1)
        collab_time_fall22_display.setEnabled(False)

        label = QLabel("Spring 2023 (January 2023 - April 2023)", self)
        label.move(70, 570)
        collab_time_spring23_display = QCheckBox(self)
        collab_time_spring23_display.move(330, 572)
        if self.data['proposed_time_spring23'] != "":
            collab_time_spring23_display.setChecked(1)
        collab_time_spring23_display.setEnabled(False)

        label = QLabel("Summer 2023 (June 2023 - August 2023)", self)
        label.move(70, 600)
        collab_time_sum23_display = QCheckBox(self)
        collab_time_sum23_display.move(330, 602)
        if self.data['proposed_time_summer23'] != "":
            collab_time_sum23_display.setChecked(1)
        collab_time_sum23_display.setEnabled(False)

        label = QLabel("Other", self)
        label.move(70, 630)
        collab_time_other_display = QCheckBox(self)
        collab_time_other_display.move(330, 632)
        if self.data['proposed_time_other'] != "":
            collab_time_other_display.setChecked(1)
        collab_time_other_display.setEnabled(False)

        # Permission to use organization name
        label = QLabel("Permission to use organization name?", self)
        label.move(50, 670)
        permission_to_use_name_display = QComboBox(self)
        permission_to_use_name_display.addItem("Yes")
        permission_to_use_name_display.addItem("No")
        permission_to_use_name_display.addItem("Further discussion is needed")
        permission_to_use_name_display.setEnabled(False)

        permission = self.data['permission_to_use_org_name']
        if permission == "Yes":
            permission_to_use_name_display.setCurrentIndex(0)
        elif permission == "No":
            permission_to_use_name_display.setCurrentIndex(1)
        else:
            permission_to_use_name_display.setCurrentIndex(2)

        permission_to_use_name_display.move(50, 700)


class ClaimEntryLoginWindow(QWidget):
    def __init__(self, entry_list_window:QWidget, selected_data:dict):
        super().__init__()
        self.signup_window = None
        self.email_display = None
        self.selected_data = selected_data
        self.entry_list_window = entry_list_window
        self.setup_window()
        self.show()

    def setup_window(self):
        self.setWindowTitle("Login")
        self.setGeometry(200, 100, 345, 125)

        label = QLabel(self)
        label.setText("Enter your BSU email:")
        label.move(50, 25)

        submit_data_button = QPushButton("Submit", self)
        submit_data_button.resize(100, 25)
        submit_data_button.move(50, 75)
        submit_data_button.clicked.connect(self.submit_button)
        cancel_data_button = QPushButton("Cancel", self)
        cancel_data_button.resize(100, 25)
        cancel_data_button.move(190, 75)
        cancel_data_button.clicked.connect(self.cancel_button)

        self.email_display = QLineEdit("j1appleseed", self)
        self.email_display.move(50, 45)

        label = QLabel(self)
        label.setText("Enter your BSU email:")
        label.move(50, 25)

        label = QLabel("@bridgew.edu", self)
        label.move(185, 47)

    def cancel_button(self):
        EntryListWindow.close_claim_login_window(self.entry_list_window)

    def submit_button(self):
        entry_claimed = DatabaseFunctions.is_entry_claimed(self.email_display.text(), self.selected_data['entry_id'])
        user_dict = DatabaseFunctions.lookup_teacher(self.email_display.text())

        if not entry_claimed:
            # If the username isn't already stored, sign user up
            if user_dict == False:
                self.signup_window = ClaimEntrySignUpWindow(self.entry_list_window, self.selected_data, self.email_display.text())
                self.close()
            # If the username is already stored
            else:
                DatabaseFunctions.accept_claim(user_dict, self.selected_data)
                reply = QMessageBox.information(
                    self,
                    'INFO',
                    'User info retrieved from email\nProject successfully claimed',
                    QMessageBox.Ok)
                self.entry_list_window.update_data()
                self.close()
        else:
            teacher_claimed_by = self.selected_data['claimed_by']
            reply = QMessageBox.information(
                self,
                'INFO',
                f'This entry is already claimed by {teacher_claimed_by}',
                QMessageBox.Ok)
            self.close()


class ClaimEntrySignUpWindow(QWidget):
    def __init__(self, entry_list_window: QWidget, selected_data: dict, bsu_email:str):
        super().__init__()
        self.bsu_email = bsu_email
        self.first_name_display = None
        self.last_name_display = None
        self.title_display = None
        self.department_display = None
        self.bsu_email = bsu_email
        self.entry_list_window = entry_list_window
        self.selected_data = selected_data
        self.setup_window()
        self.show()

    def setup_window(self):
        self.setWindowTitle("Enter Your Information:")
        self.setGeometry(200, 100, 345, 200)

        label = QLabel(self)
        label.setText(f"{self.bsu_email}@bridgew.edu")
        label.move(50, 25)

        label = QLabel(self)
        label.setText("First Name:")
        label.move(50, 50)
        self.first_name_display = QLineEdit(self)
        self.first_name_display.move(125, 50)

        label = QLabel(self)
        label.setText("Last Name:")
        label.move(50, 75)
        self.last_name_display = QLineEdit(self)
        self.last_name_display.move(125, 75)

        label = QLabel(self)
        label.setText("Title:")
        label.move(50, 100)
        self.title_display = QLineEdit(self)
        self.title_display.move(125, 100)

        label = QLabel(self)
        label.setText("Department:")
        label.move(50, 125)
        self.department_display = QLineEdit(self)
        self.department_display.move(125, 125)

        submit_data_button = QPushButton("Submit", self)
        submit_data_button.resize(100, 25)
        submit_data_button.move(50, 160)
        submit_data_button.clicked.connect(self.submit_button)

        cancel_data_button = QPushButton("Cancel", self)
        cancel_data_button.resize(100, 25)
        cancel_data_button.move(190, 160)
        cancel_data_button.clicked.connect(self.cancel_button)

    def cancel_button(self):
        self.entry_list_window.list_item_claimed()
        self.close()

    def submit_button(self):
        is_entry_claimed = DatabaseFunctions.is_entry_claimed(self.bsu_email, self.selected_data['entry_id'])
        if not is_entry_claimed:
            teacher_data = {
                "bsu_email" : self.bsu_email,
                "first_name" : self.first_name_display.text(),
                "last_name" : self.last_name_display.text(),
                "title" : self.title_display.text(),
                "department" : self.department_display.text()
            }
            DatabaseFunctions.add_teacher_row(teacher_data)
            reply = QMessageBox.information(
                self,
                'INFO',
                'User info logged',
                QMessageBox.Ok)
            DatabaseFunctions.accept_claim(teacher_data, self.selected_data)
            reply = QMessageBox.information(
                self,
                'INFO',
                'Project successfully claimed',
                QMessageBox.Ok)
            self.entry_list_window.update_data()
            self.entry_list_window.close_claim_login_window()
