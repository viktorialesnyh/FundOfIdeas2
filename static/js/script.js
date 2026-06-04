// === ЛОГИКА АВТОРИЗАЦИИ ===
function switchTab(tab) {
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (tab === 'login') {
        loginTab.classList.add('active'); registerTab.classList.remove('active');
        loginForm.classList.remove('hidden'); registerForm.classList.add('hidden');
    } else {
        registerTab.classList.add('active'); loginTab.classList.remove('active');
        registerForm.classList.remove('hidden'); loginForm.classList.add('hidden');
    }
}

// === ПРОФИЛЬ ===
document.addEventListener("DOMContentLoaded", () => {
    const tabProfile = document.getElementById('tab-profile');
    const tabSettings = document.getElementById('tab-settings');
    const contentProfile = document.getElementById('content-profile');
    const contentSettings = document.getElementById('content-settings');
    if (tabProfile && tabSettings) {
        tabProfile.addEventListener('click', () => {
            tabProfile.classList.add('active'); tabSettings.classList.remove('active');
            contentProfile.style.display = 'block'; contentSettings.style.display = 'none';
        });
        tabSettings.addEventListener('click', () => {
            tabSettings.classList.add('active'); tabProfile.classList.remove('active');
            contentProfile.style.display = 'none'; contentSettings.style.display = 'block';
        });
    }
});

function toggleSkillsForm() {
    const form = document.getElementById('addSkillForm');
    if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// === ИДЕИ (Фильтры/Поиск на странице /ideas) ===
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
                    if (filter === 'all' || card.dataset.visibility === filter) card.classList.remove('hidden');
                    else card.classList.add('hidden');
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
    toggleFormBtn.addEventListener('click', () => entryFormContainer.classList.toggle('hidden'));
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
                if (card.textContent.toLowerCase().includes(term)) card.classList.remove('hidden');
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

// === МОДАЛЬНЫЕ ОКНА ===
function openModal() { document.getElementById('createIdeaModal').classList.add('active'); }
function closeModal() { document.querySelectorAll('.modal').forEach(m => m.classList.remove('active')); }
document.addEventListener('click', (e) => { if (e.target.classList.contains('modal')) closeModal(); });
document.addEventListener('keydown', (e) => { if(e.key === 'Escape') closeModal(); });

function openViewModal(card) {
    const t = card.dataset.title, d = card.dataset.desc, cat = card.dataset.category, vis = card.dataset.visibility;
    const lic = card.dataset.license, tags = card.dataset.tags, date = card.dataset.date;
    document.getElementById('viewTitle').textContent = t;
    document.getElementById('viewDate').textContent = ` ${date}`;
    const catNames = {'edtech':'🎓 EdTech','health':'🏥 HealthTech','fintech':'💰 FinTech','other':'📦 Другое'};
    document.getElementById('viewCategory').textContent = catNames[cat] || cat;
    const visNames = {'draft':' Черновик','private':'🔒 Приватная','published':'🌍 Опубликована'};
    const vb = document.getElementById('viewVisibility');
    vb.textContent = visNames[vis] || vis; vb.className = 'badge ' + vis;
    document.getElementById('viewDesc').textContent = d;
    const tc = document.getElementById('viewTags'); tc.innerHTML = '';
    if (tags) tags.split(',').forEach(tag => { if(tag.trim()) { const s = document.createElement('span'); s.textContent = tag.trim(); tc.appendChild(s); } });
    const licNames = {'all_rights':'© Все права','cc_by':'CC BY','cc_by_sa':'CC BY-SA','cc_by_nc':'CC BY-NC','mit':'MIT','public_domain':'🌍 Public Domain'};
    document.getElementById('viewLicense').textContent = `Лицензия: ${licNames[lic] || lic}`;
    document.getElementById('viewIdeaModal').classList.add('active');
}

function openEditModal(card) {
    const id = card.dataset.id;
    document.getElementById('editTitle').value = card.dataset.title;
    document.getElementById('editDesc').value = card.dataset.desc;
    document.getElementById('editCategory').value = card.dataset.category;
    document.getElementById('editVisibility').value = card.dataset.visibility;
    document.getElementById('editLicense').value = card.dataset.license;
    document.getElementById('editTags').value = card.dataset.tags;
    document.getElementById('editForm').action = `/update_idea/${id}`;
    document.getElementById('editIdeaModal').classList.add('active');
}

function closeAnyModal(id) { const m = document.getElementById(id); if(m) m.classList.remove('active'); }

function escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }

// === НОВЫЕ ФУНКЦИИ ДЛЯ КОММЕНТАРИЕВ (АСИНХРОННЫЕ, С ОТВЕТАМИ) ===
let currentIdeaIdForComments = null;

async function openCommentsModal(ideaId) {
    currentIdeaIdForComments = ideaId;
    document.getElementById('commentText').value = '';
    document.getElementById('commentParentId').value = '';
    document.getElementById('commentsModal').classList.add('active');
    await loadComments(ideaId);
}

async function loadComments(ideaId) {
    const list = document.getElementById('commentsList');
    list.innerHTML = '<p class="no-comments">Загрузка...</p>';
    try {
        const res = await fetch(`/get_comments/${ideaId}`);
        if (!res.ok) throw new Error('Fail');
        const data = await res.json();

        const commentsById = {};
        data.forEach(c => { commentsById[c.id] = c; c.children = []; });
        const roots = [];
        data.forEach(c => {
            if (c.parent_id && commentsById[c.parent_id]) {
                commentsById[c.parent_id].children.push(c);
            } else {
                roots.push(c);
            }
        });

        function renderComment(comment) {
            const div = document.createElement('div');
            div.className = 'comment-item';
            div.setAttribute('data-comment-id', comment.id);
            div.innerHTML = `
                <div class="comment-header">
                    <span class="comment-author">
                        <a href="/user/${comment.author_id}" style="text-decoration: none; color: #374151;">${escapeHtml(comment.author)}</a>
                    </span>
                    <span class="comment-date">${escapeHtml(comment.date)}</span>
                </div>
                <p class="comment-text">${escapeHtml(comment.text)}</p>
                <button class="reply-btn" onclick="showReplyForm(${comment.id})">Ответить</button>
                <div class="replies" style="margin-left: 30px; margin-top: 10px;"></div>
            `;
            const repliesContainer = div.querySelector('.replies');
            if (comment.children && comment.children.length) {
                comment.children.forEach(child => {
                    repliesContainer.appendChild(renderComment(child));
                });
            }
            return div;
        }

        list.innerHTML = '';
        if (roots.length === 0) {
            list.innerHTML = '<p class="no-comments">Пока нет комментариев.</p>';
        } else {
            roots.forEach(root => list.appendChild(renderComment(root)));
        }
    } catch (e) {
        list.innerHTML = '<p class="no-comments">Ошибка загрузки.</p>';
    }
}

function showReplyForm(commentId) {
    document.getElementById('commentParentId').value = commentId;
    const textarea = document.getElementById('commentText');
    textarea.focus();
    textarea.scrollIntoView({ behavior: 'smooth' });
}

async function submitComment() {
    const ideaId = currentIdeaIdForComments;
    const text = document.getElementById('commentText').value.trim();
    const parentId = document.getElementById('commentParentId').value;
    if (!text) return;

    const formData = new FormData();
    formData.append('comment_text', text);
    if (parentId) formData.append('parent_id', parentId);

    try {
        const res = await fetch(`/add_comment/${ideaId}`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: formData
        });
        if (!res.ok) throw new Error('Network error');
        const result = await res.json();
        if (result.success) {
            document.getElementById('commentText').value = '';
            document.getElementById('commentParentId').value = '';
            await loadComments(ideaId);
            updateCommentsCount(ideaId, result.comments_count);
        }
    } catch (err) {
        alert('Ошибка при отправке комментария');
    }
}

function updateCommentsCount(ideaId, newCount) {
    const btn = document.getElementById(`commentsBtn-${ideaId}`);
    if (btn) btn.innerHTML = `💬 Комментарии (${newCount})`;
}

function closeCommentsModal() {
    document.getElementById('commentsModal').classList.remove('active');
    currentIdeaIdForComments = null;
}

// === ЛАЙКИ В ЛЕНТЕ ===
function toggleLike(btn) {
    fetch(`/like_idea/${btn.dataset.id}`, { method: 'POST', headers: {'Content-Type':'application/json','X-Requested-With':'XMLHttpRequest'} })
    .then(r => r.json()).then(data => {
        btn.dataset.liked = data.is_liked;
        btn.querySelector('.like-count').textContent = data.likes;
        const icon = btn.querySelector('.like-icon');
        if (data.is_liked) { icon.textContent = '❤️'; btn.classList.add('liked'); }
        else { icon.textContent = '🤍'; btn.classList.remove('liked'); }
    }).catch(() => window.location.href = '/');
}

// === ПОИСК НА ГЛАВНОЙ (ТОЛЬКО ПО ENTER) ===
document.addEventListener('DOMContentLoaded', () => {
    const feedContainer = document.getElementById('feedContainer');
    const searchInput = document.getElementById('feedSearchInput');
    const clearBtn = document.getElementById('feedSearchClear');
    const loading = document.getElementById('feedLoading');
    const feedTitle = document.getElementById('feedTitle');
    let originalHTML = feedContainer.innerHTML;

    searchInput.addEventListener('input', () => {
        if (searchInput.value.trim()) {
            clearBtn.classList.remove('hidden');
        } else {
            clearBtn.classList.add('hidden');
        }
    });

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const q = searchInput.value.trim();
            if (q) {
                runSearch(q);
            }
        }
    });

    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearBtn.classList.add('hidden');
        restoreFeed();
    });

    async function runSearch(query) {
        loading.classList.remove('hidden');
        feedTitle.textContent = 'Поиск...';
        try {
            const res = await fetch(`/search_ideas?q=${encodeURIComponent(query)}`);
            if (!res.ok) throw new Error('Network error');
            const data = await res.json();
            renderResults(data, query);
        } catch (err) {
            feedContainer.innerHTML = '<p class="no-results"> Ошибка загрузки.</p>';
        } finally {
            loading.classList.add('hidden');
        }
    }

    function renderResults(ideas, query) {
        feedTitle.textContent = `Результаты по "${query}"`;
        if (ideas.length === 0) {
            feedContainer.innerHTML = '<p class="no-results">🔍 Идеи не найдены</p>';
            return;
        }
        let html = `<h2 class="feed-title">${feedTitle.textContent}</h2>`;
        ideas.forEach(i => {
            const tagsHtml = i.tags ? i.tags.split(',').map(t => t.trim() ? `<span>#${t.trim()}</span>` : '').join('') : '';
            html += `
            <article class="feed-card idea-card" data-id="${i.id}" data-title="${i.title}" data-desc="${i.description}" data-category="${i.category}" data-visibility="${i.visibility}" data-license="${i.license}" data-tags="${i.tags}" data-date="${i.date}">
                <div class="feed-card-header card-header">
                    <div class="feed-author">
                        <div class="feed-avatar member-avatar">${i.author_username.substring(0,2).toUpperCase()}</div>
                        <div><span class="feed-name">${i.author_username}</span><span class="feed-time">${i.date}</span></div>
                    </div>
                    <span class="badge published">🌍 Опубликована</span>
                </div>
                <h3 class="feed-title-text">${i.title}</h3>
                <p class="feed-desc">${i.description.substring(0,180)}${i.description.length>180?'...':''}</p>
                <div class="feed-tags card-tags">${tagsHtml}</div>
                <div class="feed-actions card-actions">
                    <button class="action-btn" onclick="openViewModal(this.closest('.idea-card'))">🔍 Открыть</button>
                    <button class="action-btn outline" id="commentsBtn-${i.id}" onclick="openCommentsModal(${i.id})">💬 Комментарии (${i.comments_count || 0})</button>
                </div>
            </article>`;
        });
        feedContainer.innerHTML = html;
    }

    function restoreFeed() {
        feedContainer.innerHTML = originalHTML;
        feedTitle.textContent = 'Рекомендации для вас';
    }
});

// === АВТО-ПЕРЕКЛЮЧЕНИЕ ВКЛАДКИ ПРИ ОШИБКАХ ===
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('tab') === 'register') {
        switchTab('register');
    }
});