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
const serviceStickyTitle = document.getElementById('serviceStickyTitle');
const serviceStickyCopy = document.getElementById('serviceStickyCopy');

const serviceStickyContent = {
  sheetmetal: {
    title: '建築板金',
    copy: '建物の外まわりに関わる金属部分の工事。'
  },
  roof: {
    title: '屋根',
    copy: '屋根材の傷みや金属部分の劣化について。'
  },
  wall: {
    title: '外壁',
    copy: '外壁のひびや傷みなど、外まわりのご相談。'
  }
};

function activateService(name){
  const content = serviceStickyContent[name];
  if (!content || !serviceStickyTitle) return;
  serviceStickyTitle.classList.add('is-changing');
  if (serviceStickyCopy) serviceStickyCopy.classList.add('is-changing');
  window.setTimeout(() => {
    serviceStickyTitle.textContent = content.title;
    if (serviceStickyCopy) serviceStickyCopy.textContent = content.copy;
    serviceStickyTitle.classList.remove('is-changing');
    if (serviceStickyCopy) serviceStickyCopy.classList.remove('is-changing');
  }, 90);
}

if (servicePanels.length && serviceStickyTitle && 'IntersectionObserver' in window) {
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
