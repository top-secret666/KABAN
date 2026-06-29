import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

from ui import LoginWindow, MainWindow, SplashScreen
from models import DBManager
from notification_scheduler import NotificationScheduler


def main():
    """
    Точка входа в приложение
    """
    # Создание приложения
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName('KABAN:manager')
    app.setWindowIcon(QIcon('ui/resources/icons/logo.png'))
    app.setFont(QFont('Segoe UI', 10))

    from ui.resources.theme_manager import apply_theme
    apply_theme(app)

    # Инициализация базы данных
    db_manager = DBManager('database/kaban.db')

    # Проверка существования директории для базы данных
    os.makedirs(os.path.dirname('database/kaban.db'), exist_ok=True)

    # Инициализация базы данных
    db_manager.connect()

    # Проверка структуры таблицы notifications
    def check_notifications_table():
        try:
            db_manager = DBManager('database/kaban.db')
            db_manager.connect()

            # Проверка существования таблицы
            cursor = db_manager.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
            if not cursor.fetchone():
                print("Таблица notifications не существует!")
                return False

            # Проверка структуры таблицы
            cursor = db_manager.conn.execute("PRAGMA table_info(notifications)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            required_columns = ['id', 'title', 'message', 'type', 'related_id', 'related_type', 'is_read', 'created_at', 'user_id']
            for col in required_columns:
                if col not in column_names:
                    print(f"В таблице notifications отсутствует столбец {col}!")
                    return False

            print("Структура таблицы notifications корректна.")
            return True
        except Exception as e:
            print(f"Ошибка при проверке таблицы notifications: {str(e)}")
            return False

    # Вызов функции проверки
    check_notifications_table()

    # Загрузка SQL-скрипта
    if not os.path.exists('database/kaban.db') or os.path.getsize('database/kaban.db') == 0:
        with open('database/kaban.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            db_manager.conn.executescript(sql_script)
            db_manager.commit()

    # Запуск проверок уведомлений
    notification_scheduler = NotificationScheduler()
    notification_scheduler.run_checks()

    # Отображение заставки
    splash = SplashScreen()
    splash.show()
    splash.start_progress()

    login_window = None
    main_window = None

    def show_login():
        nonlocal login_window, main_window
        print("Функция show_login вызвана")
        splash.close()
        print("Заставка закрыта")

        login_window = LoginWindow()
        print("Объект LoginWindow создан")

        if hasattr(login_window, 'exec_'):
            print("LoginWindow имеет метод exec_")
            if login_window.exec_():
                main_window = MainWindow(login_window.user)
                main_window.show()
        else:
            print("LoginWindow не имеет метода exec_, вызываем show()")
            login_window.show()

    QTimer.singleShot(3000, show_login)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
