import FlexSearch from 'flexsearch';

// Field weights: a hit in a page title or section heading means the result is
// about the query, a hit in body text only that it mentions it.
const WEIGHTS = { title: 12, heading: 8, keywords: 4, content: 1.5 };
const MAX_RESULTS = 15;
const MAX_PER_PAGE = 3;
const LOW_PRIORITY = 0.3; // changelog pages

const escapeHTML = (s) => s.replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[c]));

const newIndex = () => new FlexSearch.Index({
  tokenize: 'forward',
  resolution: 9,
  minlength: 1,
  optimize: true,
});

export default class SiteSearch {
  constructor() {
    this.records = [];
    this.indexes = null;
    this.loading = null;
    this.searchTimeout = null;
    this.selectedIndex = -1;
    this.results = [];

    this.initElements();
    this.bindEvents();
  }

  initElements() {
    this.searchBtns = document.querySelectorAll('[data-search-open], #search-btn');
    this.searchModal = document.getElementById('search-modal');
    this.searchClose = document.getElementById('search-close');
    this.searchInput = document.getElementById('search-input');
    this.searchResults = document.getElementById('search-results');
    this.searchResultsList = document.getElementById('search-results-list');
    this.searchEmpty = document.getElementById('search-empty');
    this.searchLoading = document.getElementById('search-loading');
    this.searchBackdrop = this.searchModal.querySelector('.fixed.inset-0.bg-black\\/30');
  }

  // The index is ~1.7 MB, so it is fetched on first use (or when the pointer
  // heads for the search button) rather than on every page view.
  ensureIndex() {
    if (!this.loading) {
      this.loading = fetch('/index.json')
        .then((r) => r.json())
        .then((records) => this.buildIndex(records))
        .catch((error) => {
          this.loading = null;
          console.error('Error loading search index:', error);
        });
    }
    return this.loading;
  }

  buildIndex(records) {
    const indexes = { title: newIndex(), heading: newIndex(), keywords: newIndex(), content: newIndex() };
    records.forEach((r, i) => {
      if (r.h) {
        indexes.heading.add(i, r.h);
      } else {
        indexes.title.add(i, r.t);
        const keywords = [r.d, r.k].filter(Boolean).join(' ');
        if (keywords) indexes.keywords.add(i, keywords);
      }
      if (r.c) indexes.content.add(i, r.c);
    });
    this.records = records;
    this.indexes = indexes;
  }

  bindEvents() {
    this.searchBtns.forEach((btn) => {
      btn.addEventListener('click', () => this.openSearch());
      btn.addEventListener('pointerenter', () => this.ensureIndex(), { once: true });
      btn.addEventListener('focus', () => this.ensureIndex(), { once: true });
    });

    this.searchClose.addEventListener('click', () => this.closeSearch());
    this.searchBackdrop.addEventListener('click', () => this.closeSearch());

    this.searchInput.addEventListener('input', (e) => this.handleInput(e));
    this.searchInput.addEventListener('keydown', (e) => this.handleKeydown(e));

    document.addEventListener('keydown', (e) => {
      const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName) ||
        document.activeElement?.isContentEditable;
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.openSearch();
      } else if (e.key === '/' && !typing && this.searchModal.classList.contains('hidden')) {
        e.preventDefault();
        this.openSearch();
      } else if (e.key === 'Escape' && !this.searchModal.classList.contains('hidden')) {
        this.closeSearch();
      }
    });
  }

  handleKeydown(e) {
    if (!this.results.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      this.selectedIndex = Math.min(this.selectedIndex + 1, this.results.length - 1);
      this.updateSelection();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
      this.updateSelection();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      this.go(this.results[Math.max(this.selectedIndex, 0)]);
    }
  }

  go(record) {
    this.closeSearch();
    window.location.href = record.u;
  }

  handleInput(e) {
    clearTimeout(this.searchTimeout);
    const query = e.target.value;
    this.searchTimeout = setTimeout(() => this.performSearch(query), 120);
  }

  async performSearch(query) {
    if (!query.trim()) {
      this.hideResults();
      return;
    }
    if (!this.indexes) {
      this.searchLoading?.classList.remove('hidden');
      await this.ensureIndex();
      this.searchLoading?.classList.add('hidden');
      // The user may have kept typing while the index loaded.
      if (query !== this.searchInput.value || !this.indexes) return;
    }

    this.results = this.rank(query);
    this.selectedIndex = this.results.length ? 0 : -1;
    if (this.results.length > 0) {
      this.renderResults(query);
    } else {
      this.showEmpty();
    }
  }

  rank(query) {
    const q = query.trim().toLowerCase();
    // "runtime.background" should find the background() heading on the
    // runtime page; the last dotted segment is the name being looked for.
    const lastSegment = q.split('.').pop();
    const scores = new Map();
    const add = (id, value) => scores.set(id, (scores.get(id) || 0) + value);

    for (const [field, weight] of Object.entries(WEIGHTS)) {
      const ids = this.indexes[field].search(q, { limit: 400 });
      ids.forEach((id, rank) => add(id, weight / (1 + rank * 0.05)));
    }

    // FlexSearch ranks by where a word appears, not how often. Reward
    // sections that use the query as a whole word repeatedly, so the section
    // documenting sorted() beats one that mentions sort_keys once.
    const wordRes = q.split(/[^a-z0-9_]+/).filter((t) => t.length > 1)
      .map((t) => new RegExp(`\\b${t}\\b`, 'gi'));

    for (const id of scores.keys()) {
      const r = this.records[id];
      const title = r.t.toLowerCase();
      if (r.c) {
        for (const re of wordRes) {
          add(id, Math.min((r.c.match(re) || []).length, 6) * 1.5);
        }
      }
      if (!r.h) {
        // Exact page or library name: "json", "kv" for scriptling.runtime.kv.
        if (title === q || title.endsWith('.' + q)) add(id, 25);
        // Exact curated tag: "regex" for the re page, "len" for builtins.
        else if (r.k && r.k.toLowerCase().split(' ').includes(q)) add(id, 20);
      } else {
        const name = r.h.split('(')[0].trim().toLowerCase();
        const bare = name.split('.').pop();
        if (name === q || (bare === lastSegment && (q === lastSegment || title.includes(q.slice(0, -lastSegment.length - 1))))) {
          add(id, 18);
        } else if (name.startsWith(q) || bare.startsWith(lastSegment)) {
          // A long query that a heading starts with ("f-string" for
          // "F-Strings") is a strong match; a short one ("del") is not.
          add(id, q.length >= 5 ? 12 : 5);
        }
      }
      if (r.x) scores.set(id, scores.get(id) * LOW_PRIORITY);
    }

    const perPage = new Map();
    const out = [];
    for (const [id] of [...scores.entries()].sort((a, b) => b[1] - a[1])) {
      const r = this.records[id];
      const page = r.u.split('#')[0];
      const n = perPage.get(page) || 0;
      if (n >= MAX_PER_PAGE) continue;
      perPage.set(page, n + 1);
      out.push(r);
      if (out.length >= MAX_RESULTS) break;
    }
    return out;
  }

  snippet(r, query) {
    const text = r.c || '';
    const terms = query.toLowerCase().split(/[^a-z0-9_]+/).filter((t) => t.length > 1);
    const lower = text.toLowerCase();
    let at = -1;
    for (const t of terms) {
      at = lower.indexOf(t);
      if (at >= 0) break;
    }
    if (at < 0) return r.d || text.slice(0, 160);
    const start = Math.max(0, at - 60);
    return (start > 0 ? '…' : '') + text.slice(start, start + 180) + (start + 180 < text.length ? '…' : '');
  }

  renderResults(query) {
    this.searchResultsList.innerHTML = this.results.map((r, index) => {
      const heading = r.h
        ? `${this.highlight(r.h, query)} <span class="font-normal text-gray-500 dark:text-gray-400">· ${escapeHTML(r.t)}</span>`
        : this.highlight(r.t, query);
      return `
        <a href="${escapeHTML(r.u)}" class="search-result block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-600 ${index === this.selectedIndex ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700' : ''}" data-index="${index}">
          <div class="text-xs text-gray-400 dark:text-gray-500 truncate">${escapeHTML(r.p || '')}</div>
          <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate mt-0.5">${heading}</h4>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">${this.highlight(this.snippet(r, query), query)}</p>
        </a>
      `;
    }).join('');

    this.searchResultsList.querySelectorAll('.search-result').forEach((a) => {
      a.addEventListener('click', () => this.closeSearch());
    });

    this.searchResults.classList.remove('hidden');
    this.searchEmpty.classList.add('hidden');
  }

  highlight(text, query) {
    const safe = escapeHTML(text);
    const terms = query.trim().split(/[^A-Za-z0-9_]+/).filter((t) => t.length > 1)
      .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    if (!terms.length) return safe;
    const regex = new RegExp(`(${terms.join('|')})`, 'gi');
    return safe.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800 rounded p-0">$1</mark>');
  }

  updateSelection() {
    const items = this.searchResultsList.querySelectorAll('.search-result');
    items.forEach((item, index) => {
      if (index === this.selectedIndex) {
        item.classList.add('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-200', 'dark:border-blue-700');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-200', 'dark:border-blue-700');
      }
    });
  }

  showEmpty() {
    this.searchResults.classList.add('hidden');
    this.searchEmpty.classList.remove('hidden');
  }

  hideResults() {
    this.searchResults.classList.add('hidden');
    this.searchEmpty.classList.add('hidden');
    this.selectedIndex = -1;
    this.results = [];
  }

  openSearch() {
    this.ensureIndex();
    this.searchModal.classList.remove('hidden');
    this.searchInput.focus();
  }

  closeSearch() {
    this.searchModal.classList.add('hidden');
    this.searchInput.value = '';
    this.hideResults();
  }
}
