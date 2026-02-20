from .db_manager import DBManager


class Task:

    def __init__(self, id=None, project_id=None, developer_id=None, description="", status="новая", hours_worked=0,
                 created_at=None, updated_at=None):
        self.id = id
        self.project_id = project_id
        self.developer_id = developer_id
        self.description = description
        self.status = status
        self.hours_worked = hours_worked
        self.created_at = created_at
        self.updated_at = updated_at

        # Добавляем инициализацию db_manager
        from models.db_manager import DBManager
        self.db_manager = DBManager()

    def __str__(self):
        return f"Task(id={self.id}, description='{self.description}', status='{self.status}', hours_worked={self.hours_worked})"

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'developer_id': self.developer_id,
            'description': self.description,
            'status': self.status,
            'hours_worked': self.hours_worked
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            project_id=data.get('project_id'),
            developer_id=data.get('developer_id'),
            description=data.get('description', ""),
            status=data.get('status', "в работе"),
            hours_worked=data.get('hours_worked', 0)
        )

    def validate(self):
        if not self.project_id:
            return False, "ID проекта не может быть пустым"

        if not self.developer_id:
            return False, "ID разработчика не может быть пустым"

        if not self.description:
            return False, "Описание задачи не может быть пустым"

        if self.status not in ['в работе', 'завершено']:
            return False, "Статус должен быть одним из: в работе, завершено"

        if self.hours_worked < 0:
            return False, "Количество часов не может быть отрицательным"

        self.db_manager.execute(
            "SELECT id FROM projects WHERE id = ?",
            (self.project_id,)
        )
        if not self.db_manager.fetch_one():
            return False, f"Проект с ID {self.project_id} не существует"

        self.db_manager.execute(
            "SELECT id FROM developers WHERE id = ?",
            (self.developer_id,)
        )
        if not self.db_manager.fetch_one():
            return False, f"Разработчик с ID {self.developer_id} не существует"

        return True, None

    def save(self):
        is_valid, error_message = self.validate()
        if not is_valid:
            return False, error_message

        try:
            if self.id is None:
                self.db_manager.execute(
                    "INSERT INTO tasks (project_id, developer_id, description, status, hours_worked) VALUES (?, ?, ?, ?, ?)",
                    (self.project_id, self.developer_id, self.description, self.status, self.hours_worked)
                )
                self.id = self.db_manager.get_last_row_id()
            else:
                self.db_manager.execute(
                    "UPDATE tasks SET project_id = ?, developer_id = ?, description = ?, status = ?, hours_worked = ? WHERE id = ?",
                    (self.project_id, self.developer_id, self.description, self.status, self.hours_worked, self.id)
                )

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def delete(self):
        if self.id is None:
            return False, "Невозможно удалить несохраненную задачу"

        try:
            self.db_manager.execute(
                "DELETE FROM tasks WHERE id = ?",
                (self.id,)
            )

            self.db_manager.commit()
            self.id = None
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    @classmethod
    def get_by_id(cls, task_id):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,)
            )
            data = db_manager.fetch_one()

            if data:
                return cls.from_dict(data)
            return None

        except Exception as e:
            print(f"Ошибка при получении задачи: {e}")
            return None

    @classmethod
    def get_all(cls):
        db_manager = DBManager()

        try:
            db_manager.execute("SELECT * FROM tasks")
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении задач: {e}")
            return []

    @classmethod
    def get_by_project(cls, project_id):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM tasks WHERE project_id = ?",
                (project_id,)
            )
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении задач: {e}")
            return []

    @classmethod
    def get_by_developer(cls, developer_id):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM tasks WHERE developer_id = ?",
                (developer_id,)
            )
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении задач: {e}")
            return []

    @classmethod
    def get_by_status(cls, status):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM tasks WHERE status = ?",
                (status,)
            )
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении задач: {e}")
            return []

    def get_project(self):
        """
        Получает связанный проект
        """
        if not hasattr(self, '_project') or self._project is None:
            from models.project import Project
            self._project = Project.get_by_id(self.project_id) if self.project_id else None
        return self._project

    def get_developer(self):
        """
        Получает связанного разработчика
        """
        if not hasattr(self, '_developer') or self._developer is None:
            from models.developer import Developer
            self._developer = Developer.get_by_id(self.developer_id) if self.developer_id else None
        return self._developer

    def update_status(self, status):
        if status not in ['в работе', 'завершено']:
            return False, "Статус должен быть одним из: в работе, завершено"

        self.status = status
        return self.save()

    def update_hours(self, hours_worked):
        if hours_worked < 0:
            return False, "Количество часов не может быть отрицательным"

        self.hours_worked = hours_worked
        return self.save()

    def __str__(self):
        return f"Task(id={self.id}, project_id={self.project_id}, developer_id={self.developer_id}, description='{self.description}', status='{self.status}', hours_worked={self.hours_worked})"