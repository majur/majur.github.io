(function () {
  const storedTheme = localStorage.getItem('theme');
  const initialTheme = storedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', initialTheme);

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (event) => {
    if (!localStorage.getItem('theme')) {
      document.documentElement.setAttribute('data-theme', event.matches ? 'dark' : 'light');
    }
  });

  window.toggleTheme = function toggleTheme() {
    const html = document.documentElement;
    const nextTheme = html.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', nextTheme);
    localStorage.setItem('theme', nextTheme);
  };

  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }
})();
