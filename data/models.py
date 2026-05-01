from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, default="Основатель стартапа в области EdTech...")
    about_me = db.Column(db.Text, default="")
    city = db.Column(db.String(100), default="Москва, Россия")
    joined_year = db.Column(db.String(10), default="2026")

    # Настройки пользователя
    notifications_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    theme_preference = db.Column(db.String(20), default='light')
    language = db.Column(db.String(5), default='ru')
    privacy_level = db.Column(db.String(20), default='public')

    ideas = db.relationship('Idea', backref='author', lazy=True)
    diary_entries = db.relationship('DiaryEntry', backref='owner', lazy=True)
    skills = db.relationship('Skill', backref='owner_skill', lazy=True)


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    visibility = db.Column(db.String(20), default='draft')
    license = db.Column(db.String(20), default='all_rights')
    tags = db.Column(db.String(200))
    date = db.Column(db.String(50))


class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(50))
    date = db.Column(db.String(50))


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(10), default='🛠')
    level = db.Column(db.Integer, default=50)
    level_text = db.Column(db.String(20))


class TeamProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.String(200))
    description = db.Column(db.Text)
    looking_for = db.Column(db.String(20), default='team')
    status = db.Column(db.String(20), default='active')
    date = db.Column(db.String(50))
    owner = db.relationship('User', backref='team_profiles', lazy=True)