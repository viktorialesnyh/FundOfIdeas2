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
    
    // Переключение вкладок "Мой профиль" / "Настройки"
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
// === ЛОГИКА СТРАНИЦЫ ИДЕЙ ===
document.addEventListener("DOMContentLoaded", () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.idea-card');

    // Фильтрация по статусу
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

    // Поиск по названию
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

    // Поиск команд
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

    // Фильтрация по категориям
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
        document.body.style.overflow = 'hidden'; // Запретить прокрутку фона
    }
}

function closeModal() {
    const modal = document.getElementById('createIdeaModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Вернуть прокрутку
    }
}

// Закрытие по клику вне модального окна
document.addEventListener('click', (e) => {
    const modal = document.getElementById('createIdeaModal');
    if (modal && e.target === modal) {
        closeModal();
    }
});

// Закрытие по Escape
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