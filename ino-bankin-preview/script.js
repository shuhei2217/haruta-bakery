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

let activeServiceName = 'sheetmetal';
let serviceScrollTicking = false;

function activateService(name){
  const content = serviceStickyContent[name];
  if (!content || !serviceStickyTitle || name === activeServiceName) return;

  activeServiceName = name;
  serviceStickyTitle.textContent = content.title;
  if (serviceStickyCopy) serviceStickyCopy.textContent = content.copy;
}

function updateActiveServiceFromScroll(){
  if (!servicePanels.length || !serviceStickyTitle) return;

  const anchorY = window.innerHeight * 0.42;
  let selected = null;

  for (const panel of servicePanels) {
    const rect = panel.getBoundingClientRect();
    if (rect.top <= anchorY && rect.bottom > anchorY) {
      selected = panel;
      break;
    }
  }

  if (!selected) {
    selected = servicePanels.reduce((closest, panel) => {
      const rect = panel.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const distance = Math.abs(center - anchorY);
      if (!closest || distance < closest.distance) return { panel, distance };
      return closest;
    }, null)?.panel || null;
  }

  if (selected) activateService(selected.dataset.service);
}

function scheduleServiceUpdate(){
  if (serviceScrollTicking) return;
  serviceScrollTicking = true;
  window.requestAnimationFrame(() => {
    updateActiveServiceFromScroll();
    serviceScrollTicking = false;
  });
}

if (servicePanels.length && serviceStickyTitle) {
  window.addEventListener('scroll', scheduleServiceUpdate, { passive: true });
  window.addEventListener('resize', scheduleServiceUpdate);
  updateActiveServiceFromScroll();
}

