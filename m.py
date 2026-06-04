from app import app
from data import db
from sqlalchemy import text


def migrate():
    with app.app_context():
        print("Миграция базы данных...")
        # Предыдущие миграции
        try:
            db.session.execute(text('ALTER TABLE comment ADD COLUMN parent_id INTEGER;'))
            print("✅ parent_id добавлен")
        except:
            pass
        try:
            db.session.execute(text('ALTER TABLE comment ADD COLUMN date VARCHAR(50);'))
            print("✅ date добавлен")
        except:
            pass

        # Новые колонки
        try:
            db.session.execute(text('ALTER TABLE idea ADD COLUMN team_id INTEGER;'))
            db.session.execute(text('ALTER TABLE idea ADD FOREIGN KEY(team_id) REFERENCES team(id);'))
            print("✅ team_id в idea добавлен")
        except Exception as e:
            print("⚠️ team_id в idea уже есть или ошибка:", e)
        try:
            db.session.execute(text('ALTER TABLE diary_entry ADD COLUMN team_id INTEGER;'))
            db.session.execute(text('ALTER TABLE diary_entry ADD FOREIGN KEY(team_id) REFERENCES team(id);'))
            print("✅ team_id в diary_entry добавлен")
        except Exception as e:
            print("⚠️ team_id в diary_entry уже есть или ошибка:", e)

        db.session.commit()
        print("Миграция завершена.")


if __name__ == '__main__':
    migrate()