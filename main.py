import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer

from paths import ROOT_DIR, resource_path
from database.bootstrap import ensure_database
from notification_scheduler import NotificationScheduler
from ui import LoginWindow, MainWindow, SplashScreen


def main():
    os.chdir(ROOT_DIR)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName('KABAN:manager')
    app.setWindowIcon(QIcon(resource_path('ui', 'resources', 'icons', 'logo.png')))
    app.setFont(QFont('Segoe UI', 10))

    from ui.resources.theme_manager import apply_theme
    apply_theme(app)

    ensure_database()

    notification_scheduler = NotificationScheduler()
    notification_scheduler.run_checks()

    splash = SplashScreen()
    splash.show()
    splash.start_progress()

    def show_login():
        splash.close()
        login_window = LoginWindow()
        if login_window.exec_():
            main_window = MainWindow(login_window.user)
            main_window.show()

    QTimer.singleShot(2500, show_login)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
