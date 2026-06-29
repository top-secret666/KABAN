from PyQt5.QtWidgets import QFormLayout, QMessageBox, QDateEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QDate

from controllers import ProjectController
from ui.dialogs.base_dialog import BaseDialog


class NewProjectDialog(BaseDialog):
    def __init__(self, parent=None, project=None):
        self.project = project
        self.project_controller = ProjectController()
        title = 'Редактирование проекта' if project else 'Новый проект'
        super().__init__(parent, title)
        self.setMinimumHeight(400)
        self._build()

    def _build(self):
        form = QFormLayout()
        form.setSpacing(12)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Название проекта')
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText('Клиент')
        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate().addMonths(1))
        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText('Бюджет')
        form.addRow('Название *', self.name_input)
        form.addRow('Клиент *', self.client_input)
        form.addRow('Дедлайн *', self.deadline_input)
        form.addRow('Бюджет *', self.budget_input)
        self.body_layout.addLayout(form)

        save_btn = QPushButton('Сохранить')
        save_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton('Отмена')
        cancel_btn.setObjectName('flat')
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)
        self.add_footer_button(cancel_btn)
        self.add_footer_button(save_btn)

        if self.project:
            self.name_input.setText(self.project.name)
            self.client_input.setText(self.project.client)
            if self.project.deadline:
                d = QDate.fromString(self.project.deadline, 'yyyy-MM-dd')
                if d.isValid():
                    self.deadline_input.setDate(d)
            self.budget_input.setText(str(self.project.budget))

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Укажите название проекта')
            return
        if not self.client_input.text().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Укажите клиента')
            return
        if not self.budget_input.text().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Укажите бюджет')
            return
        try:
            if float(self.budget_input.text()) <= 0:
                QMessageBox.warning(self, 'Предупреждение', 'Бюджет должен быть положительным')
                return
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Бюджет должен быть числом')
            return
        self.accept()
