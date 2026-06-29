"""Пути проекта — не зависят от текущей рабочей директории."""
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(*parts):
    return os.path.join(ROOT_DIR, *parts)


DB_PATH = resource_path('database', 'kaban.db')
SQL_PATH = resource_path('database', 'kaban.sql')
