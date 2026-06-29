from PyQt5.QtWidgets import QFormLayout, QMessageBox, QComboBox, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QDoubleValidator

from controllers import TaskController, ProjectController, DeveloperController
from ui.dialogs.base_dialog import BaseDialog
from ui.resources.icon_helper import get_icon


class TaskDialog(BaseDialog):
    def __init__(self, parent=None, task=None, default_status=None, default_developer_id=None):
        self.task = task
        self._default_status = default_status
        self._default_developer_id = default_developer_id
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.developer_controller = DeveloperController()
        title = 'Редактирование задачи' if task else 'Новая задача'
        super().__init__(parent, title)
        self.setWindowIcon(get_icon('task'))
        self.setMinimumHeight(460)
        self._build()

    def _build(self):
        form = QFormLayout()
        form.setSpacing(12)
        self.project_combo = QComboBox()
        self._load_projects()
        self.developer_combo = QComboBox()
        self._load_developers()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Описание задачи')
        self.description_input.setMinimumHeight(100)
        self.status_combo = QComboBox()
        statuses_result = self.task_controller.get_task_statuses()
        if statuses_result['success']:
            for status in statuses_result['data']:
                self.status_combo.addItem(status, status)
        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('0')
        self.hours_input.setValidator(QDoubleValidator(0, 1000, 2))
        form.addRow('Проект *', self.project_combo)
        form.addRow('Разработчик *', self.developer_combo)
        form.addRow('Описание *', self.description_input)
        form.addRow('Статус *', self.status_combo)
        form.addRow('Часы', self.hours_input)
        self.body_layout.addLayout(form)

        save_btn = QPushButton('Сохранить')
        save_btn.setIcon(get_icon('save'))
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton('Отмена')
        cancel_btn.setObjectName('flat')
        cancel_btn.clicked.connect(self.reject)
        self.add_footer_button(cancel_btn)
        self.add_footer_button(save_btn)

        if self.task:
            pi = self.project_combo.findData(self.task.project_id)
            if pi >= 0:
                self.project_combo.setCurrentIndex(pi)
            di = self.developer_combo.findData(self.task.developer_id)
            if di >= 0:
                self.developer_combo.setCurrentIndex(di)
            self.description_input.setText(self.task.description)
            si = self.status_combo.findText(self.task.status)
            if si >= 0:
                self.status_combo.setCurrentIndex(si)
            self.hours_input.setText(str(self.task.hours_worked or 0))
        else:
            if self._default_status:
                si = self.status_combo.findText(self._default_status)
                if si >= 0:
                    self.status_combo.setCurrentIndex(si)
            if self._default_developer_id is not None:
                di = self.developer_combo.findData(self._default_developer_id)
                if di >= 0:
                    self.developer_combo.setCurrentIndex(di)

    def _load_projects(self):
        result = self.project_controller.get_all_projects()
        if result['success']:
            for project in result['data']:
                self.project_combo.addItem(project.name, project.id)

    def _load_developers(self):
        result = self.developer_controller.get_all_developers()
        if result['success']:
            for developer in result['data']:
                self.developer_combo.addItem(developer.full_name, developer.id)

    def accept(self):
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Заполните описание задачи')
            return
        if self.project_combo.currentIndex() < 0:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите проект')
            return
        if self.developer_combo.currentIndex() < 0:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите разработчика')
            return
        if self.hours_input.text().strip():
            try:
                if float(self.hours_input.text()) < 0:
                    QMessageBox.warning(self, 'Предупреждение', 'Часы не могут быть отрицательными')
                    return
            except ValueError:
                QMessageBox.warning(self, 'Предупреждение', 'Часы должны быть числом')
                return
        super().accept()
