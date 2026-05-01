from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime
from data import db, setup_database, User, Idea, DiaryEntry, Skill, TeamProfile
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

setup_database(app)

with app.app_context():
    db.create_all()


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# === МАРШРУТЫ АВТОРИЗАЦИИ ===
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password_hash:
            if check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash('Неверный пароль', 'error')
                return redirect(url_for('index'))
        else:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

    flash('Пользователь не найден', 'error')
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', 'User')
    email = request.form.get('email', 'user@test.com')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash('Email уже занят', 'error')
        return redirect(url_for('index'))

    new_user = User(username=username, email=email)
    if password:
        new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    return redirect(url_for('dashboard'))


# === ОСНОВНЫЕ МАРШРУТЫ ===
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=user.username)


@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)


@app.route('/ideas')
def ideas():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    return render_template('ideas.html', username=user.username, user=user)


@app.route('/diary', methods=['GET', 'POST'])
def diary():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    if request.method == 'POST':
        text = request.form.get('entry_text')
        tag = request.form.get('tag', 'success')
        if text:
            db.session.add(DiaryEntry(
                user_id=user.id,
                text=text,
                tag=tag,
                date=datetime.datetime.now().strftime('%d %b, %H:%M')
            ))
            db.session.commit()
        return redirect(url_for('diary'))
    entries = DiaryEntry.query.filter_by(user_id=user.id).order_by(DiaryEntry.id.desc()).all()
    return render_template('diary.html', username=user.username, entries=entries)


@app.route('/team')
def team():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    profiles = TeamProfile.query.filter(TeamProfile.user_id != user.id).all()
    my_profile = TeamProfile.query.filter_by(user_id=user.id).first()
    return render_template('team.html',
                           username=user.username,
                           profiles=profiles,
                           my_profile=my_profile)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# === ОБНОВЛЕНИЕ ПРОФИЛЯ ===
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    user.about_me = request.form.get('about_text')
    user.bio = request.form.get('bio_text')
    user.city = request.form.get('city')
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/add_skill', methods=['POST'])
def add_skill():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    name = request.form.get('skill_name')
    icon = request.form.get('skill_icon', '🛠')
    level = int(request.form.get('skill_level', 50))
    text = 'Начальный' if level < 50 else 'Средний' if level < 75 else 'Продвинутый' if level < 100 else 'Эксперт'
    db.session.add(Skill(user_id=user.id, name=name, icon=icon, level=level, level_text=text))
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    skill = Skill.query.get(skill_id)
    if skill and skill.user_id == user.id:
        db.session.delete(skill)
        db.session.commit()
    return redirect(url_for('profile'))


# === МАРШРУТЫ НАСТРОЕК ===

# Смена пароля
@app.route('/settings/change_password', methods=['POST'])
def change_password():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))

    current_pass = request.form.get('current_password')
    new_pass = request.form.get('new_password')

    if user.password_hash:
        if not check_password_hash(user.password_hash, current_pass):
            return redirect(url_for('profile', error='Неверный текущий пароль'))

    if new_pass:
        user.set_password(new_pass)
        db.session.commit()
        return redirect(url_for('profile', success='Пароль успешно изменен'))

    return redirect(url_for('profile'))


# Обновление приватности
@app.route('/settings/privacy', methods=['POST'])
def update_privacy():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))

    privacy_fields = [
        'is_email_visible', 'is_city_visible', 'is_photo_visible',
        'is_skills_visible', 'is_description_visible',
        'is_ideas_visible', 'is_team_visible'
    ]

    for field in privacy_fields:
        setattr(user, field, request.form.get(field) == 'on')

    db.session.commit()
    return redirect(url_for('profile', success='Настройки конфиденциальности сохранены'))


# Удаление аккаунта
@app.route('/settings/delete_account', methods=['POST'])
def delete_account():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))

    confirm_pass = request.form.get('confirm_password')

    if not user.check_password(confirm_pass):
        return redirect(url_for('profile', error='Неверный пароль. Аккаунт не удален.'))

    DiaryEntry.query.filter_by(user_id=user.id).delete()
    Skill.query.filter_by(user_id=user.id).delete()
    TeamProfile.query.filter_by(user_id=user.id).delete()
    Idea.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    session.pop('user_id', None)
    return redirect(url_for('index'))


# === МАРШРУТЫ ИДЕЙ ===
@app.route('/create_idea', methods=['POST'])
def create_idea():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    new_idea = Idea(
        user_id=user.id,
        title=request.form.get('title'),
        description=request.form.get('description'),
        category=request.form.get('category', 'other'),
        visibility=request.form.get('visibility', 'draft'),
        license=request.form.get('license', 'all_rights'),
        tags=request.form.get('tags', ''),
        date=datetime.datetime.now().strftime('%d %b %Y')
    )
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('ideas'))


@app.route('/update_idea/<int:idea_id>', methods=['POST'])
def update_idea(idea_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    idea = Idea.query.get_or_404(idea_id)
    if idea.user_id != user.id:
        return redirect(url_for('ideas'))

    idea.title = request.form.get('title')
    idea.description = request.form.get('description')
    idea.category = request.form.get('category', 'other')
    idea.visibility = request.form.get('visibility', 'draft')
    idea.license = request.form.get('license', 'all_rights')
    idea.tags = request.form.get('tags', '')
    db.session.commit()
    return redirect(url_for('ideas'))


# === МАРШРУТЫ КОМАНДЫ ===
@app.route('/create_team_profile', methods=['POST'])
def create_team_profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    profile = TeamProfile.query.filter_by(user_id=user.id).first()
    data = {
        'role': request.form.get('role'),
        'skills': request.form.get('skills', ''),
        'description': request.form.get('description'),
        'looking_for': request.form.get('looking_for', 'team'),
        'date': datetime.datetime.now().strftime('%d %b %Y')
    }
    if profile:
        for key, value in data.items():
            setattr(profile, key, value)
    else:
        new_profile = TeamProfile(user_id=user.id, **data)
        db.session.add(new_profile)
    db.session.commit()
    return redirect(url_for('team'))


@app.route('/delete_team_profile')
def delete_team_profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('index'))
    profile = TeamProfile.query.filter_by(user_id=user.id).first()
    if profile:
        db.session.delete(profile)
        db.session.commit()
    return redirect(url_for('team'))


if __name__ == '__main__':
    app.run(debug=True)