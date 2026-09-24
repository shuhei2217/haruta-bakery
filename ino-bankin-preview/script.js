const menuBtn = document.querySelector('.menu-button');
const drawer = document.querySelector('.drawer');
const drawerClose = document.querySelector('.drawer-close');

function setDrawer(open){
  if (!drawer || !menuBtn) return;
  drawer.classList.toggle('open', open);
  drawer.setAttribute('aria-hidden', String(!open));
  menuBtn.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
}

if (menuBtn) {
  menuBtn.addEventListener('click', () => setDrawer(!drawer?.classList.contains('open')));
}
if (drawerClose) {
  drawerClose.addEventListener('click', () => setDrawer(false));
}
if (drawer) {
  drawer.addEventListener('click', e => { if (e.target === drawer) setDrawer(false); });
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setDrawer(false)));
}

// Content visibility must never depend on animation or IntersectionObserver.
// Keep every section readable even if JavaScript or browser timing behaves differently.
document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));


const servicePanels = [...document.querySelectorAll('[data-service]')];
const serviceVisuals = [...document.querySelectorAll('[data-service-visual]')];

function activateService(name){
  if (!name) return;
  serviceVisuals.forEach(el => {
    el.classList.toggle('is-active', el.dataset.serviceVisual === name);
  });
}

if (servicePanels.length && serviceVisuals.length && 'IntersectionObserver' in window) {
  const serviceObserver = new IntersectionObserver(entries => {
    const visible = entries
      .filter(entry => entry.isIntersecting)
      .sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) activateService(visible.target.dataset.service);
  }, {
    threshold: [0.2, 0.45, 0.7],
    rootMargin: '-18% 0px -36% 0px'
  });
  servicePanels.forEach(panel => serviceObserver.observe(panel));
}
