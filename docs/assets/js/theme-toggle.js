(function () {
  var STORAGE_KEY = 'theme';
  var root = document.documentElement;
  var button = document.getElementById('theme-toggle');

  if (!button) return;

  function getStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setStored(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {}
  }

  function isDark() {
    return root.getAttribute('data-theme') === 'dark';
  }

  function syncButton() {
    var dark = isDark();
    button.textContent = dark ? '☀️' : '🌙';
    button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  }

  if (!getStored()) {
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  }

  syncButton();

  button.addEventListener('click', function () {
    var next = isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    setStored(next);
    syncButton();
  });
})();
