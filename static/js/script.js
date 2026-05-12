// === ЛОГИКА АВТОРИЗАЦИИ (ВХОД/РЕГИСТРАЦИЯ) ===
function switchTab(tab) {
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (tab === 'login') {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    } else {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
    }
}

// === ЛОГИКА ПРОФИЛЯ (Переключение вкладок) ===
document.addEventListener("DOMContentLoaded", () => {
    const tabProfile = document.getElementById('tab-profile');
    const tabSettings = document.getElementById('tab-settings');
    const contentProfile = document.getElementById('content-profile');
    const contentSettings = document.getElementById('content-settings');
    if (tabProfile && tabSettings) {
        tabProfile.addEventListener('click', () => {
            tabProfile.classList.add('active');
            tabSettings.classList.remove('active');
            contentProfile.style.display = 'block';
            contentSettings.style.display = 'none';
        });

        tabSettings.addEventListener('click', () => {
            tabSettings.classList.add('active');
            tabProfile.classList.remove('active');
            contentProfile.style.display = 'none';
            contentSettings.style.display = 'block';
        });
    }
});

// === ЛОГИКА НАВЫКОВ ===
function toggleSkillsForm() {
    const form = document.getElementById('addSkillForm');
    if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// === ЛОГИКА ИДЕЙ (Фильтры и Поиск) ===
document.addEventListener("DOMContentLoaded", () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.idea-card');
    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter;
                cards.forEach(card => {
                    if (filter === 'all' || card.dataset.status === filter) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                });
            });
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            cards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                if (title.includes(term)) card.classList.remove('hidden');
                else card.classList.add('hidden');
            });
        });
    }
});

// === ДНЕВНИК ===
const toggleFormBtn = document.getElementById('toggleFormBtn');
const entryFormContainer = document.getElementById('entryFormContainer');
if (toggleFormBtn && entryFormContainer) {
    toggleFormBtn.addEventListener('click', () => {
        entryFormContainer.classList.toggle('hidden');
    });
}

// === КОМАНДА ===
document.addEventListener("DOMContentLoaded", () => {
    const teamSearch = document.getElementById('teamSearch');
    const teamCards = document.querySelectorAll('.team-card');
    const filterBtns = document.querySelectorAll('.filter-btn');
    if (teamSearch) {
        teamSearch.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            teamCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(term)) card.classList.remove('hidden');
                else card.classList.add('hidden');
            });
        });
    }

    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter;
                teamCards.forEach(card => {
                    if (filter === 'all' || card.dataset.category.includes(filter)) card.classList.remove('hidden');
                    else card.classList.add('hidden');
                });
            });
        });
    }
});

// === МОДАЛЬНЫЕ ОКНА ИДЕЙ ===
function openModal() { document.getElementById('createIdeaModal').classList.add('active'); }
function closeModal() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(m => m.classList.remove('active'));
}
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) closeModal();
});
document.addEventListener('keydown', (e) => { if(e.key === 'Escape') closeModal(); });

// === МОДАЛЬНОЕ ОКНО: ПРОСМОТР ИДЕИ ===
function openViewModal(card) {
    const title = card.dataset.title;
    const desc = card.dataset.desc;
    const category = card.dataset.category;
    const visibility = card.dataset.visibility;
    const license = card.dataset.license;
    const tags = card.dataset.tags;
    const date = card.dataset.date;

    document.getElementById('viewTitle').textContent = title;
    document.getElementById('viewDate').textContent = `📅 ${date}`;

    const catNames = { 'edtech': '🎓 EdTech', 'health': '🏥 HealthTech', 'fintech': '💰 FinTech', 'other': '📦 Другое' };
    document.getElementById('viewCategory').textContent = catNames[category] || category;

    const visNames = { 'draft': '📝 Черновик', 'private': '🔒 Приватная', 'published': '🌍 Опубликована' };
    const visBadge = document.getElementById('viewVisibility');
    visBadge.textContent = visNames[visibility] || visibility;
    visBadge.className = 'badge ' + visibility;

    document.getElementById('viewDesc').textContent = desc;

    const tagsContainer = document.getElementById('viewTags');
    tagsContainer.innerHTML = '';
    if (tags) {
        tags.split(',').forEach(tag => {
            if (tag.trim()) {
                const span = document.createElement('span');
                span.textContent = tag.trim();
                tagsContainer.appendChild(span);
            }
        });
    }

    const licNames = {
        'all_rights': '© Все права защищены', 'cc_by': 'CC BY', 'cc_by_sa': 'CC BY-SA',
        'cc_by_nc': 'CC BY-NC', 'mit': 'MIT License', 'public_domain': '🌍 Public Domain'
    };
    document.getElementById('viewLicense').textContent = `Лицензия: ${licNames[license] || license}`;

    document.getElementById('viewIdeaModal').classList.add('active');
}

// === МОДАЛЬНОЕ ОКНО: РЕДАКТИРОВАНИЕ ИДЕИ ===
function openEditModal(card) {
    const ideaId = card.dataset.id;
    document.getElementById('editTitle').value = card.dataset.title;
    document.getElementById('editDesc').value = card.dataset.desc;
    document.getElementById('editCategory').value = card.dataset.category;
    document.getElementById('editVisibility').value = card.dataset.visibility;
    document.getElementById('editLicense').value = card.dataset.license;
    document.getElementById('editTags').value = card.dataset.tags;

    const editForm = document.getElementById('editForm');
    editForm.action = `/update_idea/${ideaId}`;

    document.getElementById('editIdeaModal').classList.add('active');
}

// === ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ===
function closeAnyModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// === ЗАЩИТА ОТ XSS ===
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// === ЛОГИКА МОДАЛЬНОГО ОКНА КОММЕНТАРИЕВ (С ПРОСМОТРОМ) ===
let currentIdeaIdForComments = null;

async function openCommentsModal(ideaId) {
    currentIdeaIdForComments = ideaId;
    const form = document.getElementById('commentForm');
    if (form) form.action = `/add_comment/${ideaId}`;

    const modal = document.getElementById('commentsModal');
    if (modal) modal.classList.add('active');

    const list = document.querySelector('#commentsModal .comments-list');
    if (!list) return;

    list.innerHTML = '<p class="no-comments">Загрузка комментариев...</p>';

    try {
        const response = await fetch(`/get_comments/${ideaId}`);
        if (!response.ok) throw new Error('Failed to load');
        const comments = await response.json();

        list.innerHTML = '';
        if (comments.length === 0) {
            list.innerHTML = '<p class="no-comments">Пока нет комментариев. Будьте первым!</p>';
        } else {
            comments.forEach(c => {
                const item = document.createElement('div');
                item.className = 'comment-item';
                item.innerHTML = `
                    <div class="comment-header">
                        <span class="comment-author">${escapeHtml(c.author)}</span>
                    </div>
                    <p class="comment-text">${escapeHtml(c.text)}</p>
                `;
                list.appendChild(item);
            });
        }
    } catch (error) {
        list.innerHTML = '<p class="no-comments">Ошибка загрузки комментариев.</p>';
        console.error(error);
    }
}

function closeCommentsModal() {
    const modal = document.getElementById('commentsModal');
    if (modal) modal.classList.remove('active');
    currentIdeaIdForComments = null;
}

document.addEventListener('click', (e) => {
    const modal = document.getElementById('commentsModal');
    if (e.target === modal) closeCommentsModal();
});

// === ЛОГИКА ЛАЙКОВ В ЛЕНТЕ (AJAX) ===
function toggleLike(btn) {
    const ideaId = btn.dataset.id;
    fetch(`/like_idea/${ideaId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        btn.dataset.liked = data.is_liked;
        btn.querySelector('.like-count').textContent = data.likes;
        const icon = btn.querySelector('.like-icon');
        if (data.is_liked) {
            icon.textContent = '❤️';
            btn.classList.add('liked');
        } else {
            icon.textContent = '🤍';
            btn.classList.remove('liked');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/';
    });
}