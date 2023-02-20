import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QLabel, \
    QLineEdit, QCheckBox, QComboBox
from PySide6.QtGui import QCloseEvent

class EntriesWindow(QWidget):

    def __init__(self, entries_data):
        super().__init__()
        self.data = entries_data
        self.list_control = None
        self.data_window = None
        self.setup_window()


    def setup_window(self):
        self.setWindowTitle("CUBES Project Entries")
        display_list = QListWidget(self)
        self.list_control = display_list
        self.populate_display_list(self.data)
        display_list.resize(400, 350)
        display_list.currentItemChanged.connect(self.list_item_selected)
        self.setGeometry(300, 50, 400, 500)
        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(300, 400)
        self.show()

    def populate_display_list(self, data: list[dict]):
        for entries in data:
            display_text = f"{entries['entry_id']}\t\t{entries['organization_name']}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)

    def do_something_to_demo(self):
        message_box = QMessageBox(self)
        message_box.setText("You just pushed the button - imagine database work here")
        message_box.setWindowTitle("Comp490 Demo")
        message_box.show()

    def find_full_data_record(self, entry_id):
        for entry_record in self.data:
            if entry_record['entry_id'] == int(entry_id):
                return entry_record

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        selected_data = current.data(0)  # the data function has a 'role' choose 0 unless you extended QListWidgetItem
        entry_id = selected_data.split("\t")[0]  # split on tab and take the first resulting entry
        full_record = self.find_full_data_record(entry_id)
        print(full_record)
        self.data_window = EntryDataWindow(full_record)
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

    def __init__(self, entry_data:dict):
        super().__init__()
        self.data = entry_data
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle(f"{self.data['organization_name']}")
        self.setGeometry(750, 50, 500, 1000)  # put the new window next to the original one wider than it is tall

        label = QLabel(self)
        label.setText("Prefix: ")
        label.move(50, 50)
        prefix_display = QComboBox(self)
        prefix_display.addItems([" ", "Dr.", "Mrs.","Ms.","Mr."])
        prefix_display.move(200, 50)

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

        # Last name
        label = QLabel("Last Name: ", self)
        label.move(50, 110)

        last_name_display = QLineEdit(self.data['last_name'], self)
        last_name_display.move(200, 110)

        # Title
        label = QLabel("Title: ", self)
        label.move(50, 140)

        title_display = QLineEdit(self.data['title'], self)
        title_display.move(200, 140)

        # Organization Name
        label = QLabel("Organization: ", self)
        label.move(50, 170)

        organization_name_display = QLineEdit(self.data['organization_name'], self)
        organization_name_display.move(200, 170)

        # Organization Email
        label = QLabel("Email: ", self)
        label.move(50, 200)

        email_display = QLineEdit(self.data['email'], self)
        email_display.move(200, 200)

        # Organization Website
        label = QLabel("Website: ", self)
        label.move(50, 230)

        organization_website_display = QLineEdit(self.data['organization_website'], self)
        organization_website_display.move(200, 230)

        #Organization Phone Number
        label = QLabel("Phone Number: ", self)
        label.move(50, 260)

        phone_number_display = QLineEdit(self.data['phone_number'], self)
        phone_number_display.move(200, 260)

        # Opportunities interested in
        label = QLabel("Opportunities interested in: ", self)
        label.move(50, 300)

        label = QLabel("Course Project", self)
        label.move(70, 340)

        opp_course_proj_display = QCheckBox(self)
        opp_course_proj_display.move(180, 342)

        if self.data['opportunity_course_project'] != "":
            opp_course_proj_display.setChecked(1)
        label = QLabel("Guest Speaker", self)
        label.move(240, 340)
        opp_guest_speak_display = QCheckBox(self)
        opp_guest_speak_display.move(340, 342)
        if self.data['opportunity_guest_speaker'] != "":
            opp_guest_speak_display.setChecked(1)
        label = QLabel("Site Visit", self)
        label.move(70, 370)
        opp_site_visit_display = QCheckBox(self)
        opp_site_visit_display.move(180, 372)
        if self.data['opportunity_site_visit'] != "":
            opp_site_visit_display.setChecked(1)
        label = QLabel("Job Shadow", self)
        label.move(240, 370)
        opp_job_shadow_display = QCheckBox(self)
        opp_job_shadow_display.move(340, 372)
        if self.data['opportunity_job_shadow'] != "":
            opp_job_shadow_display.setChecked(1)
        label = QLabel("Internships", self)
        label.move(70, 400)
        opp_internships_display = QCheckBox(self)
        opp_internships_display.move(180, 402)
        if self.data['opportunity_internships'] != "":
            opp_internships_display.setChecked(1)
        label = QLabel("Career Panel", self)
        label.move(240, 400)
        opp_career_panel_display = QCheckBox(self)
        opp_career_panel_display.move(340, 402)
        if self.data['opportunity_career_panel'] != "":
            opp_career_panel_display.setChecked(1)
        label = QLabel("Networking Event", self)
        label.move(70, 430)
        opp_network_event_display = QCheckBox(self)
        opp_network_event_display.move(180, 432)
        if self.data['opportunity_networking_event'] != "":
            opp_network_event_display.setChecked(1)

        # Proposed collaboration time
        label = QLabel("Proposed collaboration time:", self)
        label.move(50, 470)
        label = QLabel("Summer 2022 (June 2022 - August 2022)", self)
        label.move(70, 510)
        collab_time_sum22_display = QCheckBox(self)
        collab_time_sum22_display.move(330, 512)
        if self.data['proposed_time_summer22'] != "":
            collab_time_sum22_display.setChecked(1)
        label = QLabel("Fall 2022 (September 2022 - December 2022)", self)
        label.move(70, 540)
        collab_time_fall22_display = QCheckBox(self)
        collab_time_fall22_display.move(330, 542)
        if self.data['proposed_time_fall22'] != "":
            collab_time_fall22_display.setChecked(1)
        label = QLabel("Spring 2023 (January 2023 - April 2023)", self)
        label.move(70, 570)
        collab_time_spring23_display = QCheckBox(self)
        collab_time_spring23_display.move(330, 572)
        if self.data['proposed_time_spring23'] != "":
            collab_time_spring23_display.setChecked(1)
        label = QLabel("Summer 2023 (June 2023 - August 2023)", self)
        label.move(70, 600)
        collab_time_sum23_display = QCheckBox(self)
        collab_time_sum23_display.move(330, 602)
        if self.data['proposed_time_summer23'] != "":
            collab_time_sum23_display.setChecked(1)
        label = QLabel("Other", self)
        label.move(70, 630)
        collab_time_other_display = QCheckBox(self)
        collab_time_other_display.move(330, 632)
        if self.data['proposed_time_other'] != "":
            collab_time_other_display.setChecked(1)

        # Permission to use organization name
        label = QLabel("Permission to use organization name?", self)
        label.move(50, 670)
        permission_to_use_name_display = QComboBox(self)
        permission_to_use_name_display.addItem("Yes")
        permission_to_use_name_display.addItem("No")
        permission_to_use_name_display.addItem("Further discussion is needed")

        permission = self.data['permission_to_use_org_name']
        if permission == "Yes":
            permission_to_use_name_display.setCurrentIndex(0)
        elif permission == "No":
            permission_to_use_name_display.setCurrentIndex(1)
        else:
            permission_to_use_name_display.setCurrentIndex(2)

        permission_to_use_name_display.move(50, 700)



