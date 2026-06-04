# migrate_db.py
# Запустите этот файл для добавления колонок parent_id и date в таблицу comment

from app import app
from data import db
from sqlalchemy import text


def migrate():
    with app.app_context():
        print("Начинаю миграцию базы данных...")

        # Добавляем колонку parent_id, если её нет
        try:
            db.session.execute(text('ALTER TABLE comment ADD COLUMN parent_id INTEGER;'))
            print("✅ Колонка parent_id добавлена")
        except Exception as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("ℹ️ Колонка parent_id уже существует")
            else:
                print(f"⚠️ Ошибка при добавлении parent_id: {e}")

        # Добавляем колонку date, если её нет
        try:
            db.session.execute(text('ALTER TABLE comment ADD COLUMN date VARCHAR(50);'))
            print("✅ Колонка date добавлена")
        except Exception as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("ℹ️ Колонка date уже существует")
            else:
                print(f"⚠️ Ошибка при добавлении date: {e}")

        # Заполняем старые записи датой (опционально)
        from datetime import datetime
        now = datetime.now().strftime('%d %b %Y, %H:%M')
        result = db.session.execute(text("SELECT id FROM comment WHERE date IS NULL;"))
        rows = result.fetchall()
        if rows:
            db.session.execute(text(f"UPDATE comment SET date = '{now}' WHERE date IS NULL;"))
            print(f"✅ Обновлено {len(rows)} старых комментариев (установлена текущая дата)")

        db.session.commit()
        print("Миграция завершена успешно!")


if __name__ == '__main__':
    migrate()