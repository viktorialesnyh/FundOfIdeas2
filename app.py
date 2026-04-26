from flask import Flask, render_template, request, redirect, url_for, session
import datetime
from data import db, setup_database, User, Idea, DiaryEntry, Skill, TeamProfile



app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# Инициализация БД
setup_database(app)

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# === МАРШРУТЫ ===
@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', 'User')
    email = request.form.get('email', 'user@test.com')
    if User.query.filter_by(email=email).first():
        return redirect(url_for('index'))
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    return render_template('dashboard.html', username=user.username)

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    return render_template('profile.html',
                           username=user.username, email=user.email,
                           bio_text=user.bio, about_text=user.about_me,
                           city=user.city, joined_year=user.joined_year,
                           skills=user.skills)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.about_me = request.form.get('about_text')
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/update_bio', methods=['POST'])
def update_bio():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.bio = request.form.get('bio_text')
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/update_city', methods=['POST'])
def update_city():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.city = request.form.get('city')
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/update_email', methods=['POST'])
def update_email():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.email = request.form.get('email')
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/update_joined', methods=['POST'])
def update_joined():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    user.joined_year = request.form.get('joined_year')
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/add_skill', methods=['POST'])
def add_skill():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
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
    if not user: return redirect(url_for('index'))
    skill = Skill.query.get(skill_id)
    if skill and skill.user_id == user.id:
        db.session.delete(skill)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route('/ideas')
def ideas():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    return render_template('ideas.html', username=user.username, user=user)

@app.route('/create_idea', methods=['POST'])
def create_idea():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
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

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    if request.method == 'POST':
        text = request.form.get('entry_text')
        tag = request.form.get('tag', 'success')
        if text:
            db.session.add(DiaryEntry(user_id=user.id, text=text, tag=tag,
                                      date=datetime.datetime.now().strftime('%d %b, %H:%M')))
            db.session.commit()
        return redirect(url_for('diary'))
    entries = DiaryEntry.query.filter_by(user_id=user.id).order_by(DiaryEntry.id.desc()).all()
    return render_template('diary.html', username=user.username, entries=entries)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/update_idea/<int:idea_id>', methods=['POST'])
def update_idea(idea_id):
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    
    idea = Idea.query.get_or_404(idea_id)
    # Защита: редактировать может только автор
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

@app.route('/team')
def team():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    
    # Получаем все профили, кроме своего (чтобы не видеть себя в поиске)
    profiles = TeamProfile.query.filter(TeamProfile.user_id != user.id).all()
    
    # Проверяем, есть ли у текущего пользователя свой профиль
    my_profile = TeamProfile.query.filter_by(user_id=user.id).first()
    
    return render_template('team.html', 
                           username=user.username, 
                           profiles=profiles, 
                           my_profile=my_profile)

@app.route('/create_team_profile', methods=['POST'])
def create_team_profile():
    user = get_current_user()
    if not user: return redirect(url_for('index'))
    
    # Если профиль уже есть, обновляем его
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
    if not user: return redirect(url_for('index'))
    
    profile = TeamProfile.query.filter_by(user_id=user.id).first()
    if profile:
        db.session.delete(profile)
        db.session.commit()
    return redirect(url_for('team'))

if __name__ == '__main__':
    app.run(debug=True)