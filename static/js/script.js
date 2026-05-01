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

function openViewModal(card) { /* Логика просмотра */ }
function openEditModal(card) { /* Логика редактирования */ }