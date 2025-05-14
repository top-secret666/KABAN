PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS developers;

-- =============================================
-- Создание основных таблиц
-- =============================================
CREATE TABLE developers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    position TEXT NOT NULL CHECK (position IN ('backend', 'frontend', 'QA')),
    hourly_rate REAL NOT NULL CHECK (hourly_rate > 0)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client TEXT NOT NULL,
    deadline DATE NOT NULL,
    budget REAL NOT NULL CHECK (budget >= 0),
    status TEXT DEFAULT 'в работе'
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    developer_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('в работе', 'завершено')),
    hours_worked REAL NOT NULL DEFAULT 0 CHECK (hours_worked >= 0),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (developer_id) REFERENCES developers (id) ON DELETE CASCADE
);

-- =============================================
-- Создание индексов для ускорения запросов
-- =============================================
DROP INDEX IF EXISTS idx_tasks_project_id;
DROP INDEX IF EXISTS idx_tasks_developer_id;
DROP INDEX IF EXISTS idx_tasks_status;
CREATE INDEX idx_tasks_project_id ON tasks (project_id);
CREATE INDEX idx_tasks_developer_id ON tasks (developer_id);
CREATE INDEX idx_tasks_status ON tasks (status);

DROP INDEX IF EXISTS idx_projects_deadline;
DROP INDEX IF EXISTS idx_projects_client;
CREATE INDEX idx_projects_deadline ON projects (deadline);
CREATE INDEX idx_projects_client ON projects (client);

DROP INDEX IF EXISTS idx_developers_position;
CREATE INDEX idx_developers_position ON developers (position);

-- =============================================
-- Добавление тестовых данных
-- =============================================
INSERT INTO developers (full_name, position, hourly_rate) VALUES
('Иванов Иван Иванович', 'backend', 1500),
('Петров Петр Петрович', 'frontend', 1300),
('Сидорова Анна Сергеевна', 'QA', 1200),
('Козлов Алексей Михайлович', 'backend', 1600),
('Новикова Елена Владимировна', 'frontend', 1400);

INSERT INTO projects (name, client, deadline, budget) VALUES
('Интернет-магазин', 'ООО "Торговый Дом"', '2023-12-31', 500000),
('Корпоративный портал', 'АО "Корпорация"', '2023-11-30', 350000),
('Мобильное приложение', 'ИП Смирнов', '2024-02-15', 600000),
('CRM-система', 'ООО "Бизнес Решения"', '2023-10-15', 450000);

INSERT INTO tasks (project_id, developer_id, description, status, hours_worked) VALUES
(1, 1, 'Разработка API для товаров', 'в работе', 10),
(1, 2, 'Верстка главной страницы', 'завершено', 15),
(1, 3, 'Тестирование функционала корзины', 'в работе', 8),
(1, 4, 'Разработка системы оплаты', 'в работе', 12),
(1, 5, 'Верстка страницы товара', 'в работе', 6),

(2, 1, 'Настройка базы данных сотрудников', 'в работе', 5),
(2, 2, 'Разработка дизайна личного кабинета', 'в работе', 12),
(2, 3, 'Тестирование авторизации', 'завершено', 4),
(2, 4, 'Разработка API для документооборота', 'в работе', 8),

(3, 1, 'Разработка серверной части', 'в работе', 20),
(3, 2, 'Верстка интерфейса приложения', 'в работе', 18),
(3, 3, 'Тестирование на разных устройствах', 'в работе', 10),
(3, 5, 'Разработка анимаций', 'в работе', 8),

(4, 1, 'Проектирование базы данных', 'завершено', 15),
(4, 2, 'Разработка интерфейса администратора', 'в работе', 10),
(4, 3, 'Тестирование импорта данных', 'в работе', 6),
(4, 4, 'Разработка API для интеграций', 'в работе', 14),
(4, 5, 'Верстка дашборда', 'завершено', 12);

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
    p.id AS project_id,
    p.name AS project_name,
    p.deadline AS project_deadline,
    d.id AS developer_id,
    d.full_name AS developer_name,
    d.position AS developer_position,
    d.hourly_rate
FROM tasks t
JOIN projects p ON t.project_id = p.id
JOIN developers d ON t.developer_id = d.id;

DROP VIEW IF EXISTS view_project_stats;
CREATE VIEW view_project_stats AS
SELECT
    p.id,
    p.name,
    p.client,
    p.deadline,
    p.budget,
    COUNT(t.id) AS total_tasks,
    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) AS completed_tasks,
    ROUND(SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) * 100.0 / CASE WHEN COUNT(t.id) = 0 THEN 1 ELSE COUNT(t.id) END, 2) AS completion_percentage,
    SUM(t.hours_worked) AS total_hours,
    SUM(t.hours_worked * d.hourly_rate) AS labor_cost
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
LEFT JOIN developers d ON t.developer_id = d.id
GROUP BY p.id;

DROP VIEW IF EXISTS view_developer_stats;
CREATE VIEW view_developer_stats AS
SELECT
    d.id,
    d.full_name,
    d.position,
    d.hourly_rate,
    COUNT(t.id) AS total_tasks,
    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) AS completed_tasks,
    SUM(CASE WHEN t.hours_worked IS NULL THEN 0 ELSE t.hours_worked END) AS total_hours,
    SUM(CASE WHEN t.hours_worked IS NULL THEN 0 ELSE t.hours_worked END * d.hourly_rate) AS total_earnings
FROM developers d
LEFT JOIN tasks t ON d.id = t.developer_id
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
WHEN NEW.status = 'завершено' AND OLD.status = 'в работе'
BEGIN
    UPDATE projects
    SET status = CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM tasks
            WHERE project_id = NEW.project_id AND status = 'в работе'
        ) THEN 'завершено'
        ELSE 'в работе'
    END
    WHERE id = NEW.project_id;
END;

-- =============================================
-- Создание индексов для оптимизации представлений
-- =============================================
DROP INDEX IF EXISTS idx_tasks_project_developer;
DROP INDEX IF EXISTS idx_tasks_status_hours;
CREATE INDEX idx_tasks_project_developer ON tasks (project_id, developer_id);
CREATE INDEX idx_tasks_status_hours ON tasks (status, hours_worked);

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
        hourly_rate = NEW.hourly_rate
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
        status = COALESCE(NEW.status, 'в работе')
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
        hours_worked = NEW.hours_worked
    WHERE project_id = NEW.project_id
    AND developer_id = NEW.developer_id
    AND description = NEW.description;

    SELECT raise(IGNORE);
END;