from flask import Flask, render_template, request, redirect, url_for, session
import datetime 

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # ЭТО ВАЖНО для сессий!

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    # Создаем сессию
    session['username'] = email.split('@')[0].title() if '@' in email else 'User'
    session['email'] = email
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', 'User')
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Дефолтные навыки, если их ещё нет в сессии
    default_skills = [
        {'name': 'Разработка', 'icon': '💻', 'level': 80, 'level_text': 'Продвинутый'},
        {'name': 'Продукт', 'icon': '📊', 'level': 60, 'level_text': 'Средний'},
        {'name': 'Маркетинг', 'icon': '📢', 'level': 40, 'level_text': 'Начальный'}
    ]
    skills = session.get('skills', default_skills)

    return render_template('profile.html', 
                           username=session['username'], 
                           email=session.get('email', 'email@example.com'), 
                           about_text=session.get('about_text', ''),
                           bio_text=session.get('bio_text', 'Основатель стартапа...'),
                           city=session.get('city', 'Москва, Россия'),
                           joined_year=session.get('joined_year', '2026'),
                           skills=skills)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/ideas')
def ideas():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('ideas.html', username=session['username'])


@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Инициализируем список записей в сессии, если его нет
    if 'diary_entries' not in session:
        session['diary_entries'] = []

    if request.method == 'POST':
        text = request.form.get('entry_text')
        tag = request.form.get('tag', 'success')
        if text and text.strip():
            new_entry = {
                'text': text,
                'tag': tag,
                'date': datetime.datetime.now().strftime('%d %b, %H:%M')
            }
            session['diary_entries'].insert(0, new_entry)  # Новые сверху
            session.modified = True
        return redirect(url_for('diary'))

    return render_template('diary.html', username=session['username'], entries=session.get('diary_entries', []))

@app.route('/team')
def team():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('team.html', username=session['username'])

@app.route('/create_idea', methods=['POST'])
def create_idea():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category', 'other')
    visibility = request.form.get('visibility', 'draft')
    license = request.form.get('license', 'all_rights')
    tags = request.form.get('tags', '')
    
    # Создаем новую идею
    new_idea = {
        'title': title,
        'description': description,
        'category': category,
        'visibility': visibility,
        'license': license,
        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
        'author': session['username'],
        'date': datetime.datetime.now().strftime('%d %b %Y')
    }
    
    # Сохраняем в сессию (в реальном проекте - в базу данных)
    if 'ideas' not in session:
        session['ideas'] = []
    session['ideas'].append(new_idea)
    session.modified = True
    
    return redirect(url_for('ideas'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Сохраняем текст в сессию
    about_text = request.form.get('about_text')
    session['about_text'] = about_text
    
    return redirect(url_for('profile'))

@app.route('/update_bio', methods=['POST'])
def update_bio():
    if 'username' not in session:
        return redirect(url_for('index'))
    session['bio_text'] = request.form.get('bio_text')
    return redirect(url_for('profile'))

@app.route('/update_city', methods=['POST'])
def update_city():
    if 'username' not in session:
        return redirect(url_for('index'))
    session['city'] = request.form.get('city')
    return redirect(url_for('profile'))

@app.route('/update_email', methods=['POST'])
def update_email():
    if 'username' not in session:
        return redirect(url_for('index'))
    session['email'] = request.form.get('email')
    return redirect(url_for('profile'))

@app.route('/update_joined', methods=['POST'])
def update_joined():
    if 'username' not in session:
        return redirect(url_for('index'))
    session['joined_year'] = request.form.get('joined_year')
    return redirect(url_for('profile'))

@app.route('/add_skill', methods=['POST'])
def add_skill():
    if 'username' not in session: return redirect(url_for('index'))
    
    name = request.form.get('skill_name')
    icon = request.form.get('skill_icon', '🛠')
    level = int(request.form.get('skill_level', 50))
    
    text = 'Начальный' if level < 50 else 'Средний' if level < 75 else 'Продвинутый' if level < 100 else 'Эксперт'
    
    if 'skills' not in session:
        session['skills'] = []
    session['skills'].append({'name': name, 'icon': icon, 'level': level, 'level_text': text})
    session.modified = True
    return redirect(url_for('profile'))

@app.route('/delete_skill/<int:idx>')
def delete_skill(idx):
    if 'username' not in session: return redirect(url_for('index'))
    if 'skills' in session and 0 <= idx < len(session['skills']):
        session['skills'].pop(idx)
        session.modified = True
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)