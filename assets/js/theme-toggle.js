// Day / moonlit-night theme switcher (follows the OS until the visitor picks one).
// The saved choice is applied before first paint by an inline snippet in <head>.

const STORAGE_KEY = 'theme-preference';

function getSystemTheme() {
  if (typeof window === 'undefined') return 'dark';
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

function getStoredTheme() {
  if (typeof localStorage === 'undefined') return null;
  return localStorage.getItem(STORAGE_KEY);
}

function applyTheme(theme) {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;

  if (theme === 'light') {
    root.setAttribute('data-theme', 'light');
  } else if (theme === 'dark') {
    root.setAttribute('data-theme', 'dark');
  } else {
    root.removeAttribute('data-theme');
  }

  updateToggleUI(theme || getSystemTheme());
}

function updateToggleUI(currentTheme) {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  const isLight = currentTheme === 'light';
  toggleBtn.setAttribute('aria-label', isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode');
  toggleBtn.setAttribute('title', isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode');

  // Sun icon for switching to light, Moon icon for switching to dark
  toggleBtn.innerHTML = isLight
    ? `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`
    : `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
}

function toggleTheme() {
  const stored = getStoredTheme();
  const current = stored || getSystemTheme();
  const next = current === 'light' ? 'dark' : 'light';

  try {
    localStorage.setItem(STORAGE_KEY, next);
  } catch (e) {
    // Ignore localStorage errors
  }

  applyTheme(next);
}

function initTheme() {
  if (typeof window === 'undefined') return;

  // 1. Initial theme application
  const saved = getStoredTheme();
  applyTheme(saved);

  // 2. Listen to system preference changes if no manual override
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
      if (!getStoredTheme()) {
        applyTheme(e.matches ? 'light' : 'dark');
      }
    });
  }

  // 3. Attach click handler
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleTheme);
  }
}

// Auto init if in browser
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
}

// Universal export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getSystemTheme,
    getStoredTheme,
    applyTheme,
    toggleTheme,
    initTheme
  };
}
