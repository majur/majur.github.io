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

  function initViewTransitionDirection() {
    const stored = sessionStorage.getItem('vt-direction');
    if (stored === 'next' || stored === 'prev') {
      document.documentElement.classList.add(`vt-dir-${stored}`);
      sessionStorage.removeItem('vt-direction');
    }

    document.addEventListener(
      'click',
      (event) => {
        const link = event.target.closest('a[data-vt-direction]');
        if (!link || link.target === '_blank' || link.origin !== location.origin) return;
        const direction = link.dataset.vtDirection;
        if (direction !== 'next' && direction !== 'prev') return;
        sessionStorage.setItem('vt-direction', direction);
        document.documentElement.classList.add(`vt-dir-${direction}`);
      },
      true
    );
  }

  function init() {
    initViewTransitionDirection();

    const navbar = document.getElementById('navbar');
    if (navbar) {
      window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
      });
    }

    const toggle = document.getElementById('nav-toggle');
    const closeBtn = document.getElementById('nav-close');
    const menu = document.getElementById('nav-menu');
    const backdrop = document.getElementById('nav-backdrop');

    if (!toggle || !menu) return;

    const closeNav = () => {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Otvoriť menu');
      if (backdrop) {
        backdrop.setAttribute('aria-hidden', 'true');
        backdrop.tabIndex = -1;
      }
    };

    const openNav = () => {
      document.body.classList.add('nav-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Zavrieť menu');
      if (backdrop) {
        backdrop.setAttribute('aria-hidden', 'false');
        backdrop.tabIndex = 0;
      }
    };

    toggle.addEventListener('click', (event) => {
      event.stopPropagation();
      if (document.body.classList.contains('nav-open')) {
        closeNav();
      } else {
        openNav();
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        closeNav();
      });
    }

    if (backdrop) {
      backdrop.addEventListener('click', (event) => {
        event.stopPropagation();
        closeNav();
      });
    }

    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeNav);
    });

    window.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeNav();
    });

    window.matchMedia('(min-width: 769px)').addEventListener('change', (event) => {
      if (event.matches) closeNav();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
