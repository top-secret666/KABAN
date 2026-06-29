from models.db_manager import DBManager
from datetime import datetime


class Notification:
    """
    Модель уведомления
    """

    def __init__(self, id=None, title=None, message=None, type=None,
                 related_id=None, related_type=None, is_read=False,
                 created_at=None, user_id=None, db_manager=None):
        """
        Инициализирует объект уведомления

        Args:
            id: ID уведомления
            title: Заголовок уведомления
            message: Текст уведомления
            type: Тип уведомления (info, warning, error)
            related_id: ID связанного объекта (проекта, задачи и т.д.)
            related_type: Тип связанного объекта (project, task, developer)
            is_read: Прочитано ли уведомление
            created_at: Дата и время создания уведомления
            user_id: ID пользователя, которому адресовано уведомление
            db_manager: Менеджер базы данных
        """
        self.id = id
        self.title = title
        self.message = message
        self.type = type or 'info'
        self.related_id = related_id
        self.related_type = related_type
        self.is_read = is_read
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.user_id = user_id
        self.db_manager = db_manager or DBManager()

    def save(self):
        """
        Сохраняет уведомление в базу данных

        Returns:
            tuple: (success, error)
        """
        try:
            # Валидация данных
            is_valid, error_message = self.validate()
            if not is_valid:
                return False, error_message

            # Подключение к базе данных
            self.db_manager.connect()

            if self.id:
                # Обновление существующего уведомления
                query = """
                    UPDATE notifications
                    SET title = ?, message = ?, type = ?, related_id = ?, 
                        related_type = ?, is_read = ?, user_id = ?
                    WHERE id = ?
                """
                self.db_manager.conn.execute(query, (
                    self.title, self.message, self.type, self.related_id,
                    self.related_type, self.is_read, self.user_id, self.id
                ))
            else:
                # Создание нового уведомления
                query = """
                    INSERT INTO notifications (title, message, type, related_id, 
                                              related_type, is_read, created_at, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor = self.db_manager.conn.execute(query, (
                    self.title, self.message, self.type, self.related_id,
                    self.related_type, self.is_read, self.created_at, self.user_id
                ))
                self.id = cursor.lastrowid

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)
    
    def delete(self):
        """
        Удаляет уведомление из базы данных
        
        Returns:
            tuple: (success, error)
        """
        try:
            if not self.id:
                return False, "Невозможно удалить уведомление без ID"
            
            # Подключение к базе данных
            self.db_manager.connect()
            
            # Удаление уведомления
            query = "DELETE FROM notifications WHERE id = ?"
            self.db_manager.conn.execute(query, (self.id,))
            
            self.db_manager.commit()
            return True, None
        
        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def validate(self):
        """
        Валидирует данные уведомления

        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.title:
            return False, "Заголовок уведомления не может быть пустым"

        if not self.message:
            return False, "Текст уведомления не может быть пустым"

        valid_types = ['info', 'warning', 'error']
        if self.type not in valid_types:
            return False, f"Недопустимый тип уведомления. Допустимые значения: {', '.join(valid_types)}"

        return True, None

    def mark_as_read(self):
        """
        Отмечает уведомление как прочитанное
        
        Returns:
            tuple: (success, error)
        """
        try:
            if not self.id:
                return False, "Невозможно обновить уведомление без ID"
            
            self.is_read = True
            
            # Подключение к базе данных
            self.db_manager.connect()
            
            # Обновление статуса уведомления
            query = "UPDATE notifications SET is_read = 1 WHERE id = ?"
            self.db_manager.conn.execute(query, (self.id,))
            
            self.db_manager.commit()
            return True, None
        
        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)
    
    @classmethod
    def get_by_id(cls, notification_id, db_manager=None):
        """
        Получает уведомление по ID
        
        Args:
            notification_id: ID уведомления
            db_manager: Менеджер базы данных
        
        Returns:
            Notification: Объект уведомления или None, если не найдено
        """
        db_manager = db_manager or DBManager()
        
        try:
            db_manager.connect()
            
            query = """
                SELECT id, title, message, type, related_id, related_type, 
                       is_read, created_at
                FROM notifications
                WHERE id = ?
            """
            cursor = db_manager.conn.execute(query, (notification_id,))
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row[0],
                    title=row[1],
                    message=row[2],
                    type=row[3],
                    related_id=row[4],
                    related_type=row[5],
                    is_read=bool(row[6]),
                    created_at=row[7],
                    db_manager=db_manager
                )
            
            return None
        
        except Exception:
            return None
    
    @classmethod
    def get_all(cls, limit=None, offset=None, only_unread=False, db_manager=None):
        """
        Получает список уведомлений
        
        Args:
            limit: Ограничение количества результатов
            offset: Смещение результатов
            only_unread: Только непрочитанные уведомления
            db_manager: Менеджер базы данных
        
        Returns:
            list: Список объектов уведомлений
        """
        db_manager = db_manager or DBManager()
        
        try:
            db_manager.connect()
            
            query = """
                SELECT id, title, message, type, related_id, related_type, 
                       is_read, created_at
                FROM notifications
            """
            params = []
            
            if only_unread:
                query += " WHERE is_read = 0"
            
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            if offset:
                query += " OFFSET ?"
                params.append(offset)
            
            cursor = db_manager.conn.execute(query, params)
            
            notifications = []
            for row in cursor.fetchall():
                notification = cls(
                    id=row[0],
                    title=row[1],
                    message=row[2],
                    type=row[3],
                    related_id=row[4],
                    related_type=row[5],
                    is_read=bool(row[6]),
                    created_at=row[7],
                    db_manager=db_manager
                )
                notifications.append(notification)
            
            return notifications
        
        except Exception:
            return []
