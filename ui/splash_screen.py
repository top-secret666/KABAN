from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class SplashScreen(QSplashScreen):
    """
    Заставка при загрузке приложения
    """
    def __init__(self):
        # Создаем пиксмап для заставки
        pixmap = QPixmap('ui/resources/icons/app_icon.png')
        super().__init__(pixmap)
        
        # Создаем виджет для размещения элементов
        self.widget = QWidget(self)
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(20, pixmap.height() - 150, 20, 20)
        
        # Добавляем название приложения
        self.title_label = QLabel("KABAN:manager")
        self.title_label.setFont(QFont('Arial', 18, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Добавляем статус загрузки
        self.status_label = QLabel("Загрузка...")
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Добавляем прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid white;
                border-radius: 5px;
                background-color: transparent;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Добавляем версию
        self.version_label = QLabel("Версия 1.0.0")
        self.version_label.setFont(QFont('Arial', 8))
        self.version_label.setStyleSheet("color: white;")
        self.version_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.version_label)
        
        # Настраиваем таймер для имитации загрузки
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        
        # Список сообщений о загрузке
        self.loading_messages = [
            "Инициализация приложения...",
            "Подключение к базе данных...",
            "Загрузка компонентов интерфейса...",
            "Проверка обновлений...",
            "Загрузка пользовательских настроек...",
            "Подготовка рабочего пространства...",
            "Почти готово..."
        ]
    
    def start_progress(self):
        """
        Запуск имитации загрузки
        """
        self.timer.start(100)  # Обновление каждые 100 мс
    
    def update_progress(self):
        """
        Обновление прогресса загрузки
        """
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        
        # Обновляем сообщение о загрузке
        message_index = min(len(self.loading_messages) - 1, self.progress_value // 15)
        self.status_label.setText(self.loading_messages[message_index])
        
        # Если достигли 100%, останавливаем таймер
        if self.progress_value >= 100:
            self.timer.stop()
            self.close()
