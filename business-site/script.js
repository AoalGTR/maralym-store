const cards = document.querySelectorAll('.card');
const bars = document.querySelectorAll('.bar-track span');
const links = document.querySelectorAll('.top-nav a, .cta a');
const openFinancialPanelBtn = document.getElementById('open-financial-panel');
const closeFinancialPanelBtn = document.getElementById('close-financial-panel');
const financialPanel = document.getElementById('financial-panel');
const panelOverlay = document.getElementById('panel-overlay');

cards.forEach((card, index) => {
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'translateY(-3px)';
    card.style.transition = 'transform 180ms ease';
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0)';
  });

  card.style.animationDelay = `${80 + index * 90}ms`;
});

bars.forEach((bar) => {
  const target = bar.style.width;
  bar.style.width = '0';
  setTimeout(() => {
    bar.style.transition = 'width 900ms ease';
    bar.style.width = target;
  }, 220);
});

links.forEach((link) => {
  link.addEventListener('click', (event) => {
    const href = link.getAttribute('href');
    if (!href || !href.startsWith('#')) {
      return;
    }

    const target = document.querySelector(href);
    if (!target) {
      return;
    }

    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

function openFinancialPanel() {
  if (!financialPanel) {
    return;
  }

  financialPanel.classList.add('is-open');
  financialPanel.setAttribute('aria-hidden', 'false');
  if (panelOverlay) {
    panelOverlay.classList.add('is-open');
    panelOverlay.setAttribute('aria-hidden', 'false');
  }
  document.body.style.overflow = 'hidden';
  if (closeFinancialPanelBtn) {
    closeFinancialPanelBtn.focus();
  }
}

function closeFinancialPanel() {
  if (!financialPanel) {
    return;
  }

  financialPanel.classList.remove('is-open');
  financialPanel.setAttribute('aria-hidden', 'true');
  if (panelOverlay) {
    panelOverlay.classList.remove('is-open');
    panelOverlay.setAttribute('aria-hidden', 'true');
  }
  document.body.style.overflow = '';
}

if (openFinancialPanelBtn) {
  openFinancialPanelBtn.addEventListener('click', openFinancialPanel);
}

if (closeFinancialPanelBtn) {
  closeFinancialPanelBtn.addEventListener('click', closeFinancialPanel);
}

if (panelOverlay) {
  panelOverlay.addEventListener('click', closeFinancialPanel);
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeFinancialPanel();
  }
});
