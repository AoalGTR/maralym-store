// Allow overriding API base for production hosts by setting `window.MARALYM_API_BASE`
const API_BASE = (window.MARALYM_API_BASE && window.MARALYM_API_BASE.replace(/\/$/, '')) || (window.location.origin.replace(/:\d+$/, '') + '/api');
let ADMIN_KEY = null;
const DEFAULT_SIZES = ['XS', 'S', 'M', 'L'];

// Resolve backend-served image paths to absolute URLs
function resolveImageUrl(img) {
  if (!img) return '';
  if (img.startsWith('http://') || img.startsWith('https://')) return img;
  if (img.startsWith('/')) return API_BASE.replace(/\/api$/, '') + img;
  return img;
}

// Show toast notification
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// Auto-fill tags with default sizes
const tagsInput = document.getElementById('tags');
if (tagsInput && !tagsInput.value.trim()) {
  tagsInput.value = DEFAULT_SIZES.join(', ');
}

function authHeaders() {
  return { 'Content-Type': 'application/json', 'x-admin-key': ADMIN_KEY };
}

// Handle login
document.getElementById('loginForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const key = document.getElementById('adminKey').value.trim();
  if (!key) {
    showToast('Введите admin key', 'error');
    return;
  }
  ADMIN_KEY = key;
  document.getElementById('loginSection').classList.add('hidden');
  document.getElementById('adminArea').classList.remove('hidden');
  loadProducts();
});

// Load and display products
async function loadProducts() {
  try {
    const res = await fetch(API_BASE + '/admin/products', { headers: { 'x-admin-key': ADMIN_KEY } });
    if (!res.ok) {
      showToast('Ошибка аутентификации', 'error');
      return;
    }
    
    const data = await res.json();
    const root = document.getElementById('productsList');
    const countEl = document.getElementById('productCount');
    
    countEl.textContent = data.items.length;
    
    if (data.items.length === 0) {
      root.innerHTML = '<div class="empty-state">🛍️ Товары будут отображаться здесь</div>';
      return;
    }
    
    root.innerHTML = '';
    data.items.forEach(p => {
      const card = document.createElement('div');
      card.className = 'product-card';
      const imgSrc = resolveImageUrl(p.image) || (API_BASE.replace(/\/api$/, '') + '/static/uploads/placeholder.png');
      card.innerHTML = `
        <img src="${imgSrc}" alt="${p.name}">
        <div class="product-info">
          <p class="product-name">${p.name}</p>
          <div class="product-meta">
            <span>📁 ${p.category}</span>
            <span>💰 ${p.price.toLocaleString('ru-RU')} сом</span>
            <span>⭐ ${p.rating || 0}</span>
          </div>
          <small>${p.description || 'Нет описания'}</small>
        </div>
        <div class="product-actions">
          <button class="btn btn-danger delete-btn" data-id="${p.id}">🗑️ Удалить</button>
        </div>
      `;
      root.appendChild(card);
    });

    // Attach delete handlers
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const id = e.target.dataset.id;
        if (confirm('⚠️ Вы уверены? Этот товар будет удален.')) {
          await deleteProduct(id);
        }
      });
    });
  } catch (err) {
    showToast('Ошибка загрузки товаров: ' + err.message, 'error');
  }
}

// Delete product
async function deleteProduct(id) {
  try {
    const res = await fetch(API_BASE + '/admin/products/' + id, {
      method: 'DELETE',
      headers: { 'x-admin-key': ADMIN_KEY }
    });
    
    if (res.ok) {
      showToast('✅ Товар удален', 'success');
      loadProducts();
    } else {
      showToast('Ошибка удаления товара', 'error');
    }
  } catch (err) {
    showToast('Ошибка: ' + err.message, 'error');
  }
}

// Handle image file selection preview
const fileUpload = document.querySelector('.file-upload');
const fileInput = document.getElementById('imageFile');

// Click on the upload area to open file dialog
if (fileUpload && fileInput) {
  fileUpload.addEventListener('click', () => {
    fileInput.click();
  });

  // Drag and drop support
  fileUpload.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = '#667eea';
    fileUpload.style.background = '#f8f9ff';
  });

  fileUpload.addEventListener('dragleave', () => {
    fileUpload.style.borderColor = '#e0e0e0';
    fileUpload.style.background = 'transparent';
  });

  fileUpload.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = '#e0e0e0';
    fileUpload.style.background = 'transparent';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      fileInput.files = files;
      const event = new Event('change', { bubbles: true });
      fileInput.dispatchEvent(event);
    }
  });
}

document.getElementById('imageFile').addEventListener('change', (e) => {
  const file = e.target.files[0];
  const preview = document.getElementById('imagePreview');
  
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      preview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
  } else {
    preview.innerHTML = '';
  }
});

// Handle form submission
document.getElementById('createForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const name = document.getElementById('name').value.trim();
  const category = document.getElementById('category').value.trim();
  const price = Number(document.getElementById('price').value);
  const badge = document.getElementById('badge').value.trim();
  const rating = Number(document.getElementById('rating').value) || 4.5;
  const tags = document.getElementById('tags').value
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);
  const description = document.getElementById('description').value.trim();
  const file = document.getElementById('imageFile').files[0];

  // Validate
  if (!name || !category || !price) {
    showToast('Заполните обязательные поля', 'error');
    return;
  }

  try {
    let imageUrl = '';
    
    // Upload image if provided
    if (file) {
      const fd = new FormData();
      fd.append('file', file);
      const uploadRes = await fetch(API_BASE + '/admin/upload-image', {
        method: 'POST',
        body: fd,
        headers: { 'x-admin-key': ADMIN_KEY }
      });
      
      if (!uploadRes.ok) {
        showToast('Ошибка загрузки изображения', 'error');
        return;
      }
      
      const uploadData = await uploadRes.json();
      imageUrl = uploadData.url;
    }

    // Create product
    const payload = {
      name,
      category,
      price,
      badge: badge || null,
      tags: tags.length ? tags : DEFAULT_SIZES,
      description: description || '',
      image: imageUrl || null,
      rating
    };

    const createRes = await fetch(API_BASE + '/admin/products', {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(payload)
    });

    if (createRes.ok) {
      showToast('✅ Товар успешно создан!', 'success');
      document.getElementById('createForm').reset();
      document.getElementById('imagePreview').innerHTML = '';
      if (tagsInput) tagsInput.value = DEFAULT_SIZES.join(', ');
      loadProducts();
    } else {
      const error = await createRes.json();
      showToast('Ошибка создания: ' + (error.detail || 'неизвестная ошибка'), 'error');
    }
  } catch (err) {
    showToast('Ошибка: ' + err.message, 'error');
  }
});

// Handle logout
document.getElementById('logoutBtn').addEventListener('click', () => {
  ADMIN_KEY = null;
  document.getElementById('adminArea').classList.add('hidden');
  document.getElementById('loginSection').classList.remove('hidden');
  document.getElementById('adminKey').value = '';
  document.getElementById('createForm').reset();
  showToast('Вы вышли', 'success');
});
