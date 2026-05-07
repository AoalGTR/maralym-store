// ===== NAVIGATION HISTORY =====
const history = ['screen-home'];

// ===== SHOW SCREEN =====
function showScreen(screenId) {
  // Hide all screens
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));

  // Show target screen
  const target = document.getElementById(screenId);
  if (target) {
    target.classList.add('active');
    target.scrollTop = 0;
  }

  // Push to history (avoid duplicates at the top)
  if (history[history.length - 1] !== screenId) {
    history.push(screenId);
  }
}

// ===== GO BACK =====
function goBack() {
  if (history.length > 1) {
    history.pop(); // remove current
    const previous = history[history.length - 1];
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(previous);
    if (target) {
      target.classList.add('active');
    }
    updateActiveTab(previous);
  }
}

// ===== SWITCH TAB (bottom nav) =====
function switchTab(screenId, tabBtn) {
  // Reset history to this tab
  history.length = 0;
  history.push(screenId);

  // Show screen
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const target = document.getElementById(screenId);
  if (target) {
    target.classList.add('active');
    target.scrollTop = 0;
  }

  // Update active tab style
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  if (tabBtn) {
    tabBtn.classList.add('active');
  }
}

// ===== UPDATE ACTIVE TAB HIGHLIGHT =====
function updateActiveTab(screenId) {
  const tabMap = {
    'screen-home': 0,
    'screen-search': 1,
    'screen-categories': 2,
    'screen-profile': 3,
  };

  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(t => t.classList.remove('active'));

  if (screenId in tabMap) {
    tabs[tabMap[screenId]].classList.add('active');
  }
}

// ===== PRODUCT SEARCH FILTER =====
function filterProducts() {
  const query = document.getElementById('searchInput').value.toLowerCase();
  const cards = document.querySelectorAll('#searchResults .product-card');

  cards.forEach(card => {
    const name = card.getAttribute('data-name') || '';
    card.style.display = name.includes(query) ? 'flex' : 'none';
  });
}
