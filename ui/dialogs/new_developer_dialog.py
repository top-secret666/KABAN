from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                             QLineEdit, QPushButton, QComboBox)

from controllers import DeveloperController
from ui.dialogs.base_dialog import BaseDialog


class NewDeveloperDialog(BaseDialog):
    """Диалог добавления/редактирования разработчика."""

    def __init__(self, parent=None, developer=None):
        self.developer = developer
        self.developer_controller = DeveloperController()
        title = 'Редактирование разработчика' if developer else 'Новый разработчик'
        super().__init__(parent, title)
        self.setMinimumHeight(280)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('ФИО')
        self.position_combo = QComboBox()
        positions_result = self.developer_controller.get_developer_positions()
        if positions_result['success']:
            for position in positions_result['data']:
                self.position_combo.addItem(position, position)
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText('Ставка в час')
        form.addRow('ФИО *', self.name_input)
        form.addRow('Должность *', self.position_combo)
        form.addRow('Ставка *', self.rate_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addStretch()
        save_btn = QPushButton('Сохранить')
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton('Отмена')
        cancel_btn.setObjectName('flat')
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

        if self.developer:
            self.name_input.setText(self.developer.full_name)
            idx = self.position_combo.findData(self.developer.position)
            if idx >= 0:
                self.position_combo.setCurrentIndex(idx)
            self.rate_input.setText(str(self.developer.hourly_rate))

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Укажите ФИО')
            return
        if not self.rate_input.text().strip():
            QMessageBox.warning(self, 'Предупреждение', 'Укажите ставку')
            return
        try:
            if float(self.rate_input.text()) <= 0:
                QMessageBox.warning(self, 'Предупреждение', 'Ставка должна быть положительной')
                return
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Ставка должна быть числом')
            return
        self.accept()
