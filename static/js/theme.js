(function () {
  const root = document.documentElement;
  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = stored || (prefersDark ? 'dark' : 'light');
  root.setAttribute('data-theme', initial);

  const toggle = document.querySelector('[data-theme-toggle]');
  if (!toggle) return;

  const updateLabel = () => {
    toggle.textContent = root.getAttribute('data-theme') === 'dark' ? 'Светлая тема' : 'Темная тема';
  };

  updateLabel();

  toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateLabel();
  });
})();
