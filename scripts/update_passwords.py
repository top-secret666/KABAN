import sqlite3
import hashlib
import os
import sys

# Добавьте путь к корневой директории проекта
sys.path.append('.')

from models.user import User
from models.db_manager import DBManager

def update_passwords():
    """
    Обновляет все пароли в базе данных в единый формат
    """
    db_manager = DBManager()
    db_manager.connect()

    # Получаем всех пользователей
    users = User.get_all(db_manager)

    for user in users:
        # Для тестовых пользователей с известными паролями
        if user.username == "admin":
            # Устанавливаем пароль "admin"
            new_password = "admin"
        elif user.username == "1":
            # Устанавливаем пароль "1"
            new_password = "1"
        else:
            # Для остальных пользователей устанавливаем временный пароль
            new_password = "password123"
            print(f"Установлен временный пароль 'password123' для пользователя {user.username}")

        # Обновляем пароль
        user.password = new_password
        success, error = user.save()

        if success:
            print(f"Пароль для пользователя {user.username} успешно обновлен")
        else:
            print(f"Ошибка при обновлении пароля для пользователя {user.username}: {error}")

    print("Обновление паролей завершено")

if __name__ == "__main__":
    update_passwords()