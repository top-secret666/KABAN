from db_manager import DBManager


class Developer:
    def __init__(self, id=None, full_name="", position="", hourly_rate=0):
        self.id = id
        self.full_name = full_name
        self.position = position
        self.hourly_rate = hourly_rate
        self.db_manager = DBManager()

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'position': self.position,
            'hourly_rate': self.hourly_rate
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            full_name=data.get('full_name', ""),
            position=data.get('position', ""),
            hourly_rate=data.get('hourly_rate', 0)
        )

    def validate(self):
        if not self.full_name:
            return False, "ФИО разработчика не может быть пустым"

        if self.position not in ['backend', 'frontend', 'QA']:
            return False, "Должность должна быть одной из: backend, frontend, QA"

        if self.hourly_rate <= 0:
            return False, "Ставка в час должна быть положительным числом"

        return True, None

    def save(self):
        is_valid, error_message = self.validate()
        if not is_valid:
            return False, error_message

        try:
            if self.id is None:
                self.db_manager.execute(
                    "INSERT INTO developers (full_name, position, hourly_rate) VALUES (?, ?, ?)",
                    (self.full_name, self.position, self.hourly_rate)
                )
                self.id = self.db_manager.get_last_row_id()
            else:
                self.db_manager.execute(
                    "UPDATE developers SET full_name = ?, position = ?, hourly_rate = ? WHERE id = ?",
                    (self.full_name, self.position, self.hourly_rate, self.id)
                )

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def delete(self):
        if self.id is None:
            return False, "Невозможно удалить несохраненного разработчика"

        try:
            self.db_manager.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE developer_id = ?",
                (self.id,)
            )
            result = self.db_manager.fetch_one()

            if result['count'] > 0:
                return False, f"Невозможно удалить разработчика, так как с ним связано {result['count']} задач"

            self.db_manager.execute(
                "DELETE FROM developers WHERE id = ?",
                (self.id,)
            )

            self.db_manager.commit()
            self.id = None
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    @classmethod
    def get_by_id(cls, developer_id):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM developers WHERE id = ?",
                (developer_id,)
            )
            data = db_manager.fetch_one()

            if data:
                return cls.from_dict(data)
            return None

        except Exception as e:
            print(f"Ошибка при получении разработчика: {e}")
            return None

    @classmethod
    def get_all(cls):
        db_manager = DBManager()

        try:
            db_manager.execute("SELECT * FROM developers")
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении разработчиков: {e}")
            return []

    @classmethod
    def get_by_position(cls, position):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM developers WHERE position = ?",
                (position,)
            )
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении разработчиков: {e}")
            return []

    def get_tasks(self):

        if self.id is None:
            return []

        from task import Task

        return Task.get_by_developer(self.id)

    def calculate_salary(self):
        if self.id is None:
            return 0

        try:
            self.db_manager.execute(
                """
                SELECT SUM(hours_worked) as total_hours
                FROM tasks
                WHERE developer_id = ?
                """,
                (self.id,)
            )
            result = self.db_manager.fetch_one()

            total_hours = result['total_hours'] if result['total_hours'] else 0
            return total_hours * self.hourly_rate

        except Exception as e:
            print(f"Ошибка при расчете зарплаты: {e}")
            return 0

    def __str__(self):
        return f"Developer(id={self.id}, full_name='{self.full_name}', position='{self.position}', hourly_rate={self.hourly_rate})"