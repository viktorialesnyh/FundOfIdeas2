from .database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    bio = db.Column(db.Text, default="")
    about_me = db.Column(db.Text, default="")
    city = db.Column(db.String(100), default="Москва, Россия")
    joined_year = db.Column(db.String(10), default="2026")

    # Настройки конфиденциальности (True = видно всем, False = скрыто)
    is_email_visible = db.Column(db.Boolean, default=True)
    is_city_visible = db.Column(db.Boolean, default=True)
    is_photo_visible = db.Column(db.Boolean, default=True)
    is_skills_visible = db.Column(db.Boolean, default=True)
    is_description_visible = db.Column(db.Boolean, default=True)
    is_ideas_visible = db.Column(db.Boolean, default=True)
    is_team_visible = db.Column(db.Boolean, default=True)

    ideas = db.relationship('Idea', backref='author', lazy=True)
    diary_entries = db.relationship('DiaryEntry', backref='owner', lazy=True)
    skills = db.relationship('Skill', backref='owner_skill', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), nullable=False)
    user = db.relationship('User', backref='likes', lazy=True)
    idea = db.relationship('Idea', backref='likes', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref='comments', lazy=True)
    idea = db.relationship('Idea', backref='comments', lazy=True)

# === МОДЕЛИ КОМАНД ===

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, recruiting, closed
    date = db.Column(db.String(50))
    # Связи
    leader = db.relationship('User', backref='led_teams', lazy=True)
    members = db.relationship('TeamMember', backref='team', lazy=True)


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50))
    joined_date = db.Column(db.String(50))
    # Связи
    user = db.relationship('User', backref='team_memberships', lazy=True)