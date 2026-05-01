from app import app
from data import db
from sqlalchemy import text

with app.app_context():
    try:
        # Добавляем новые колонки вручную
        db.session.execute(text('ALTER TABLE user ADD COLUMN notifications_enabled BOOLEAN DEFAULT 1'))
        db.session.execute(text('ALTER TABLE user ADD COLUMN email_notifications BOOLEAN DEFAULT 1'))
        db.session.execute(text('ALTER TABLE user ADD COLUMN theme_preference VARCHAR(20) DEFAULT \'light\''))
        db.session.execute(text('ALTER TABLE user ADD COLUMN language VARCHAR(5) DEFAULT \'ru\''))
        db.session.execute(text('ALTER TABLE user ADD COLUMN privacy_level VARCHAR(20) DEFAULT \'public\''))

        # Сохраняем изменения
        db.session.commit()
        print("Миграция завершена успешно!")
    except Exception as e:
        print(f"Ошибка миграции: {e}")
        db.session.rollback()