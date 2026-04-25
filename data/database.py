import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_database(app):
    # Определяем путь к папке db/ в корне проекта
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_folder = os.path.join(base_dir, '..', 'db')
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, 'fundofideas.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)