import os
import platform
import subprocess
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from about import AboutWindow


class GradesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""
        self.file_header = ""
        self.about_window = None

        self.setWindowTitle("Grades Updater")
        self.setMinimumSize(760, 620)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        header_layout = QHBoxLayout()
        title_label = QLabel("Grades File Updater")
        title_label.setObjectName("titleLabel")
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.open_about)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.about_button)

        control_card = QFrame()
        control_card.setObjectName("controlCard")
        control_layout = QHBoxLayout(control_card)
        control_layout.setContentsMargins(14, 12, 14, 12)
        control_layout.setSpacing(10)

        self.load_button = QPushButton("Select Grades File")
        self.load_button.clicked.connect(self.load_file)

        self.file_label = QLabel("No file loaded")
        self.file_label.setObjectName("fileLabel")

        bonus_label = QLabel("Bonus Points:")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 100)
        self.bonus_input.setFixedWidth(90)
        self.bonus_input.lineEdit().returnPressed.connect(self.apply_bonus)

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.update_file)

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.file_label)
        control_layout.addStretch()
        control_layout.addWidget(bonus_label)
        control_layout.addWidget(self.bonus_input)
        control_layout.addWidget(self.update_button)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(control_card)
        main_layout.addWidget(self.table)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Grades File",
            os.path.dirname(__file__),
            "CSV Files (*.csv);;All Files (*)",
        )
        if not file_path:
            return

        self.selected_file = file_path
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()

        if not lines:
            return

        self.file_header = lines[0].strip()

        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split(",")
            student_id = parts[0].strip()
            grade = float(parts[1].strip())
            if grade.is_integer():
                grade = int(grade)
            self.student_ids.append(student_id)
            self.original_grades.append(grade)
            self.corrected_grades.append(grade)

        self.bonus_input.setValue(0)
        self.file_label.setText(os.path.basename(self.selected_file))
        self.update_table()

    def update_table(self):
        self.table.clearContents()
        self.table.setRowCount(max(50, len(self.student_ids)))

        for row in range(len(self.student_ids)):
            values = [
                str(self.student_ids[row]),
                str(self.original_grades[row]),
                str(self.corrected_grades[row]),
            ]
            for col in range(3):
                item = QTableWidgetItem(values[col])
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def apply_bonus(self):
        self.bonus_input.interpretText()
        bonus = self.bonus_input.value()

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select a grades file first.")
            return

        with open(self.selected_file, "w", encoding="utf-8", newline="") as file:
            file.write(self.file_header + "\n")
            for i in range(len(self.student_ids)):
                file.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

        self.open_file_externally(self.selected_file)

    def open_file_externally(self, file_path):
        system_name = platform.system()
        if system_name == "Windows":
            os.startfile(file_path)
        elif system_name == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])

    def open_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())
    window = GradesWindow()
    window.show()
    sys.exit(app.exec())
