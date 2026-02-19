import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

from src.main.ui import LoginWindow, MainWindow, SplashScreen
from src.main.models import DBManager


def main():
    """
    Точка входа в приложение
    """
    # Создание приложения
    app = QApplication(sys.argv)
    app.setApplicationName('KABAN:manager')
    app.setWindowIcon(QIcon('ui/resources/icons/app_icon.png'))

    # Инициализация базы данных
    db_manager = DBManager('database/kaban.db')

    # Проверка существования директории для базы данных
    os.makedirs(os.path.dirname('database/kaban.db'), exist_ok=True)

    # Инициализация базы данных
    db_manager.connect()

    # Загрузка SQL-скрипта
    if not os.path.exists('database/kaban.db') or os.path.getsize('database/kaban.db') == 0:
        with open('database/kaban.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            db_manager.conn.executescript(sql_script)
            db_manager.commit()

    # Отображение заставки
    splash = SplashScreen()
    splash.show()
    splash.start_progress()

    # Задержка для отображения заставки
    def show_login():
        splash.close()

        # Отображение окна входа
        login_window = LoginWindow()
        login_window.show()

        # Если вход успешен, отображаем главное окно
        if hasattr(login_window, 'exec_'):
            result = login_window.exec_()
            print(f"LoginWindow exec_() result: {result}")
            if result:
                print(f"LoginWindow user: {getattr(login_window, 'user', None)}")
                if hasattr(login_window, 'user') and login_window.user:
                    global main_window
                    main_window = MainWindow(login_window.user)
                    print("MainWindow created")
                    main_window.show()
                else:
                    print("User not found after login!")
            else:
                print("Login cancelled or failed.")
        else:
            login_window.exec_()

    # Запуск таймера для отображения окна входа после заставки
    QTimer.singleShot(3000, show_login)

    # Запуск приложения
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
