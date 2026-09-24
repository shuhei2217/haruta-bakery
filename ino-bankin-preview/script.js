const root = document.documentElement;
const menuBtn = document.querySelector('.menu-button');
const drawer = document.querySelector('.drawer');
const drawerClose = document.querySelector('.drawer-close');

function setDrawer(open){
  drawer.classList.toggle('open', open);
  drawer.setAttribute('aria-hidden', String(!open));
  menuBtn.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
}
menuBtn.addEventListener('click', () => setDrawer(!drawer.classList.contains('open')));
drawerClose.addEventListener('click', () => setDrawer(false));
drawer.addEventListener('click', e => { if (e.target === drawer) setDrawer(false); });
drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setDrawer(false)));

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const reveals = [...document.querySelectorAll('.reveal')];
if (!reduced && 'IntersectionObserver' in window) {
  root.classList.add('js-motion');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: .08, rootMargin: '0px 0px 70px 0px' });
  reveals.forEach(el => io.observe(el));
  setTimeout(() => reveals.forEach(el => el.classList.add('visible')), 1600);
} else {
  reveals.forEach(el => el.classList.add('visible'));
}