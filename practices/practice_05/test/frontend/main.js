// Утилита запроса JSON
async function fetchJSON(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`${path} -> ${r.status}`);
  return await r.json();
}

// Загрузка статуса (health/ready/store)
async function loadStatus() {
  try {
    const health = await fetchJSON('/health');
    document.getElementById('health').textContent = `Health: ${health.status}`;
    document.getElementById('health').className = health.status === 'ok' ? 'ok' : 'warn';
  } catch (e) {
    document.getElementById('health').textContent = 'Health: error';
    document.getElementById('health').className = 'warn';
  }
  try {
    const ready = await fetchJSON('/ready');
    document.getElementById('ready').textContent = `Ready: ${ready.ready ? 'yes' : 'no'}`;
    document.getElementById('ready').className = ready.ready ? 'ok' : 'warn';
  } catch (e) {
    document.getElementById('ready').textContent = 'Ready: error';
    document.getElementById('ready').className = 'warn';
  }
  try {
    const st = await fetchJSON('/api/store/status');
    const text = st.open ? 'Открыто' : 'Закрыто';
    document.getElementById('store').textContent = `${text} · до ${new Date(st.next_change).toLocaleTimeString()}`;
  } catch (e) {
    document.getElementById('store').textContent = 'Не удалось получить статус';
  }
}

// Загрузка меню
async function loadMenu() {
  const grid = document.getElementById('menu-grid');
  const empty = document.getElementById('menu-empty');
  if (!grid) return;
  grid.innerHTML = '';
  try {
    const items = await fetchJSON('/api/v1/menu/');
    if (items.length === 0) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    for (const it of items) {
      const card = document.createElement('div');
      card.className = 'card';
      const sizes = (it.sizes || []).join(', ') || 'n/a';
      const ingr = (it.ingredients || []).join(', ') || 'n/a';
      card.innerHTML = `
        <div class="title">${it.name}</div>
        <div class="meta">${sizes}</div>
        <div class="meta">${ingr}</div>
        <div class="price"><strong>${it.priceCoffeeCoin} CoffeeCoin</strong> · ${it.calories||0} ккал</div>
      `;
      grid.appendChild(card);
    }
  } catch (e) {
    grid.innerHTML = '<div class="warn">Не удалось загрузить меню</div>';
  }
}

// Загрузка новостей
async function loadNews() {
  const ul = document.getElementById('news-list');
  if (!ul) return;
  ul.innerHTML = '';
  try {
    const items = await fetchJSON('/api/v1/news/');
    if (items.length === 0) {
      ul.innerHTML = '<li><em>Новостей пока нет</em></li>';
      return;
    }
    for (const n of items) {
      const li = document.createElement('li');
      li.textContent = `${new Date(n.createdAt).toLocaleString()}: ${n.title}`;
      ul.appendChild(li);
    }
  } catch (e) {
    ul.innerHTML = '<li class="warn">Не удалось загрузить новости</li>';
  }
}

// Загрузка текущей скидки
async function loadDiscount() {
  const el = document.getElementById('discount');
  if (!el) return;
  try {
    const d = await fetchJSON('/api/v1/discounts/current');
    el.textContent = `Скидка: ${d.percent}%`;
  } catch (e) {
    el.textContent = 'Скидка: ошибка';
  }
}

// Быстрый сид демо-меню
async function seedDemoMenu() {
  try {
    const items = [
      { name: 'Эспрессо', ingredients: ['кофе'], sizes: ['single'], priceCoffeeCoin: 3.0, calories: 5 },
      { name: 'Капучино', ingredients: ['кофе','молоко'], sizes: ['tall'], priceCoffeeCoin: 4.5, calories: 120 },
      { name: 'Латте', ingredients: ['кофе','молоко'], sizes: ['tall'], priceCoffeeCoin: 4.8, calories: 150 },
    ];
    for (const it of items) {
      await fetch('/api/v1/menu/', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(it)});
    }
    await loadMenu();
    await fillOrderSelect();
  } catch {}
}

// Наполнение селекта заказов
async function fillOrderSelect() {
  const sel = document.getElementById('order-item');
  if (!sel) return;
  sel.innerHTML = '';
  const items = await fetchJSON('/api/v1/menu/');
  for (const it of items) {
    const opt = document.createElement('option');
    opt.value = it.id;
    opt.textContent = `${it.name} — ${it.priceCoffeeCoin}`;
    sel.appendChild(opt);
  }
}

// Создание заказа
async function createOrder() {
  const sel = document.getElementById('order-item');
  const qty = document.getElementById('order-qty');
  const res = document.getElementById('order-result');
  const pay = document.getElementById('btn-pay');
  try {
    const payload = { items: [{ menuId: Number(sel.value), quantity: Number(qty.value) }] };
    const r = await fetch('/api/v1/orders/', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail||'Ошибка заказа');
    res.textContent = `Заказ #${data.id}: ${data.totalCoffeeCoin} CoffeeCoin (скидка ${data.discountPercent}%)`;
    pay.disabled = false;
    pay.dataset.orderId = data.id;
  } catch (e) {
    res.textContent = e.message || 'Ошибка';
  }
}

// Оплата заказа
async function payOrder() {
  const pay = document.getElementById('btn-pay');
  const res = document.getElementById('order-result');
  const oid = pay.dataset.orderId;
  if (!oid) return;
  const r = await fetch(`/api/v1/orders/${oid}/pay`, { method:'POST' });
  const data = await r.json();
  if (r.ok) res.textContent = `Заказ #${data.id} оплачен`;
}

window.addEventListener('DOMContentLoaded', async () => {
  await loadStatus();
  await loadMenu();
  await loadNews();
  await loadDiscount();
  await fillOrderSelect();
  document.getElementById('btn-refresh')?.addEventListener('click', loadMenu);
  document.getElementById('btn-seed')?.addEventListener('click', seedDemoMenu);
  document.getElementById('btn-order')?.addEventListener('click', createOrder);
  document.getElementById('btn-pay')?.addEventListener('click', payOrder);
});
