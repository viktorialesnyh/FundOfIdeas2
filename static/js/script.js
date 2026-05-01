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

// === ЛОГИКА ПРОФИЛЯ ===
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

// === ЛОГИКА СТРАНИЦЫ ИДЕЙ (Фильтры и Поиск) ===
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
                if (title.includes(term)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    }
});

// === ЛОГИКА ДНЕВНИКА ===
const toggleFormBtn = document.getElementById('toggleFormBtn');
const entryFormContainer = document.getElementById('entryFormContainer');
if (toggleFormBtn && entryFormContainer) {
    toggleFormBtn.addEventListener('click', () => {
        entryFormContainer.classList.toggle('hidden');
        if (!entryFormContainer.classList.contains('hidden')) {
            entryFormContainer.querySelector('textarea').focus();
        }
    });
}

// === ЛОГИКА СТРАНИЦЫ КОМАНДА ===
document.addEventListener("DOMContentLoaded", () => {
    const teamSearch = document.getElementById('teamSearch');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const teamCards = document.querySelectorAll('.team-card');

    if (teamSearch) {
        teamSearch.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            teamCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const project = card.querySelector('.team-project').textContent.toLowerCase();
                const skills = card.querySelector('.team-skills').textContent.toLowerCase();

                if (title.includes(term) || project.includes(term) || skills.includes(term)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
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
                    if (filter === 'all' || card.dataset.category.includes(filter)) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                });
            });
        });
    }
});

// === МОДАЛЬНОЕ ОКНО СОЗДАНИЯ ИДЕИ ===
function openModal() {
    const modal = document.getElementById('createIdeaModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}
function closeModal() {
    const modal = document.getElementById('createIdeaModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}
document.addEventListener('click', (e) => {
    const modal = document.getElementById('createIdeaModal');
    if (modal && e.target === modal) {
        closeModal();
    }
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// === ЛОГИКА НАВЫКОВ ===
function toggleSkillsForm() {
    const form = document.getElementById('addSkillForm');
    if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// === ПРОСМОТР ИДЕИ ===
function openViewModal(card) {
    if (!card) return;
    document.getElementById('viewTitle').textContent = card.dataset.title || '';
    document.getElementById('viewDate').textContent = '📅 ' + (card.dataset.date || '');
    document.getElementById('viewDesc').textContent = card.dataset.desc || '';
    document.getElementById('viewCategory').textContent = (card.dataset.category || '').toUpperCase();
    var visBadge = document.getElementById('viewVisibility');
    visBadge.textContent = card.dataset.visibility || '';
    visBadge.className = 'badge ' + (card.dataset.visibility || '');
    var licenseText = (card.dataset.license || '').split('_').join(' ').toUpperCase();
    document.getElementById('viewLicense').textContent = ' Лицензия: ' + licenseText;
    var tagsContainer = document.getElementById('viewTags');
    tagsContainer.innerHTML = '';
    if (card.dataset.tags) {
        var tags = card.dataset.tags.split(',');
        for (var i = 0; i < tags.length; i++) {
            var t = tags[i].trim();
            if (t) {
                var span = document.createElement('span');
                span.textContent = t;
                tagsContainer.appendChild(span);
            }
        }
    }
    document.getElementById('viewIdeaModal').classList.add('active');
}

// === РЕДАКТИРОВАНИЕ ИДЕИ ===
function openEditModal(card) {
    if (!card) return;
    var id = card.dataset.id;
    document.getElementById('editForm').action = '/update_idea/' + id;
    document.getElementById('editTitle').value = card.dataset.title || '';
    document.getElementById('editDesc').value = card.dataset.desc || '';
    document.getElementById('editCategory').value = card.dataset.category || 'other';
    document.getElementById('editVisibility').value = card.dataset.visibility || 'draft';
    document.getElementById('editLicense').value = card.dataset.license || 'all_rights';
    document.getElementById('editTags').value = card.dataset.tags || '';
    document.getElementById('editIdeaModal').classList.add('active');
}

// === УНИВЕРСАЛЬНОЕ ЗАКРЫТИЕ МОДАЛОК ===
function closeAnyModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        if (event.target.id !== 'createIdeaModal') {
            event.target.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});

// === ЛОГИКА НАСТРОЕК (НОВОЕ) ===
const settingsForm = document.getElementById('settingsForm');
if (settingsForm) {
    settingsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(settingsForm);
        const btn = settingsForm.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.textContent = 'Сохранение';
        btn.disabled = true;

        try {
            const response = await fetch('/update_settings', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                btn.textContent = 'Сохранено';
                btn.style.background = '#10b981';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 2000);
            } else {
                throw new Error('Ошибка сервера');
            }
        } catch (err) {
            btn.textContent = 'Ошибка';
            btn.style.background = '#ef4444';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 2000);
        }
    });
}