from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import datetime
from data import db, setup_database, User, Idea, DiaryEntry, Skill, TeamProfile, Like, Comment, Team, TeamMember
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

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

    user_ideas = Idea.query.filter_by(user_id=user.id).all()
    user_categories = {i.category for i in user_ideas if i.category}
    user_tags = set()
    for i in user_ideas:
        if i.tags:
            user_tags.update(t.strip().lower() for t in i.tags.split(','))
    user_skills = {s.name.lower() for s in Skill.query.filter_by(user_id=user.id).all()}

    candidates = Idea.query.filter(Idea.visibility == 'published').all()
    scored_ideas = []
    now = datetime.datetime.now()

    for idea in candidates:
        score = 0
        if idea.category in user_categories:
            score += 30
        idea_tags = set(t.strip().lower() for t in idea.tags.split(',')) if idea.tags else set()
        score += len(idea_tags & user_tags) * 10
        score += len(idea_tags & user_skills) * 5
        likes_count = Like.query.filter_by(idea_id=idea.id).count()
        score += likes_count * 2
        try:
            idea_date = datetime.datetime.strptime(idea.date, '%d %b %Y')
            days_old = (now - idea_date).days
            if days_old < 30:
                score += (30 - days_old) * 1.5
        except ValueError:
            pass
        scored_ideas.append({'idea': idea, 'score': score})

    scored_ideas.sort(key=lambda x: (x['score'], x['idea'].id), reverse=True)
    recommended_ideas = [item['idea'] for item in scored_ideas[:15]]
    liked_ideas = {l.idea_id for l in Like.query.filter_by(user_id=user.id).all()}

    return render_template('dashboard.html', username=user.username, recommended_ideas=recommended_ideas,
                           liked_ideas=liked_ideas)


@app.route('/search_ideas', methods=['GET'])
def search_ideas():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    search_term = f'%{query}%'

    # Используем ilike для поиска БЕЗ УЧЕТА РЕГИСТРА (Case Insensitive)
    results = Idea.query.join(User, Idea.user_id == User.id).filter(
        Idea.visibility == 'published',
        or_(
            Idea.title.ilike(search_term),
            Idea.description.ilike(search_term),
            Idea.tags.ilike(search_term),
            User.username.ilike(search_term)
        )
    ).order_by(Idea.id.desc()).limit(20).all()

    data = []
    for idea in results:
        data.append({
            'id': idea.id,
            'title': idea.title,
            'description': idea.description,
            'date': idea.date,
            'tags': idea.tags,
            'author_username': idea.author.username if idea.author else 'Аноним',
            'visibility': idea.visibility,
            'category': idea.category,
            'license': idea.license
        })
    return jsonify(data)


@app.route('/profile')
def profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    return render_template('profile.html', user=user)


@app.route('/ideas')
def ideas():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    liked_ideas = {l.idea_id for l in Like.query.filter_by(user_id=user.id).all()}
    return render_template('ideas.html', username=user.username, user=user, liked_ideas=liked_ideas)


@app.route('/diary', methods=['GET', 'POST'])
def diary():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    if request.method == 'POST':
        text = request.form.get('entry_text')
        tag = request.form.get('tag', 'success')
        if text:
            db.session.add(
                DiaryEntry(user_id=user.id, text=text, tag=tag, date=datetime.datetime.now().strftime('%d %b, %H:%M')))
            db.session.commit()
            return redirect(url_for('diary'))
    entries = DiaryEntry.query.filter_by(user_id=user.id).order_by(DiaryEntry.id.desc()).all()
    return render_template('diary.html', username=user.username, entries=entries)


@app.route('/team')
def team():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    profiles = TeamProfile.query.filter(TeamProfile.user_id != user.id).all()
    teams = Team.query.filter(Team.status == 'recruiting').all()
    my_profile = TeamProfile.query.filter_by(user_id=user.id).first()
    return render_template('team.html', username=user.username, profiles=profiles, teams=teams, my_profile=my_profile)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# === ОБНОВЛЕНИЕ ПРОФИЛЯ ===
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.about_me = request.form.get('about_text')
    user.bio = request.form.get('bio_text')
    user.city = request.form.get('city')
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/add_skill', methods=['POST'])
def add_skill():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    name = request.form.get('skill_name')
    icon = request.form.get('skill_icon', '')
    level = int(request.form.get('skill_level', 50))
    text = 'Начальный' if level < 50 else 'Средний' if level < 75 else 'Продвинутый' if level < 100 else 'Эксперт'
    db.session.add(Skill(user_id=user.id, name=name, icon=icon, level=level, level_text=text))
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    skill = Skill.query.get(skill_id)
    if skill and skill.user_id == user.id:
        db.session.delete(skill)
        db.session.commit()
    return redirect(url_for('profile'))


# === НАСТРОЙКИ ===
@app.route('/settings/change_password', methods=['POST'])
def change_password():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    current_pass = request.form.get('current_password')
    new_pass = request.form.get('new_password')
    if user.password_hash and not check_password_hash(user.password_hash, current_pass):
        return redirect(url_for('profile', error='Неверный текущий пароль'))
    if new_pass:
        user.set_password(new_pass)
        db.session.commit()
        return redirect(url_for('profile', success='Пароль успешно изменен'))
    return redirect(url_for('profile'))


@app.route('/settings/privacy', methods=['POST'])
def update_privacy():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    fields = ['is_email_visible', 'is_city_visible', 'is_photo_visible', 'is_skills_visible', 'is_description_visible',
              'is_ideas_visible', 'is_team_visible']
    for f in fields:
        setattr(user, f, request.form.get(f) == 'on')
    db.session.commit()
    return redirect(url_for('profile', success='Настройки сохранены'))


@app.route('/settings/delete_account', methods=['POST'])
def delete_account():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    if not user.check_password(request.form.get('confirm_password')):
        return redirect(url_for('profile', error='Неверный пароль'))

    DiaryEntry.query.filter_by(user_id=user.id).delete()
    Skill.query.filter_by(user_id=user.id).delete()
    TeamProfile.query.filter_by(user_id=user.id).delete()
    Idea.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)
    return redirect(url_for('index'))


# === ИДЕИ ===
@app.route('/create_idea', methods=['POST'])
def create_idea():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    new_idea = Idea(
        user_id=user.id, title=request.form.get('title'), description=request.form.get('description'),
        category=request.form.get('category', 'other'), visibility=request.form.get('visibility', 'draft'),
        license=request.form.get('license', 'all_rights'), tags=request.form.get('tags', ''),
        date=datetime.datetime.now().strftime('%d %b %Y')
    )
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('ideas'))


@app.route('/update_idea/<int:idea_id>', methods=['POST'])
def update_idea(idea_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    idea = Idea.query.get_or_404(idea_id)
    if idea.user_id != user.id: return redirect(url_for('ideas'))
    idea.title = request.form.get('title')
    idea.description = request.form.get('description')
    idea.category = request.form.get('category', 'other')
    idea.visibility = request.form.get('visibility', 'draft')
    idea.license = request.form.get('license', 'all_rights')
    idea.tags = request.form.get('tags', '')
    db.session.commit()
    return redirect(url_for('ideas'))


# === КОМАНДА ===
@app.route('/create_team_profile', methods=['POST'])
def create_team_profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    profile = TeamProfile.query.filter_by(user_id=user.id).first()
    data = {
        'role': request.form.get('role'), 'skills': request.form.get('skills', ''),
        'description': request.form.get('description'), 'looking_for': request.form.get('looking_for', 'team'),
        'date': datetime.datetime.now().strftime('%d %b %Y')
    }
    if profile:
        for k, v in data.items(): setattr(profile, k, v)
    else:
        db.session.add(TeamProfile(user_id=user.id, **data))
    db.session.commit()
    return redirect(url_for('team'))


@app.route('/delete_team_profile')
def delete_team_profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    profile = TeamProfile.query.filter_by(user_id=user.id).first()
    if profile: db.session.delete(profile)
    db.session.commit()
    return redirect(url_for('team'))


# === ЛАЙКИ И КОММЕНТАРИИ ===
@app.route('/like_idea/<int:idea_id>', methods=['POST'])
def like_idea(idea_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))

    existing = Like.query.filter_by(user_id=user.id, idea_id=idea_id).first()
    if existing:
        db.session.delete(existing)
        is_liked = False
    else:
        db.session.add(Like(user_id=user.id, idea_id=idea_id))
        is_liked = True

    db.session.commit()
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_count = Like.query.filter_by(idea_id=idea_id).count()
        return jsonify({'likes': new_count, 'is_liked': is_liked})
    return redirect(url_for('ideas'))


@app.route('/get_comments/<int:idea_id>', methods=['GET'])
def get_comments(idea_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    comments = Comment.query.filter_by(idea_id=idea_id).order_by(Comment.id.desc()).all()
    comments_data = [{'id': c.id, 'text': c.text, 'author': c.user.username if c.user else 'Пользователь'} for c in
                     comments]
    return jsonify(comments_data)


@app.route('/add_comment/<int:idea_id>', methods=['POST'])
def add_comment(idea_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    text = request.form.get('comment_text')
    if text:
        db.session.add(Comment(user_id=user.id, idea_id=idea_id, text=text))
        db.session.commit()
    return redirect(url_for('ideas'))


@app.route('/create_team', methods=['POST'])
def create_team():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    name = request.form.get('team_name')
    description = request.form.get('description')
    if name:
        new_team = Team(name=name, description=description, leader_id=user.id, status='recruiting',
                        date=datetime.datetime.now().strftime('%d %b %Y'))
        db.session.add(new_team)
        db.session.add(TeamMember(team_id=new_team.id, user_id=user.id, role='Лидер',
                                  joined_date=datetime.datetime.now().strftime('%d %b %Y')))
        db.session.commit()
    return redirect(url_for('team'))


@app.route('/team_members/<int:team_id>')
def team_members(team_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    team = Team.query.get_or_404(team_id)
    members = TeamMember.query.filter_by(team_id=team_id).all()
    return render_template('team_members.html', team=team, members=members, username=user.username)


@app.route('/join_team/<int:team_id>', methods=['POST'])
def join_team(team_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    existing = TeamMember.query.filter_by(team_id=team_id, user_id=user.id).first()
    if not existing:
        db.session.add(TeamMember(team_id=team_id, user_id=user.id, role='Участник',
                                  joined_date=datetime.datetime.now().strftime('%d %b %Y')))
        db.session.commit()
    return redirect(url_for('team'))


@app.route('/send_message', methods=['POST'])
def send_message():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    flash('Сообщение отправлено!', 'success')
    return redirect(url_for('team'))


if __name__ == '__main__':
    app.run(debug=True)