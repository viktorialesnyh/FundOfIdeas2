from app import app
from data import db
from sqlalchemy import text

with app.app_context():
    columns_to_add = [
        ("password_hash", "VARCHAR(256)"),
        ("is_email_visible", "BOOLEAN DEFAULT 1"),
        ("is_city_visible", "BOOLEAN DEFAULT 1"),
        ("is_photo_visible", "BOOLEAN DEFAULT 1"),
        ("is_skills_visible", "BOOLEAN DEFAULT 1"),
        ("is_description_visible", "BOOLEAN DEFAULT 1"),
        ("is_ideas_visible", "BOOLEAN DEFAULT 1"),
        ("is_team_visible", "BOOLEAN DEFAULT 1")
    ]

    for col_name, col_type in columns_to_add:
        try:
            db.session.execute(text(f'ALTER TABLE user ADD COLUMN {col_name} {col_type}'))
            print(f"Добавлено поле: {col_name}")
        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate column name" in error_msg:
                print(f"ℹПоле '{col_name}' уже существует (пропущено)")
            else:
                print(f"️ Ошибка при добавлении '{col_name}': {e}")

    db.session.commit()
    print("Миграция завершена успешно")