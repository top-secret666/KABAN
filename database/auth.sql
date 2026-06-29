-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'manager', 'developer')),
    is_active INTEGER NOT NULL DEFAULT 1,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для ускорения запросов
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users (role);

-- Создание таблицы сессий
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions (session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions (user_id);

-- Добавление администратора по умолчанию (пароль: admin)
INSERT OR IGNORE INTO users (username, password, email, full_name, role, is_active)
VALUES ('admin', '$kaban_admin_v1$5339711063c99e0091dd0d254336e5373e1c2bdd0235f814696d45eeebab7e86', 'admin@example.com', 'Администратор', 'admin', 1);
