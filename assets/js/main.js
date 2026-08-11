(() => {
  const header = document.querySelector('[data-header]');
  const nav = document.querySelector('[data-nav]');
  const menuButton = document.querySelector('[data-menu-button]');

  const updateHeader = () => {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  if (menuButton && nav) {
    const closeMenu = () => {
      nav.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    };

    menuButton.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
    });

    nav.addEventListener('click', (event) => {
      if (event.target instanceof HTMLAnchorElement) closeMenu();
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 980) closeMenu();
    });
  }

  const accessibilityToggle = document.querySelector('[data-accessibility-toggle]');
  const accessibilityMenu = document.querySelector('[data-accessibility-menu]');

  if (accessibilityToggle instanceof HTMLButtonElement && accessibilityMenu instanceof HTMLElement) {
    const closeAccessibilityMenu = () => {
      accessibilityMenu.hidden = true;
      accessibilityToggle.setAttribute('aria-expanded', 'false');
    };

    accessibilityToggle.addEventListener('click', () => {
      const willOpen = accessibilityMenu.hidden;
      accessibilityMenu.hidden = !willOpen;
      accessibilityToggle.setAttribute('aria-expanded', String(willOpen));
      if (willOpen) accessibilityMenu.querySelector('button')?.focus();
    });

    accessibilityMenu.addEventListener('click', (event) => {
      const actionButton = event.target instanceof Element
        ? event.target.closest('[data-accessibility-action]')
        : null;
      if (!(actionButton instanceof HTMLButtonElement)) return;

      const action = actionButton.dataset.accessibilityAction;
      if (action === 'reset') {
        document.documentElement.classList.remove('accessibility-text', 'accessibility-contrast', 'accessibility-links', 'accessibility-motion');
        return;
      }
      if (action) document.documentElement.classList.toggle(`accessibility-${action}`);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !accessibilityMenu.hidden) {
        closeAccessibilityMenu();
        accessibilityToggle.focus();
      }
    });
  }
})();
