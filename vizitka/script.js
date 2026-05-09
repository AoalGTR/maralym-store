// Products loaded from API
let products = [];

// State management
let currentFilter = 'all';
let maxPrice = 10000;
let cart = [];
let favorites = [];
let orders = [];
let userProfile = { name: '', email: '', phone: '', address: '' };

const API_BASE = 'https://maralym-store-4xe7.onrender.com/api';

async function initState() {
  try {
    // Load products from API
    const productsRes = await fetch(`${API_BASE}/products`);
    if (productsRes.ok) {
      const productsData = await productsRes.json();
      products = productsData.items || [];
    }

    // Load state from API
    const stateRes = await fetch(`${API_BASE}/state`);
    if (stateRes.ok) {
      const data = await stateRes.json();
      cart = data.cart || [];
      favorites = data.favorites || [];
      orders = data.orders || [];
        userProfile = data.user_profile || userProfile;
        // Bind session email from server to frontend profile/localStorage
        const sessionEmail = data.session_email || (data.user_profile && data.user_profile.email) || localStorage.getItem('userEmail') || '';
        if (sessionEmail) {
          userProfile.email = userProfile.email || sessionEmail;
          localStorage.setItem('userEmail', sessionEmail);
          localStorage.setItem('userProfile', JSON.stringify(userProfile));
        }
    }
  } catch (err) {
    // fallback to localStorage when backend not available
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    orders = JSON.parse(localStorage.getItem('orders')) || [];
    userProfile = JSON.parse(localStorage.getItem('userProfile')) || userProfile;
  }
}
let selectedProduct = null;

// DOM elements
const productsRoot = document.getElementById('products');
const modal = document.getElementById('modal');
const cartSidebar = document.getElementById('cartSidebar');
const favoritesSidebar = document.getElementById('favoritesSidebar');
const profileModal = document.getElementById('profileModal');
const checkoutModal = document.getElementById('checkoutModal');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// Helper functions
function formatPrice(value) {
  return new Intl.NumberFormat('ru-RU').format(value) + ' сом';
}

function renderStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  let stars = '★'.repeat(full);
  if (half) stars += '☆';
  return stars;
}

function getGradient(category) {
  const gradients = {
    shirts: 'linear-gradient(160deg, #f0d9df, #c88a9b)',
    pants: 'linear-gradient(160deg, #e6dfd8, #b8a79a)',
    dresses: 'linear-gradient(160deg, #efc6d2, #b26a85)',
    outerwear: 'linear-gradient(160deg, #d9dde4, #8792a3)'
  };
  return gradients[category] || 'linear-gradient(160deg, #f0d9df, #c88a9b)';
}

// Render products
function renderProducts() {
  let filtered = products;
  
  if (currentFilter !== 'all') {
    filtered = filtered.filter(p => p.category === currentFilter);
  }
  
  filtered = filtered.filter(p => p.price <= maxPrice);
  
  const searchQuery = document.getElementById('searchInput').value.toLowerCase();
  if (searchQuery) {
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(searchQuery) || 
      p.description.toLowerCase().includes(searchQuery)
    );
  }
  
  productsRoot.innerHTML = filtered.map(product => {
    const isFavorite = favorites.includes(product.id);
    return `
      <article class="product-card">
        <div class="product-visual">
          <div class="product-image" style="background-image: url('${product.image}')"></div>
          <div class="badge">${product.badge}</div>
          <button class="favorite-btn ${isFavorite ? 'active' : ''}" data-id="${product.id}" title="Добавить в избранное">❤️</button>
        </div>
        <div class="product-body">
          <div class="product-top">
            <h3>${product.name}</h3>
            <div class="price">${formatPrice(product.price)}</div>
          </div>
          <div class="rating-display">${renderStars(product.rating)} ${product.rating}</div>
          <p>${product.description}</p>
          <div class="product-actions">
            <button class="small-btn primary" data-id="${product.id}">Подробнее</button>
            <button class="small-btn add-cart-btn" data-id="${product.id}">В корзину</button>
          </div>
        </div>
      </article>
    `;
  }).join('');

  // Add event listeners
  document.querySelectorAll('[data-id]').forEach(btn => {
    const id = Number(btn.dataset.id);
    if (btn.classList.contains('primary')) {
      btn.addEventListener('click', () => openProductModal(id));
    } else if (btn.classList.contains('add-cart-btn')) {
      btn.addEventListener('click', () => addToCart(id, 1));
    }
  });

  document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleFavorite(Number(btn.dataset.id));
    });
  });
}

// Product modal
function openProductModal(id) {
  selectedProduct = products.find(p => p.id === id);
  if (!selectedProduct) return;

  document.getElementById('modalTitle').textContent = selectedProduct.name;
  document.getElementById('modalTitleVisual').textContent = selectedProduct.name;
  document.getElementById('modalMiniText').textContent = selectedProduct.description;
  document.getElementById('modalDescription').textContent = selectedProduct.description;
  document.getElementById('modalPrice').textContent = formatPrice(selectedProduct.price);
  document.getElementById('modalCategoryBadge').textContent = selectedProduct.badge;
  document.getElementById('modalRating').textContent = `⭐ ${renderStars(selectedProduct.rating)} (${selectedProduct.rating}/5)`;
  document.getElementById('modalVisual').style.background = getGradient(selectedProduct.category);

  // Fill size options
  const sizeSelect = document.getElementById('sizeSelect');
  sizeSelect.innerHTML = '<option>Выберите размер</option>' + 
    selectedProduct.tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');

  // Reset quantity
  document.getElementById('quantityInput').value = 1;

  // Update button state
  const addBtn = document.getElementById('addToCartBtn');
  const favBtn = document.getElementById('addToFavBtn');
  const isFav = favorites.includes(id);
  favBtn.innerHTML = isFav ? '❤️ В избранном' : '❤️ В избранное';
  addBtn.onclick = () => {
    const size = sizeSelect.value;
    if (size === 'Выберите размер') {
      alert('Пожалуйста, выберите размер');
      return;
    }
    const qty = parseInt(document.getElementById('quantityInput').value);
    addToCart(id, qty, size);
  };
  favBtn.onclick = () => toggleFavorite(id);

  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
}

function closeProductModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
}

document.getElementById('closeModal').addEventListener('click', closeProductModal);
document.getElementById('decreaseQty').addEventListener('click', () => {
  const input = document.getElementById('quantityInput');
  if (input.value > 1) input.value--;
});
document.getElementById('increaseQty').addEventListener('click', () => {
  const input = document.getElementById('quantityInput');
  input.value++;
});

// Cart management
function addToCart(productId, quantity, size = null) {
  const product = products.find(p => p.id === productId);
  const existingItem = cart.find(item => item.id === productId && item.size === (size || null));

  if (existingItem) {
    existingItem.quantity += quantity;
  } else {
    cart.push({
      id: productId,
      name: product.name,
      price: product.price,
      quantity,
      size
    });
  }

  saveCart();
  updateCartUI();
  closeProductModal();
  alert(`${product.name} добавлено в корзину!`);
}

function removeFromCart(index) {
  cart.splice(index, 1);
  saveCart();
  updateCartUI();
}

function saveCart() {
  // Try to persist to server; fallback to localStorage
  (async () => {
    try {
      const payload = cart.map(item => ({ id: item.id, quantity: item.quantity, size: item.size }));
      const res = await fetch(`${API_BASE}/cart`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('failed to save');
    } catch (err) {
      localStorage.setItem('cart', JSON.stringify(cart));
    }
  })();
}

function updateCartUI() {
  document.getElementById('cartCount').textContent = cart.length;
  const cartItems = document.getElementById('cartItems');
  
  if (cart.length === 0) {
    cartItems.innerHTML = '<p class="empty-message">Корзина пуста</p>';
    document.getElementById('cartTotal').textContent = '0 сом';
    return;
  }

  let total = 0;
  cartItems.innerHTML = cart.map((item, index) => {
    const subtotal = item.price * item.quantity;
    total += subtotal;
    return `
      <div class="cart-item">
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          ${item.size ? `<small>Размер: ${item.size}</small>` : ''}
          <div>${item.quantity} × ${formatPrice(item.price)}</div>
        </div>
        <div class="cart-item-price">${formatPrice(subtotal)}</div>
        <button class="remove-btn" data-index="${index}">✕</button>
      </div>
    `;
  }).join('');

  document.getElementById('cartTotal').textContent = formatPrice(total);

  document.querySelectorAll('.remove-btn').forEach(btn => {
    btn.addEventListener('click', () => removeFromCart(Number(btn.dataset.index)));
  });
}

// Favorites
function toggleFavorite(productId) {
  (async () => {
    try {
      const res = await fetch(`${API_BASE}/favorites/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
      });
      if (!res.ok) throw new Error('fav toggle failed');
      const data = await res.json();
      favorites = data.favorites || favorites;
      updateFavoritesUI();
      renderProducts();
    } catch (err) {
      // fallback local
      const index = favorites.indexOf(productId);
      if (index > -1) favorites.splice(index, 1);
      else favorites.push(productId);
      localStorage.setItem('favorites', JSON.stringify(favorites));
      updateFavoritesUI();
      renderProducts();
    }
  })();
}

function saveFavorites() {
  localStorage.setItem('favorites', JSON.stringify(favorites));
}

function updateFavoritesUI() {
  document.getElementById('favCount').textContent = favorites.length;
  const favItems = document.getElementById('favoritesItems');
  
  if (favorites.length === 0) {
    favItems.innerHTML = '<p class="empty-message">Избранное пусто</p>';
    return;
  }

  favItems.innerHTML = favorites.map(id => {
    const product = products.find(p => p.id === id);
    return `
      <div class="fav-item">
        <strong>${product.name}</strong>
        <div>${formatPrice(product.price)}</div>
        <div style="display: flex; gap: 5px;">
          <button class="small-btn primary" data-id="${id}" style="flex: 1;">Подробнее</button>
          <button class="small-btn remove-fav" data-id="${id}">✕</button>
        </div>
      </div>
    `;
  }).join('');

  document.querySelectorAll('[data-id]').forEach(btn => {
    if (btn.classList.contains('primary')) {
      btn.addEventListener('click', () => {
        openProductModal(Number(btn.dataset.id));
        closeSidebars();
      });
    }
  });

  document.querySelectorAll('.remove-fav').forEach(btn => {
    btn.addEventListener('click', () => toggleFavorite(Number(btn.dataset.id)));
  });
}

// Sidebar management
function openSidebar(sidebar) {
  sidebar.classList.add('open');
  sidebarOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeSidebars() {
  cartSidebar.classList.remove('open');
  favoritesSidebar.classList.remove('open');
  sidebarOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

// Profile management
function updateProfileUI() {
  document.getElementById('userName').value = userProfile.name || '';
  document.getElementById('userEmail').value = userProfile.email || '';
  document.getElementById('userPhone').value = userProfile.phone || '';
  document.getElementById('userAddress').value = userProfile.address || '';

  const ordersList = document.getElementById('ordersList');
  if (orders.length === 0) {
    ordersList.innerHTML = '<p class="empty-message">Нет заказов</p>';
  } else {
    ordersList.innerHTML = orders.map(order => `
      <div class="order-item">
        <strong>Заказ #${order.id}</strong>
        <small>${new Date(order.date).toLocaleDateString('ru-RU')}</small>
        <div>${formatPrice(order.total)}</div>
        <small>${order.items} товаров</small>
      </div>
    `).join('');
  }
}

// Checkout
document.getElementById('checkoutForm').addEventListener('submit', (e) => {
  e.preventDefault();
  
  if (cart.length === 0) {
    alert('Корзина пуста!');
    return;
  }

  // Require login before checkout
  const savedEmail = localStorage.getItem('userEmail') || userProfile.email;
  if (!savedEmail) {
    showLoginModal();
    return;
  }

  const name = document.getElementById('checkoutName').value;
  const email = document.getElementById('checkoutEmail').value;
  const phone = document.getElementById('checkoutPhone').value;
  const address = document.getElementById('checkoutAddress').value;
  const delivery = document.getElementById('deliveryMethod').value;
  // Send checkout to server
  (async () => {
    try {
      const payload = {
        name,
        email,
        phone,
        address,
        delivery,
        items: cart.map(i => ({ id: i.id, quantity: i.quantity, size: i.size }))
      };

      const res = await fetch(`${API_BASE}/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('checkout failed');
      const data = await res.json();

      // update local state from server response
      const ordersRes = await fetch(`${API_BASE}/orders`);
      orders = ordersRes.ok ? (await ordersRes.json()).orders || [] : orders;
      userProfile = data.user_profile || userProfile;
      cart = data.cart || [];

      saveCart();
      updateCartUI();

      alert(`Спасибо за заказ!\n\nНомер заказа: ${data.order.id}\nОбщая сумма: ${formatPrice(data.order.total)}\n\nМы свяжемся с вами в ближайшее время.`);

      document.getElementById('checkoutForm').reset();
      closeCheckoutModal();
      closeSidebars();
      updateProfileUI();
    } catch (err) {
      alert('Не удалось оформить заказ — попробуйте позднее.');
    }
  })();
});

function closeCheckoutModal() {
  checkoutModal.classList.remove('open');
  checkoutModal.setAttribute('aria-hidden', 'true');
}

document.getElementById('closeCheckout').addEventListener('click', closeCheckoutModal);

// Event listeners
document.getElementById('cartBtn').addEventListener('click', () => openSidebar(cartSidebar));
document.getElementById('favoritesBtn').addEventListener('click', () => openSidebar(favoritesSidebar));
document.getElementById('closeCart').addEventListener('click', closeSidebars);
document.getElementById('closeFavorites').addEventListener('click', closeSidebars);
document.getElementById('profileBtn').addEventListener('click', () => {
  updateProfileUI();
  profileModal.classList.add('open');
  profileModal.setAttribute('aria-hidden', 'false');
});
document.getElementById('closeProfile').addEventListener('click', () => {
  profileModal.classList.remove('open');
  profileModal.setAttribute('aria-hidden', 'true');
});

document.getElementById('checkoutBtn').addEventListener('click', () => {
  if (cart.length === 0) {
    alert('Корзина пуста!');
    return;
  }
  // Block checkout if not logged in
  const savedEmail = localStorage.getItem('userEmail') || userProfile.email;
  if (!savedEmail) {
    showLoginModal();
    return;
  }
  closeSidebars();
  
  // Populate checkout form with saved data
  document.getElementById('checkoutName').value = userProfile.name || '';
  document.getElementById('checkoutEmail').value = userProfile.email || '';
  document.getElementById('checkoutPhone').value = userProfile.phone || '';
  document.getElementById('checkoutAddress').value = userProfile.address || '';

  // Update summary
  let subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  document.getElementById('summaryProducts').textContent = formatPrice(subtotal);
  
  const updateSummary = () => {
    const delivery = document.getElementById('deliveryMethod').value;
    const fee = delivery === 'pickup' ? 0 : delivery === 'delivery' ? 500 : 1500;
    document.getElementById('summaryDelivery').textContent = formatPrice(fee);
    document.getElementById('summaryTotal').textContent = formatPrice(subtotal + fee);
  };
  
  updateSummary();
  document.getElementById('deliveryMethod').addEventListener('change', updateSummary);

  checkoutModal.classList.add('open');
  checkoutModal.setAttribute('aria-hidden', 'false');
});

sidebarOverlay.addEventListener('click', closeSidebars);
modal.addEventListener('click', (e) => {
  if (e.target === modal) closeProductModal();
});
profileModal.addEventListener('click', (e) => {
  if (e.target === profileModal) {
    profileModal.classList.remove('open');
    profileModal.setAttribute('aria-hidden', 'true');
  }
});
checkoutModal.addEventListener('click', (e) => {
  if (e.target === checkoutModal) closeCheckoutModal();
});

// Filter and search
document.querySelectorAll('.filter-btn, .filter-chip, .category-card').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetFilter = btn.dataset.filter;
    if (!targetFilter) return;

    document.querySelectorAll('.filter-btn, .filter-chip, .category-card').forEach(b => {
      b.classList.toggle('active', b.dataset.filter === targetFilter);
    });

    currentFilter = targetFilter;
    renderProducts();

    // After applying the filter, scroll to the products list so user sees filtered items
    // Use a short timeout to ensure DOM has been updated by renderProducts
    try {
      setTimeout(() => {
        if (productsRoot && typeof productsRoot.scrollIntoView === 'function') {
          productsRoot.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 80);
    } catch (e) {
      // ignore if scroll fails
    }
  });
});

document.getElementById('priceRange').addEventListener('input', (e) => {
  maxPrice = parseInt(e.target.value);
  document.getElementById('priceLabel').textContent = `0 - ${formatPrice(maxPrice)}`;
  renderProducts();
});

document.getElementById('searchInput').addEventListener('input', renderProducts);

document.querySelectorAll('.profile-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.profile-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.profile-tab-content').forEach(c => c.classList.add('hidden'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab + 'Tab').classList.remove('hidden');
  });
});

document.getElementById('saveProfileBtn').addEventListener('click', () => {
  (async () => {
    const payload = {
      name: document.getElementById('userName').value,
      email: document.getElementById('userEmail').value,
      phone: document.getElementById('userPhone').value,
      address: document.getElementById('userAddress').value
    };
    try {
      const res = await fetch(`${API_BASE}/profile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('profile save failed');
      const data = await res.json();
      userProfile = data.user_profile || payload;
      alert('Данные сохранены!');
    } catch (err) {
      // fallback
      userProfile = payload;
      localStorage.setItem('userProfile', JSON.stringify(userProfile));
      alert('Данные сохранены (локально).');
    }
  })();
});

// Login functions
async function handleLogin(email) {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    if (res.ok) {
      const data = await res.json();
      userProfile.email = data.user_profile.email || email;
      localStorage.setItem('userEmail', email);
      localStorage.setItem('userProfile', JSON.stringify(userProfile));
      document.getElementById('loginModal').classList.remove('open');
      return true;
    }
  } catch (err) {
    console.warn('Login failed, using localStorage:', err);
    localStorage.setItem('userEmail', email);
  }
  return false;
}

async function handleLogout() {
  try {
    const res = await fetch(`${API_BASE}/logout`, { method: 'POST' });
    if (res.ok) {
      localStorage.removeItem('userEmail');
      window.location.reload();
    }
  } catch (err) {
    console.warn('Logout failed:', err);
    localStorage.removeItem('userEmail');
    window.location.reload();
  }
}

function showLoginModal() {
  const loginModal = document.getElementById('loginModal');
  if (loginModal) {
    loginModal.classList.add('open');
  }
}

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value.trim();
  if (email) {
    const success = await handleLogin(email);
    if (!success) {
      alert('Проверьте ваш email и попробуйте ещё раз.');
    }
    document.getElementById('loginEmail').value = '';
  }
});

document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);

// Initialize
(async () => {
  await initState();
  renderProducts();
  updateCartUI();
  updateFavoritesUI();
  updateProfileUI();
  
  // Show login modal if not logged in yet
  const savedEmail = localStorage.getItem('userEmail');
  if (!savedEmail) {
    showLoginModal();
  }
})();
