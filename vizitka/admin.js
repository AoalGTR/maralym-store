// Allow overriding API base for production hosts by setting `window.MARALYM_API_BASE`
const API_BASE = (window.MARALYM_API_BASE && window.MARALYM_API_BASE.replace(/\/$/, '')) || (window.location.origin.replace(/:\d+$/, '') + '/api');
let ADMIN_KEY = null;

function authHeaders(){
  return { 'Content-Type': 'application/json', 'x-admin-key': ADMIN_KEY };
}

document.getElementById('btnAuth').addEventListener('click', ()=>{
  const v = document.getElementById('adminKey').value.trim();
  if(!v) return alert('Введите admin key');
  ADMIN_KEY = v;
  loadProducts();
  document.getElementById('adminArea').classList.remove('hidden');
});

async function loadProducts(){
  const res = await fetch(API_BASE + '/admin/products', { headers: { 'x-admin-key': ADMIN_KEY } });
  if(!res.ok) return alert('Auth failed or cannot load products');
  const data = await res.json();
  const root = document.getElementById('productsList');
  root.innerHTML = '';
  data.items.forEach(p => {
    const div = document.createElement('div');
    div.className = 'product-row';
    div.innerHTML = `
      <img src="${p.image || '/static/uploads/placeholder.png'}" alt="">
      <div class="meta">
        <strong>${p.name}</strong>
        <div>${p.category} — ${p.price} сом</div>
      </div>
      <div>
        <button data-id="${p.id}" class="edit">Редактировать</button>
        <button data-id="${p.id}" class="del">Удалить</button>
      </div>
    `;
    root.appendChild(div);
  });

  document.querySelectorAll('.del').forEach(b=>b.addEventListener('click', async (e)=>{
    const id = e.target.dataset.id;
    if(!confirm('Удалить товар?')) return;
    const res = await fetch(API_BASE + '/admin/products/' + id, { method:'DELETE', headers:{'x-admin-key': ADMIN_KEY} });
    if(res.ok) loadProducts(); else alert('Delete failed');
  }));
}

document.getElementById('createForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const category = document.getElementById('category').value.trim();
  const price = Number(document.getElementById('price').value);
  const badge = document.getElementById('badge').value.trim();
  const tags = document.getElementById('tags').value.split(',').map(s=>s.trim()).filter(Boolean);
  const description = document.getElementById('description').value.trim();
  const file = document.getElementById('imageFile').files[0];

  let imageUrl = '';
  if(file){
    const fd = new FormData(); fd.append('file', file);
    const up = await fetch(API_BASE + '/admin/upload-image', { method:'POST', body: fd, headers: {'x-admin-key': ADMIN_KEY} });
    if(up.ok){ const u = await up.json(); imageUrl = u.url; } else { alert('Upload failed'); return; }
  }

  const payload = { name, category, price, badge, tags, description, image: imageUrl };
  const res = await fetch(API_BASE + '/admin/products', { method:'POST', headers: authHeaders(), body: JSON.stringify(payload) });
  if(res.ok){ alert('Created'); document.getElementById('createForm').reset(); loadProducts(); } else { alert('Create failed'); }
});
