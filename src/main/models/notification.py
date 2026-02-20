from .db_manager import DBManager
from datetime import datetime


class Notification:
    def __init__(self, id=None, title=None, message=None, type=None,
                 related_id=None, related_type=None, is_read=False,
                 created_at=None, db_manager=None):

        self.id = id
        self.title = title
        self.message = message
        self.type = type or 'info'
        self.related_id = related_id
        self.related_type = related_type
        self.is_read = is_read
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db_manager = db_manager or DBManager()

    def validate(self):
        if not self.title:
            return False, "Заголовок уведомления не может быть пустым"

        if not self.message:
            return False, "Текст уведомления не может быть пустым"

        valid_types = ['info', 'warning', 'error']
        if self.type not in valid_types:
            return False, f"Недопустимый тип уведомления. Допустимые значения: {', '.join(valid_types)}"

        return True, None

    def save(self):
        try:
            is_valid, error_message = self.validate()
            if not is_valid:
                return False, error_message

            self.db_manager.connect()

            if self.id:
                query = """
                    UPDATE notifications
                    SET title = ?, message = ?, type = ?, related_id = ?, 
                        related_type = ?, is_read = ?
                    WHERE id = ?
                """
                self.db_manager.conn.execute(query, (
                    self.title, self.message, self.type, self.related_id,
                    self.related_type, self.is_read, self.id
                ))
            else:
                query = """
                    INSERT INTO notifications (title, message, type, related_id, 
                                              related_type, is_read, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor = self.db_manager.conn.execute(query, (
                    self.title, self.message, self.type, self.related_id,
                    self.related_type, self.is_read, self.created_at
                ))
                self.id = cursor.lastrowid

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def delete(self):
        try:
            if not self.id:
                return False, "Невозможно удалить уведомление без ID"

            self.db_manager.connect()

            query = "DELETE FROM notifications WHERE id = ?"
            self.db_manager.conn.execute(query, (self.id,))

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def mark_as_read(self):
        try:
            if not self.id:
                return False, "Невозможно обновить уведомление без ID"

            self.is_read = True

            self.db_manager.connect()

            query = "UPDATE notifications SET is_read = 1 WHERE id = ?"
            self.db_manager.conn.execute(query, (self.id,))

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    @classmethod
    def get_by_id(cls, notification_id, db_manager=None):
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
