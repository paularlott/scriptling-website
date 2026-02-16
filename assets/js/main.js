import FlexSearch from 'flexsearch';
import MeshAnimation from './mesh-animation.js';

class SiteSearch {
  constructor() {
    this.index = null;
    this.documents = [];
    this.searchTimeout = null;
    this.selectedIndex = -1;
    this.results = [];

    this.initElements();
    this.loadSearchIndex();
    this.bindEvents();
  }

  initElements() {
    this.searchBtn = document.getElementById('search-btn');
    this.searchModal = document.getElementById('search-modal');
    this.searchClose = document.getElementById('search-close');
    this.searchInput = document.getElementById('search-input');
    this.searchResults = document.getElementById('search-results');
    this.searchResultsList = document.getElementById('search-results-list');
    this.searchEmpty = document.getElementById('search-empty');
    this.searchBackdrop = this.searchModal.querySelector('.fixed.inset-0.bg-black\\/30');
  }

  async loadSearchIndex() {
    try {
      const response = await fetch('/index.json');
      const data = await response.json();

      this.index = new FlexSearch.Index({
        tokenize: 'forward',
        resolution: 9,
        minlength: 2,
        optimize: true,
        fastupdate: true
      });

      this.documents = data;

      // Index all documents
      data.forEach((doc, i) => {
        const content = `${doc.title} ${doc.content} ${doc.section || ''}`;
        this.index.add(i, content);
      });
    } catch (error) {
      console.error('Error loading search index:', error);
    }
  }

  bindEvents() {
    // Open search
    this.searchBtn.addEventListener('click', () => this.openSearch());

    // Close search
    this.searchClose.addEventListener('click', () => this.closeSearch());
    this.searchBackdrop.addEventListener('click', () => this.closeSearch());

    // Search input
    this.searchInput.addEventListener('input', (e) => this.handleInput(e));
    this.searchInput.addEventListener('keydown', (e) => this.handleKeydown(e));

    // Global keyboard shortcuts
    document.addEventListener('keydown', (e) => this.handleGlobalKeydown(e));
  }

  handleGlobalKeydown(e) {
    // Ctrl+K or Cmd+K to open search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      this.openSearch();
      return;
    }

    // Escape to close
    if (e.key === 'Escape' && !this.searchModal.classList.contains('hidden')) {
      this.closeSearch();
    }
  }

  handleKeydown(e) {
    if (this.results.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.results.length - 1);
        this.updateSelection();
        break;
      case 'ArrowUp':
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
        this.updateSelection();
        break;
      case 'Enter':
        e.preventDefault();
        if (this.selectedIndex >= 0) {
          window.location.href = this.results[this.selectedIndex].item.href;
        }
        break;
    }
  }

  handleInput(e) {
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      this.performSearch(e.target.value);
    }, 150);
  }

  performSearch(query) {
    if (!query.trim() || !this.index) {
      this.hideResults();
      return;
    }

    const searchResults = this.index.search(query, { limit: 8 });
    this.results = searchResults.map(id => ({ item: this.documents[id] }));
    this.selectedIndex = -1;

    if (this.results.length > 0) {
      this.renderResults(query);
    } else {
      this.showEmpty();
    }
  }

  renderResults(query) {
    this.searchResultsList.innerHTML = this.results.map((result, index) => {
      const item = result.item;
      return `
        <a href="${item.href}" class="search-result block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-600 ${index === this.selectedIndex ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700' : ''}" data-index="${index}">
          <div class="flex items-start space-x-3">
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">${this.highlightText(item.title, query)}</h4>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">${this.highlightText(item.content, query)}</p>
              <div class="flex items-center mt-2 text-xs text-gray-400 dark:text-gray-500">
                <span class="capitalize">${item.section || 'Page'}</span>
                <span class="mx-1">•</span>
                <span>${item.date}</span>
              </div>
            </div>
          </div>
        </a>
      `;
    }).join('');

    this.searchResults.classList.remove('hidden');
    this.searchEmpty.classList.add('hidden');
  }

  highlightText(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
    return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800 rounded p-0">$1</mark>');
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
    this.searchModal.classList.remove('hidden');
    this.searchInput.focus();
  }

  closeSearch() {
    this.searchModal.classList.add('hidden');
    this.searchInput.value = '';
    this.hideResults();
  }
}

class MobileMenu {
  constructor() {
    this.initElements();
    this.bindEvents();
  }

  initElements() {
    this.mobileMenuBtn = document.getElementById('mobile-menu-btn');
    this.mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    this.mobileMenuSidebar = document.getElementById('mobile-menu-sidebar');
    this.mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');
    this.mobileMenuClose = document.getElementById('mobile-menu-close');

    this.startX = 0;
    this.currentX = 0;
    this.isDragging = false;
  }

  bindEvents() {
    this.mobileMenuBtn.addEventListener('click', () => this.open());
    this.mobileMenuClose.addEventListener('click', () => this.close());
    this.mobileMenuBackdrop.addEventListener('click', () => this.close());

    // Touch gestures
    this.mobileMenuBackdrop.addEventListener('touchstart', (e) => this.handleTouchStart(e));
    this.mobileMenuBackdrop.addEventListener('touchmove', (e) => this.handleTouchMove(e));
    this.mobileMenuBackdrop.addEventListener('touchend', (e) => this.handleTouchEnd(e));
  }

  open() {
    document.body.style.overflow = 'hidden';
    this.mobileMenuOverlay.classList.remove('hidden');
    requestAnimationFrame(() => {
      this.mobileMenuBackdrop.classList.remove('opacity-0');
      this.mobileMenuBackdrop.classList.add('opacity-100');
      this.mobileMenuSidebar.classList.remove('-translate-x-full');
      this.mobileMenuSidebar.classList.add('translate-x-0');
    });
  }

  close() {
    document.body.style.overflow = '';
    this.mobileMenuBackdrop.classList.remove('opacity-100');
    this.mobileMenuBackdrop.classList.add('opacity-0');
    this.mobileMenuSidebar.classList.remove('translate-x-0');
    this.mobileMenuSidebar.classList.add('-translate-x-full');
    setTimeout(() => {
      this.mobileMenuOverlay.classList.add('hidden');
    }, 300);
  }

  handleTouchStart(e) {
    this.startX = e.touches[0].clientX;
    this.isDragging = true;
  }

  handleTouchMove(e) {
    if (!this.isDragging) return;
    this.currentX = e.touches[0].clientX;
    const diffX = this.currentX - this.startX;

    if (diffX < 0) {
      const translateX = Math.max(diffX, -320);
      this.mobileMenuSidebar.style.transform = `translateX(${translateX}px)`;
    }
  }

  handleTouchEnd(e) {
    if (!this.isDragging) return;
    this.isDragging = false;

    const diffX = this.currentX - this.startX;
    this.mobileMenuSidebar.style.transform = '';

    if (diffX < -80) {
      this.close();
    }
  }
}

class ThemeToggle {
  constructor() {
    this.initElements();
    this.updateTheme();
    this.bindEvents();
  }

  initElements() {
    this.themeToggle = document.getElementById('theme-toggle');
    this.darkIcon = document.getElementById('theme-toggle-dark-icon');
    this.lightIcon = document.getElementById('theme-toggle-light-icon');
  }

  bindEvents() {
    this.themeToggle.addEventListener('click', () => this.toggle());
  }

  updateTheme() {
    // Get the default theme from the window object (will be set by Hugo)
    const defaultTheme = window.siteConfig?.defaultTheme || 'light';

    // Check localStorage first, fall back to default theme if not set
    const theme = localStorage.getItem('theme') || defaultTheme;

    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      this.darkIcon.classList.remove('hidden');
      this.lightIcon.classList.add('hidden');
    } else {
      document.documentElement.classList.remove('dark');
      this.lightIcon.classList.remove('hidden');
      this.darkIcon.classList.add('hidden');
    }
  }

  toggle() {
    if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    }
    this.updateTheme();
  }
}

class ImageModal {
  constructor() {
    this.initElements();
    this.bindEvents();
  }

  initElements() {
    this.imageModal = document.getElementById('image-modal');
    this.imageModalClose = document.getElementById('image-modal-close');
    this.imageModalImg = document.getElementById('image-modal-img');
    this.imageModalCaption = document.getElementById('image-modal-caption');
  }

  bindEvents() {
    this.imageModalClose.addEventListener('click', () => this.close());
    this.imageModal.addEventListener('click', (e) => {
      if (e.target === this.imageModal || e.target.classList.contains('backdrop-blur-sm')) {
        this.close();
      }
    });
    document.addEventListener('keydown', (e) => this.handleKeydown(e));
  }

  handleKeydown(e) {
    if (e.key === 'Escape' && !this.imageModal.classList.contains('hidden')) {
      this.close();
    }
  }

  open(src, alt, caption) {
    this.imageModalImg.src = src;
    this.imageModalImg.alt = alt;
    if (caption) {
      this.imageModalCaption.innerHTML = caption;
      this.imageModalCaption.classList.remove('hidden');
    } else {
      this.imageModalCaption.classList.add('hidden');
    }
    this.imageModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.imageModal.classList.add('hidden');
    document.body.style.overflow = '';
    this.imageModalImg.src = '';
    this.imageModalImg.alt = '';
    this.imageModalCaption.innerHTML = '';
    this.imageModalCaption.classList.add('hidden');
  }
}

// Copy code functionality
function copyCode(button) {
  const codeBlock = button.closest('.group').querySelector('code');
  const text = codeBlock.textContent;

  navigator.clipboard.writeText(text).then(() => {
    const originalSvg = button.innerHTML;
    button.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
    </svg>`;

    setTimeout(() => {
      button.innerHTML = originalSvg;
    }, 2000);
  });
}

// Image modal functionality
let imageModalInstance;
function openImageModal(src, alt, caption) {
  if (imageModalInstance) {
    imageModalInstance.open(src, alt, caption);
  }
}

// Make functions available globally
window.copyCode = copyCode;
window.openImageModal = openImageModal;

function scrollToActiveItem() {
  const sidebarScrollbar = document.querySelector("aside .nav-container");
  const activeItems = document.querySelectorAll(".active-nav-item");
  const visibleActiveItem = Array.from(activeItems).find(function (activeItem) {
    return activeItem.getBoundingClientRect().height > 0;
  });

  if (!visibleActiveItem) {
    return;
  }

  const yOffset = visibleActiveItem.clientHeight;
  const yDistance = visibleActiveItem.getBoundingClientRect().top - sidebarScrollbar.getBoundingClientRect().top;
  sidebarScrollbar.scrollTo({
    behavior: "instant",
    top: yDistance - yOffset
  });
}

// Mesh animation initialization
let heroMeshAnimation = null;

function initHeroMesh() {
  const heroCanvas = document.getElementById('heroMesh');
  if (heroCanvas && window.MeshAnimation) {
    heroMeshAnimation = new window.MeshAnimation('heroMesh');
  }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (heroMeshAnimation) {
    heroMeshAnimation.destroy();
  }
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new SiteSearch();
  new MobileMenu();
  new ThemeToggle();
  imageModalInstance = new ImageModal();

  // Make sure the active menu item is visible
  scrollToActiveItem();

  // Start the mesh animation
  initHeroMesh();

  // Add line numbers to code blocks that have data-linenos="true"
  document.querySelectorAll('code[data-linenos="true"]').forEach(function(code) {
    const lines = code.textContent.split('\n');
    const lineCount = lines.length;

    // Create line numbers
    const lineNumbers = document.createElement('div');
    lineNumbers.className = 'absolute left-0 top-0 p-4 text-gray-400 dark:text-gray-600 text-sm font-mono select-none pointer-events-none';
    lineNumbers.style.width = '3rem';

    for (let i = 1; i <= lineCount; i++) {
      const lineNum = document.createElement('div');
      lineNum.textContent = i;
      lineNumbers.appendChild(lineNum);
    }

    // Add padding to code for line numbers
    code.style.paddingLeft = '3.5rem';
    code.parentElement.style.position = 'relative';
    code.parentElement.appendChild(lineNumbers);
  });
});

// Tabs functionality
function showTab(tabsId, activeIndex, totalTabs) {
  const wrapper = document.querySelector(`[data-tabs-id="${tabsId}"]`);
  const buttons = wrapper.querySelectorAll('.tab-btn');

  for (let i = 0; i < totalTabs; i++) {
    const tabContent = document.getElementById(`${tabsId}-${i}`);
    const tabButton = buttons[i];

    if (i === activeIndex) {
      tabContent.classList.remove('hidden');
      tabButton.classList.remove('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-200', 'hover:bg-gray-100', 'dark:hover:bg-gray-700');
      tabButton.classList.add('bg-white', 'dark:bg-gray-900', 'text-blue-600', 'dark:text-blue-400', 'border-b-2', 'border-blue-600', 'dark:border-blue-400');
    } else {
      tabContent.classList.add('hidden');
      tabButton.classList.remove('bg-white', 'dark:bg-gray-900', 'text-blue-600', 'dark:text-blue-400', 'border-b-2', 'border-blue-600', 'dark:border-blue-400');
      tabButton.classList.add('text-gray-600', 'dark:text-gray-400', 'hover:text-gray-900', 'dark:hover:text-gray-200', 'hover:bg-gray-100', 'dark:hover:bg-gray-700');
    }
  }
}

window.showTab = showTab;
