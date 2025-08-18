function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('menuToggle');
  const menu = document.getElementById('mobileMenu');
  toggle && toggle.addEventListener('click', () => menu.classList.toggle('hidden'));

  const input = document.getElementById('nav-search');
  const results = document.getElementById('nav-search-results');

  const render = (items) => {
    if (!results) return;
    if (!items.length) {
      results.classList.add('hidden');
      results.innerHTML = '';
      return;
    }
    const q = input.value.trim();
    results.innerHTML = items
      .map(p => `<li><a href="/products/${p.slug}/" class="block px-2 py-1 hover:bg-gray-100">${p.name}</a></li>`)
      .join('') + `<li><a href="/products/?q=${encodeURIComponent(q)}" class="block px-2 py-1 text-blue-600">See all results</a></li>`;
    results.classList.remove('hidden');
  };

  const fetchResults = debounce(async () => {
    if (!input) return;
    const q = input.value.trim();
    if (!q) { render([]); return; }
    try {
      const resp = await fetch(`/api/products/?q=${encodeURIComponent(q)}`);
      const data = await resp.json();
      render(data.results ? data.results.slice(0,5) : []);
    } catch (e) {
      render([]);
    }
  }, 300);

  input && input.addEventListener('input', fetchResults);
});
