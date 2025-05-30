PRAGMA foreign_keys = ON;

-- =============================================
-- Создание таблицы пользователей
-- =============================================
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

-- =============================================
-- Создание таблицы сессий
-- =============================================
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- =============================================
-- Создание основных таблиц
-- =============================================
CREATE TABLE IF NOT EXISTS developers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    position TEXT NOT NULL CHECK (position IN ('backend', 'frontend', 'QA')),
    hourly_rate REAL NOT NULL CHECK (hourly_rate > 0),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client TEXT NOT NULL,
    deadline DATE NOT NULL,
    budget REAL NOT NULL CHECK (budget >= 0),
    status TEXT DEFAULT 'в работе',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    developer_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('новая', 'в работе', 'на проверке', 'завершено')),
    hours_worked REAL NOT NULL DEFAULT 0 CHECK (hours_worked >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (developer_id) REFERENCES developers (id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
);
-- =============================================
-- Создание таблицы уведомлений
-- =============================================
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('info', 'warning', 'error')),
    related_id INTEGER,
    related_type TEXT,
    is_read INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- =============================================
-- Создание индексов для ускорения запросов
-- =============================================
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users (role);

CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions (session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions (user_id);

CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks (project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_developer_id ON tasks (developer_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);
CREATE INDEX IF NOT EXISTS idx_tasks_created_by ON tasks (created_by);

CREATE INDEX IF NOT EXISTS idx_projects_deadline ON projects (deadline);
CREATE INDEX IF NOT EXISTS idx_projects_client ON projects (client);
CREATE INDEX IF NOT EXISTS idx_projects_created_by ON projects (created_by);

CREATE INDEX IF NOT EXISTS idx_developers_position ON developers (position);
CREATE INDEX IF NOT EXISTS idx_developers_user_id ON developers (user_id);

CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications (is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications (created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_related ON notifications (related_id, related_type);
-- =============================================
-- Создание представлений (Views) для удобства работы
-- =============================================
DROP VIEW IF EXISTS view_task_details;
CREATE VIEW view_task_details AS
SELECT
    t.id,
    t.description,
    t.status,
    t.hours_worked,
    t.created_at,
    t.updated_at,
    p.id AS project_id,
    p.name AS project_name,
    p.deadline AS project_deadline,
    d.id AS developer_id,
    d.full_name AS developer_name,
    d.position AS developer_position,
    d.hourly_rate,
    u.username AS created_by_username
FROM tasks t
JOIN projects p ON t.project_id = p.id
JOIN developers d ON t.developer_id = d.id
LEFT JOIN users u ON t.created_by = u.id;

DROP VIEW IF EXISTS view_project_stats;
CREATE VIEW view_project_stats AS
SELECT
    p.id,
    p.name,
    p.client,
    p.deadline,
    p.budget,
    p.status,
    p.created_at,
    COUNT(t.id) AS total_tasks,
    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) AS completed_tasks,
    ROUND(SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) * 100.0 / CASE WHEN COUNT(t.id) = 0 THEN 1 ELSE COUNT(t.id) END, 2) AS completion_percentage,
    SUM(t.hours_worked) AS total_hours,
    SUM(t.hours_worked * d.hourly_rate) AS labor_cost,
    u.username AS created_by_username
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
LEFT JOIN developers d ON t.developer_id = d.id
LEFT JOIN users u ON p.created_by = u.id
GROUP BY p.id;

DROP VIEW IF EXISTS view_developer_stats;
CREATE VIEW view_developer_stats AS
SELECT
    d.id,
    d.full_name,
    d.position,
    d.hourly_rate,
    u.username AS user_username,
    COUNT(t.id) AS total_tasks,
    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) AS completed_tasks,
    SUM(CASE WHEN t.hours_worked IS NULL THEN 0 ELSE t.hours_worked END) AS total_hours,
    SUM(CASE WHEN t.hours_worked IS NULL THEN 0 ELSE t.hours_worked END * d.hourly_rate) AS total_earnings
FROM developers d
LEFT JOIN tasks t ON d.id = t.developer_id
LEFT JOIN users u ON d.user_id = u.id
GROUP BY d.id;

-- =============================================
-- Создание триггеров для автоматизации
-- =============================================
DROP TRIGGER IF EXISTS check_project_budget;
CREATE TRIGGER check_project_budget
BEFORE INSERT ON tasks
BEGIN
    SELECT CASE
        WHEN (
            SELECT COALESCE(SUM(t.hours_worked * d.hourly_rate), 0) + NEW.hours_worked * (SELECT hourly_rate FROM developers WHERE id = NEW.developer_id)
            FROM tasks t
            JOIN developers d ON t.developer_id = d.id
            WHERE t.project_id = NEW.project_id
        ) > (SELECT budget FROM projects WHERE id = NEW.project_id)
        THEN RAISE(ABORT, 'Превышение бюджета проекта')
    END;
END;

DROP TRIGGER IF EXISTS update_project_status;
CREATE TRIGGER update_project_status
AFTER UPDATE ON tasks
WHEN NEW.status = 'завершено' AND OLD.status != 'завершено'
BEGIN
    UPDATE projects
    SET status = CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM tasks
            WHERE project_id = NEW.project_id AND status != 'завершено'
        ) THEN 'завершено'
        ELSE 'в работе'
    END
    WHERE id = NEW.project_id;
END;

DROP TRIGGER IF EXISTS update_task_timestamp;
CREATE TRIGGER update_task_timestamp
AFTER UPDATE ON tasks
BEGIN
    UPDATE tasks
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- =============================================
-- Триггеры для предотвращения дублирования записей
-- =============================================
DROP TRIGGER IF EXISTS upsert_developer;
CREATE TRIGGER upsert_developer
BEFORE INSERT ON developers
WHEN EXISTS (SELECT 1 FROM developers WHERE full_name = NEW.full_name)
BEGIN
    UPDATE developers
    SET position = NEW.position,
        hourly_rate = NEW.hourly_rate,
        user_id = COALESCE(NEW.user_id, user_id)
    WHERE full_name = NEW.full_name;

    SELECT raise(IGNORE);
END;

DROP TRIGGER IF EXISTS upsert_project;
CREATE TRIGGER upsert_project
BEFORE INSERT ON projects
WHEN EXISTS (SELECT 1 FROM projects WHERE name = NEW.name AND client = NEW.client)
BEGIN
    UPDATE projects
    SET deadline = NEW.deadline,
        budget = NEW.budget,
        status = COALESCE(NEW.status, 'в работе'),
        created_by = COALESCE(NEW.created_by, created_by)
    WHERE name = NEW.name AND client = NEW.client;

    SELECT raise(IGNORE);
END;

DROP TRIGGER IF EXISTS upsert_task;
CREATE TRIGGER upsert_task
BEFORE INSERT ON tasks
WHEN EXISTS (
    SELECT 1 FROM tasks
    WHERE project_id = NEW.project_id
    AND developer_id = NEW.developer_id
    AND description = NEW.description
)
BEGIN
    UPDATE tasks
    SET status = NEW.status,
        hours_worked = NEW.hours_worked,
        created_by = COALESCE(NEW.created_by, created_by)
    WHERE project_id = NEW.project_id
    AND developer_id = NEW.developer_id
    AND description = NEW.description;

    SELECT raise(IGNORE);
END;

-- =============================================
-- Добавление тестовых данных
-- =============================================
-- Добавление администратора по умолчанию (пароль: admin)
INSERT OR IGNORE INTO users (username, password, email, full_name, role, is_active)
VALUES ('admin', '$f47ac10b-58cc-4372-a567-0e02b2c3d479$8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin@example.com', 'Администратор', 'admin', 1);

-- Добавление тестовых пользователей
INSERT OR IGNORE INTO users (username, password, email, full_name, role, is_active)
VALUES
('manager', '$f47ac10b-58cc-4372-a567-0e02b2c3d479$5f4dcc3b5aa765d61d8327deb882cf99', 'manager@example.com', 'Менеджер Проектов', 'manager', 1),
('developer1', '$f47ac10b-58cc-4372-a567-0e02b2c3d479$5f4dcc3b5aa765d61d8327deb882cf99', 'dev1@example.com', 'Иванов Иван Иванович', 'developer', 1),
('developer2', '$f47ac10b-58cc-4372-a567-0e02b2c3d479$5f4dcc3b5aa765d61d8327deb882cf99', 'dev2@example.com', 'Петров Петр Петрович', 'developer', 1);

-- Добавление разработчиков
INSERT OR IGNORE INTO developers (full_name, position, hourly_rate, user_id)
VALUES
('Иванов Иван Иванович', 'backend', 1500, (SELECT id FROM users WHERE username = 'developer1')),
('Петров Петр Петрович', 'frontend', 1300, (SELECT id FROM users WHERE username = 'developer2')),
('Сидорова Анна Сергеевна', 'QA', 1200, NULL),
('Козлов Алексей Михайлович', 'backend', 1600, NULL),
('Новикова Елена Владимировна', 'frontend', 1400, NULL);

-- Добавление проектов
INSERT OR IGNORE INTO projects (name, client, deadline, budget, created_by)
VALUES
('Интернет-магазин', 'ООО "Торговый Дом"', '2023-12-31', 500000, (SELECT id FROM users WHERE username = 'manager')),
('Корпоративный портал', 'АО "Корпорация"', '2023-11-30', 350000, (SELECT id FROM users WHERE username = 'manager')),
('Мобильное приложение', 'ИП Смирнов', '2024-02-15', 600000, (SELECT id FROM users WHERE username = 'manager')),
('CRM-система', 'ООО "Бизнес Решения"', '2023-10-15', 450000, (SELECT id FROM users WHERE username = 'manager'));

-- Добавление задач
INSERT OR IGNORE INTO tasks (project_id, developer_id, description, status, hours_worked, created_by)
VALUES
(1, 1, 'Разработка API для товаров', 'в работе', 10, (SELECT id FROM users WHERE username = 'manager')),
(1, 2, 'Верстка главной страницы', 'завершено', 15, (SELECT id FROM users WHERE username = 'manager')),
(1, 3, 'Тестирование функционала корзины', 'в работе', 8, (SELECT id FROM users WHERE username = 'manager')),
(1, 4, 'Разработка системы оплаты', 'в работе', 12, (SELECT id FROM users WHERE username = 'manager')),
(1, 5, 'Верстка страницы товара', 'в работе', 6, (SELECT id FROM users WHERE username = 'manager')),

(2, 1, 'Настройка базы данных сотрудников', 'в работе', 5, (SELECT id FROM users WHERE username = 'manager')),
(2, 2, 'Разработка дизайна личного кабинета', 'в работе', 12, (SELECT id FROM users WHERE username = 'manager')),
(2, 3, 'Тестирование авторизации', 'завершено', 4, (SELECT id FROM users WHERE username = 'manager')),
(2, 4, 'Разработка API для документооборота', 'в работе', 8, (SELECT id FROM users WHERE username = 'manager')),

(3, 1, 'Разработка серверной части', 'в работе', 20, (SELECT id FROM users WHERE username = 'manager')),
(3, 2, 'Верстка интерфейса приложения', 'в работе', 18, (SELECT id FROM users WHERE username = 'manager')),
(3, 3, 'Тестирование на разных устройствах', 'в работе', 10, (SELECT id FROM users WHERE username = 'manager')),
(3, 5, 'Разработка анимаций', 'в работе', 8, (SELECT id FROM users WHERE username = 'manager')),

(4, 1, 'Проектирование базы данных', 'завершено', 15, (SELECT id FROM users WHERE username = 'manager')),
(4, 2, 'Разработка интерфейса администратора', 'в работе', 10, (SELECT id FROM users WHERE username = 'manager')),
(4, 3, 'Тестирование импорта данных', 'в работе', 6, (SELECT id FROM users WHERE username = 'manager')),
(4, 4, 'Разработка API для интеграций', 'в работе', 14, (SELECT id FROM users WHERE username = 'manager')),
(4, 5, 'Верстка дашборда', 'завершено', 12, (SELECT id FROM users WHERE username = 'manager'));
