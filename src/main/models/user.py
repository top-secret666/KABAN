from db_manager import DBManager
import hashlib
import os
from datetime import datetime


class User:
    def __init__(self, id=None, username=None, password=None, email=None,
                 full_name=None, role=None, is_active=True, last_login=None,
                 created_at=None, db_manager=None):

        self.id = id
        self.username = username
        self.password = password  # Хранится в хешированном виде
        self.email = email
        self.full_name = full_name
        self.role = role or 'developer'
        self.is_active = is_active
        self.last_login = last_login
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db_manager = db_manager or DBManager()

    def validate(self):
        if not self.username:
            return False, "Имя пользователя не может быть пустым"

        if not self.password and not self.id:
            return False, "Пароль не может быть пустым"

        if not self.email:
            return False, "Email не может быть пустым"

        if not self.full_name:
            return False, "Полное имя не может быть пустым"

        valid_roles = ['admin', 'manager', 'developer']
        if self.role not in valid_roles:
            return False, f"Недопустимая роль. Допустимые значения: {', '.join(valid_roles)}"

        return True, None

    def save(self):
        try:
            is_valid, error_message = self.validate()
            if not is_valid:
                return False, error_message

            self.db_manager.connect()

            if self.id:
                query = """
                    UPDATE users
                    SET username = ?, email = ?, full_name = ?, 
                        role = ?, is_active = ?
                """
                params = [
                    self.username, self.email, self.full_name,
                    self.role, self.is_active
                ]

                if self.password and not self.password.startswith('$'):
                    hashed_password = self._hash_password(self.password)
                    query += ", password = ?"
                    params.append(hashed_password)

                query += " WHERE id = ?"
                params.append(self.id)

                self.db_manager.conn.execute(query, params)
            else:
                hashed_password = self._hash_password(self.password)

                query = """
                    INSERT INTO users (username, password, email, full_name, 
                                      role, is_active, last_login, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor = self.db_manager.conn.execute(query, (
                    self.username, hashed_password, self.email, self.full_name,
                    self.role, self.is_active, self.last_login, self.created_at
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
                return False, "Невозможно удалить пользователя без ID"

            self.db_manager.connect()

            query = "DELETE FROM users WHERE id = ?"
            self.db_manager.conn.execute(query, (self.id,))

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def update_last_login(self):
        try:
            if not self.id:
                return False, "Невозможно обновить пользователя без ID"

            self.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.db_manager.connect()

            query = "UPDATE users SET last_login = ? WHERE id = ?"
            self.db_manager.conn.execute(query, (self.last_login, self.id))

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def _hash_password(self, password):
        salt = os.urandom(16).hex()

        hashed = hashlib.sha256((password + salt).encode()).hexdigest()

        return f"${salt}${hashed}"

    def check_password(self, password):
        if not self.password or not password:
            return False

        parts = self.password.split('$')
        if len(parts) != 3:
            return False

        salt = parts[1]
        stored_hash = parts[2]

        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()

        return computed_hash == stored_hash

    @classmethod
    def get_by_id(cls, user_id, db_manager=None):
        db_manager = db_manager or DBManager()

        try:
            db_manager.connect()

            query = """
                SELECT id, username, password, email, full_name, 
                       role, is_active, last_login, created_at
                FROM users
                WHERE id = ?
            """
            cursor = db_manager.conn.execute(query, (user_id,))
            row = cursor.fetchone()

            if row:
                return cls(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3],
                    full_name=row[4],
                    role=row[5],
                    is_active=bool(row[6]),
                    last_login=row[7],
                    created_at=row[8],
                    db_manager=db_manager
                )

            return None

        except Exception:
            return None

    @classmethod
    def get_by_username(cls, username, db_manager=None):
        db_manager = db_manager or DBManager()

        try:
            db_manager.connect()

            query = """
                SELECT id, username, password, email, full_name, 
                       role, is_active, last_login, created_at
                FROM users
                WHERE username = ?
            """
            cursor = db_manager.conn.execute(query, (username,))
            row = cursor.fetchone()

            if row:
                return cls(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3],
                    full_name=row[4],
                    role=row[5],
                    is_active=bool(row[6]),
                    last_login=row[7],
                    created_at=row[8],
                    db_manager=db_manager
                )

            return None

        except Exception:
            return None

    @classmethod
    def get_all(cls, db_manager=None):
        db_manager = db_manager or DBManager()

        try:
            db_manager.connect()

            query = """
                SELECT id, username, password, email, full_name, 
                       role, is_active, last_login, created_at
                FROM users
                ORDER BY username
            """
            cursor = db_manager.conn.execute(query)

            users = []
            for row in cursor.fetchall():
                user = cls(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3],
                    full_name=row[4],
                    role=row[5],
                    is_active=bool(row[6]),
                    last_login=row[7],
                    created_at=row[8],
                    db_manager=db_manager
                )
                users.append(user)

            return users

        except Exception:
            return []
