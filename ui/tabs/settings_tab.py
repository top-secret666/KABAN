from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGroupBox, QFormLayout, QLineEdit, QCheckBox, QComboBox,
                             QTabWidget, QFileDialog, QMessageBox, QSpinBox, QColorDialog)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QSettings

from controllers import AuthController
from ui.widgets.tab_page import TabPage
from ui.resources.icon_helper import get_icon
from ui.resources.theme_manager import BG_PRESETS, apply_theme, get_config
from ui.dialogs.base_dialog import BaseDialog


class SettingsTab(QWidget):
    """
    Вкладка "Настройки" - настройки приложения и пользователя
    """

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.auth_controller = AuthController()
        self.settings = QSettings("KABAN", "KABAN:manager")
        self.init_ui()

    def init_ui(self):
        page = TabPage('Настройки', 'Профиль, интерфейс и база данных')
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)
        main_layout = page.content_layout

        self.tab_widget = QTabWidget()

        # Вкладка "Профиль"
        profile_tab = QWidget()
        profile_layout = QVBoxLayout(profile_tab)

        # Группа настроек профиля
        profile_group = QGroupBox("Профиль пользователя")
        profile_form = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setText(self.user.username)
        self.username_input.setReadOnly(True)

        self.email_input = QLineEdit()
        self.email_input.setText(self.user.email)

        self.full_name_input = QLineEdit()
        self.full_name_input.setText(self.user.full_name)

        self.role_label = QLabel(self.user.role)

        profile_form.addRow("Имя пользователя:", self.username_input)
        profile_form.addRow("Email:", self.email_input)
        profile_form.addRow("Полное имя:", self.full_name_input)
        profile_form.addRow("Роль:", self.role_label)

        profile_group.setLayout(profile_form)
        profile_layout.addWidget(profile_group)

        # Группа смены пароля
        password_group = QGroupBox("Смена пароля")
        password_form = QFormLayout()

        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        password_form.addRow("Текущий пароль:", self.current_password_input)
        password_form.addRow("Новый пароль:", self.new_password_input)
        password_form.addRow("Подтверждение пароля:", self.confirm_password_input)

        password_group.setLayout(password_form)
        profile_layout.addWidget(password_group)

        # Кнопки
        profile_buttons_layout = QHBoxLayout()

        save_profile_button = QPushButton("Сохранить изменения")
        save_profile_button.setIcon(get_icon('save'))
        save_profile_button.clicked.connect(self.save_profile)

        change_password_button = QPushButton("Изменить пароль")
        change_password_button.setIcon(get_icon('edit'))
        change_password_button.clicked.connect(self.change_password)

        profile_buttons_layout.addWidget(save_profile_button)
        profile_buttons_layout.addWidget(change_password_button)

        profile_layout.addLayout(profile_buttons_layout)
        profile_layout.addStretch()

        # Вкладка "Интерфейс"
        interface_tab = QWidget()
        interface_layout = QVBoxLayout(interface_tab)

        # Группа настроек интерфейса
        interface_group = QGroupBox("Настройки интерфейса")
        interface_form = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Светлая", "light")
        self.theme_combo.addItem("Тёмная", "dark")
        current_theme = self.settings.value("theme", "light")
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        self.theme_combo.currentIndexChanged.connect(self._preview_theme)

        self.bg_preset_combo = QComboBox()
        self.bg_preset_combo.addItem("По умолчанию", "default")
        self.bg_preset_combo.addItem("Серый", "gray")
        self.bg_preset_combo.addItem("Голубой", "blue")
        self.bg_preset_combo.addItem("Мятный", "mint")
        self.bg_preset_combo.addItem("Тёплый", "warm")
        self.bg_preset_combo.addItem("Тёмно-серый", "dark_gray")
        self.bg_preset_combo.addItem("Тёмно-синий", "dark_blue")
        self.bg_preset_combo.addItem("Свой цвет…", "custom")
        preset = self.settings.value("bg_preset", "default")
        pi = self.bg_preset_combo.findData(preset)
        if pi >= 0:
            self.bg_preset_combo.setCurrentIndex(pi)
        self.bg_preset_combo.currentIndexChanged.connect(self._on_bg_preset_changed)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 16)
        self.font_size_spin.setValue(int(self.settings.value("font_size", 10)))

        self.accent_color_button = QPushButton()
        self.accent_color_button.setFixedSize(36, 28)
        self.accent_color = QColor(self.settings.value("accent_color", "#2FC6F6"))
        self.accent_color_button.setStyleSheet(
            f"background-color: {self.accent_color.name()}; border: 1px solid #888; border-radius: 4px;"
        )
        self.accent_color_button.clicked.connect(self.choose_accent_color)

        self.bg_color_button = QPushButton()
        self.bg_color_button.setFixedSize(36, 28)
        self.bg_color = QColor(self.settings.value("bg_color", "#EDEEF0"))
        self.bg_color_button.setStyleSheet(
            f"background-color: {self.bg_color.name()}; border: 1px solid #888; border-radius: 4px;"
        )
        self.bg_color_button.clicked.connect(self.choose_bg_color)

        interface_form.addRow("Тема:", self.theme_combo)
        interface_form.addRow("Фон рабочей области:", self.bg_preset_combo)
        interface_form.addRow("Свой цвет фона:", self.bg_color_button)
        interface_form.addRow("Размер шрифта:", self.font_size_spin)
        interface_form.addRow("Цвет акцента:", self.accent_color_button)

        interface_group.setLayout(interface_form)
        interface_layout.addWidget(interface_group)

        # Группа настроек таблиц
        table_group = QGroupBox("Настройки таблиц")
        table_form = QFormLayout()

        self.rows_per_page_spin = QSpinBox()
        self.rows_per_page_spin.setRange(10, 100)
        self.rows_per_page_spin.setValue(int(self.settings.value("rows_per_page", 20)))

        self.alternate_row_colors_check = QCheckBox()
        self.alternate_row_colors_check.setChecked(self.settings.value("alternate_row_colors", True, type=bool))

        table_form.addRow("Строк на странице:", self.rows_per_page_spin)
        table_form.addRow("Чередовать цвета строк:", self.alternate_row_colors_check)

        table_group.setLayout(table_form)
        interface_layout.addWidget(table_group)

        # Кнопки
        interface_buttons_layout = QHBoxLayout()

        save_interface_button = QPushButton("Применить")
        save_interface_button.setIcon(get_icon('save'))
        save_interface_button.clicked.connect(self.save_interface_settings)

        preview_button = QPushButton("Предпросмотр")
        preview_button.setObjectName('flat')
        preview_button.clicked.connect(self._preview_theme)

        reset_interface_button = QPushButton("Сбросить")
        reset_interface_button.setIcon(get_icon('refresh'))
        reset_interface_button.clicked.connect(self.reset_interface_settings)

        interface_buttons_layout.addWidget(save_interface_button)
        interface_buttons_layout.addWidget(preview_button)
        interface_buttons_layout.addWidget(reset_interface_button)

        interface_layout.addLayout(interface_buttons_layout)
        interface_layout.addStretch()
        self._on_bg_preset_changed()

        # Вкладка "База данных"
        database_tab = QWidget()
        database_layout = QVBoxLayout(database_tab)

        # Группа настроек базы данных
        database_group = QGroupBox("Настройки базы данных")
        database_form = QFormLayout()

        self.db_path_input = QLineEdit()
        self.db_path_input.setText(self.settings.value("db_path", "database/kaban.db"))
        self.db_path_input.setReadOnly(True)

        self.browse_db_button = QPushButton("Обзор...")
        self.browse_db_button.clicked.connect(self.browse_db_path)

        db_path_layout = QHBoxLayout()
        db_path_layout.addWidget(self.db_path_input)
        db_path_layout.addWidget(self.browse_db_button)

        self.backup_path_input = QLineEdit()
        self.backup_path_input.setText(self.settings.value("backup_path", "database/backup"))
        self.backup_path_input.setReadOnly(True)

        self.browse_backup_button = QPushButton("Обзор...")
        self.browse_backup_button.clicked.connect(self.browse_backup_path)

        backup_path_layout = QHBoxLayout()
        backup_path_layout.addWidget(self.backup_path_input)
        backup_path_layout.addWidget(self.browse_backup_button)

        self.auto_backup_check = QCheckBox()
        self.auto_backup_check.setChecked(self.settings.value("auto_backup", True, type=bool))

        database_form.addRow("Путь к базе данных:", db_path_layout)
        database_form.addRow("Путь для резервных копий:", backup_path_layout)
        database_form.addRow("Автоматическое резервное копирование:", self.auto_backup_check)

        database_group.setLayout(database_form)
        database_layout.addWidget(database_group)

        # Кнопки
        database_buttons_layout = QHBoxLayout()

        save_database_button = QPushButton("Сохранить настройки")
        save_database_button.setIcon(get_icon('save'))
        save_database_button.clicked.connect(self.save_database_settings)

        backup_now_button = QPushButton("Создать резервную копию")
        backup_now_button.setIcon(get_icon('backup'))
        backup_now_button.clicked.connect(self.create_backup)

        database_buttons_layout.addWidget(save_database_button)
        database_buttons_layout.addWidget(backup_now_button)

        database_layout.addLayout(database_buttons_layout)
        database_layout.addStretch()

        # Добавление вкладок
        self.tab_widget.addTab(profile_tab, "Профиль")
        self.tab_widget.addTab(interface_tab, "Интерфейс")
        self.tab_widget.addTab(database_tab, "База данных")

        main_layout.addWidget(self.tab_widget)

    def save_profile(self):
        """
        Сохранение изменений профиля
        """
        # Получение данных из полей
        email = self.email_input.text()
        full_name = self.full_name_input.text()

        # Проверка заполнения обязательных полей
        if not email or not full_name:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля")
            return

        # Проверка формата email (простая проверка)
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите корректный email")
            return

        # Обновление данных пользователя
        user_data = {
            'email': email,
            'full_name': full_name
        }

        result = self.auth_controller.update_user(self.user.id, user_data)

        if result['success']:
            # Обновление данных пользователя в памяти
            self.user.email = email
            self.user.full_name = full_name

            QMessageBox.information(self, "Успех", "Профиль успешно обновлен")
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])

    def change_password(self):
        """
        Изменение пароля пользователя
        """
        # Получение данных из полей
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Проверка заполнения всех полей
        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля")
            return

        # Проверка совпадения паролей
        if new_password != confirm_password:
            QMessageBox.warning(self, "Предупреждение", "Новый пароль и подтверждение не совпадают")
            return

        # Изменение пароля
        result = self.auth_controller.change_password(self.user.id, current_password, new_password)

        if result['success']:
            QMessageBox.information(self, "Успех", "Пароль успешно изменен")

            # Очистка полей
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])

    def _on_bg_preset_changed(self):
        preset = self.bg_preset_combo.currentData()
        if preset == 'custom':
            self.bg_color_button.setEnabled(True)
        else:
            self.bg_color_button.setEnabled(False)
            color = BG_PRESETS.get(preset, '')
            if color:
                self.bg_color = QColor(color)
                self.bg_color_button.setStyleSheet(
                    f"background-color: {color}; border: 1px solid #888; border-radius: 4px;"
                )
        self._preview_theme()

    def _build_theme_config(self):
        preset = self.bg_preset_combo.currentData()
        bg_color = ''
        if preset == 'custom':
            bg_color = self.bg_color.name()
        elif preset and preset != 'default':
            bg_color = BG_PRESETS.get(preset, '')
        return {
            'theme': self.theme_combo.currentData(),
            'accent': self.accent_color.name(),
            'bg_main': bg_color,
            'bg_preset': preset,
            'font_size': self.font_size_spin.value(),
        }

    def _refresh_main_window(self):
        win = self.window()
        if win and hasattr(win, 'apply_theme'):
            win.apply_theme()

    def _preview_theme(self):
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            apply_theme(app, self._build_theme_config())
            self._refresh_main_window()

    def choose_accent_color(self):
        """
        Выбор цвета акцента
        """
        color = QColorDialog.getColor(self.accent_color, self, "Выберите цвет акцента")

        if color.isValid():
            self.accent_color = color
            self.accent_color_button.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #888; border-radius: 4px;"
            )

            self.accent_color_button.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #888; border-radius: 4px;"
            )

    def choose_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self, "Цвет фона рабочей области")
        if color.isValid():
            self.bg_color = color
            self.bg_color_button.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #888; border-radius: 4px;"
            )
            idx = self.bg_preset_combo.findData('custom')
            if idx >= 0:
                self.bg_preset_combo.setCurrentIndex(idx)

    def save_interface_settings(self):
        config = self._build_theme_config()
        self.settings.setValue("theme", config['theme'])
        self.settings.setValue("font_size", config['font_size'])
        self.settings.setValue("accent_color", config['accent'])
        self.settings.setValue("bg_preset", config['bg_preset'])
        self.settings.setValue("bg_color", config['bg_main'] or self.bg_color.name())
        self.settings.setValue("rows_per_page", self.rows_per_page_spin.value())
        self.settings.setValue("alternate_row_colors", self.alternate_row_colors_check.isChecked())

        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            apply_theme(app, config)

        QMessageBox.information(self, "Успех", "Настройки интерфейса применены.")

    def reset_interface_settings(self):
        """
        Сброс настроек интерфейса
        """
        # Подтверждение сброса
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите сбросить настройки интерфейса?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.theme_combo.setCurrentIndex(self.theme_combo.findData("light"))
            self.bg_preset_combo.setCurrentIndex(self.bg_preset_combo.findData("default"))
            self.font_size_spin.setValue(10)
            self.accent_color = QColor("#2FC6F6")
            self.bg_color = QColor("#EDEEF0")
            self.accent_color_button.setStyleSheet(
                f"background-color: {self.accent_color.name()}; border: 1px solid #888; border-radius: 4px;"
            )
            self.bg_color_button.setStyleSheet(
                f"background-color: {self.bg_color.name()}; border: 1px solid #888; border-radius: 4px;"
            )
            self.rows_per_page_spin.setValue(20)
            self.alternate_row_colors_check.setChecked(True)
            self.save_interface_settings()

    def browse_db_path(self):
        """
        Выбор пути к базе данных
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбор файла базы данных", "", "SQLite Database (*.db);;All Files (*)"
        )

        if file_path:
            self.db_path_input.setText(file_path)

    def browse_backup_path(self):
        """
        Выбор пути для резервных копий
        """
        dir_path = QFileDialog.getExistingDirectory(
            self, "Выбор директории для резервных копий", ""
        )

        if dir_path:
            self.backup_path_input.setText(dir_path)

    def save_database_settings(self):
        """
        Сохранение настроек базы данных
        """
        # Получение данных из полей
        db_path = self.db_path_input.text()
        backup_path = self.backup_path_input.text()
        auto_backup = self.auto_backup_check.isChecked()

        # Сохранение настроек
        self.settings.setValue("db_path", db_path)
        self.settings.setValue("backup_path", backup_path)
        self.settings.setValue("auto_backup", auto_backup)

        QMessageBox.information(self, "Успех",
                                "Настройки базы данных сохранены. Изменения вступят в силу после перезапуска приложения.")

    def create_backup(self):
        """
        Создание резервной копии базы данных
        """
        import shutil
        import os
        from datetime import datetime

        # Получение путей
        db_path = self.db_path_input.text()
        backup_path = self.backup_path_input.text()

        # Проверка существования файла базы данных
        if not os.path.exists(db_path):
            QMessageBox.warning(self, "Предупреждение", "Файл базы данных не найден")
            return

        # Создание директории для резервных копий, если она не существует
        os.makedirs(backup_path, exist_ok=True)

        # Формирование имени файла резервной копии
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_path, f"kaban_backup_{timestamp}.db")

        try:
            # Копирование файла базы данных
            shutil.copy2(db_path, backup_file)
            QMessageBox.information(self, "Успех", f"Резервная копия успешно создана: {backup_file}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать резервную копию: {str(e)}")
