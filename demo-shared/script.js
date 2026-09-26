const menuBtn=document.querySelector('.menu-button');
const drawer=document.querySelector('.drawer');
const drawerClose=document.querySelector('.drawer-close');
function setDrawer(open){
  if(!drawer||!menuBtn)return;
  drawer.classList.toggle('open',open);
  drawer.setAttribute('aria-hidden',String(!open));
  menuBtn.setAttribute('aria-expanded',String(open));
  document.body.style.overflow=open?'hidden':'';
}
menuBtn?.addEventListener('click',()=>setDrawer(!drawer?.classList.contains('open')));
drawerClose?.addEventListener('click',()=>setDrawer(false));
drawer?.addEventListener('click',e=>{if(e.target===drawer)setDrawer(false)});
drawer?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setDrawer(false)));
document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));

const panels=[...document.querySelectorAll('[data-service]')];
const stickyTitle=document.getElementById('serviceStickyTitle');
const stickyCopy=document.getElementById('serviceStickyCopy');
function activate(panel){
  if(!panel||!stickyTitle)return;
  const title=panel.querySelector('h3')?.textContent?.trim();
  const copy=panel.querySelector('p:not(.service-no)')?.textContent?.trim();
  if(title)stickyTitle.textContent=title;
  if(copy&&stickyCopy)stickyCopy.textContent=copy;
}
let ticking=false;
function update(){
  if(!panels.length||!stickyTitle)return;
  const y=window.innerHeight*.42;
  let selected=panels.find(p=>{const r=p.getBoundingClientRect();return r.top<=y&&r.bottom>y});
  if(!selected)selected=panels.reduce((best,p)=>{
    const r=p.getBoundingClientRect(),d=Math.abs(r.top+r.height/2-y);
    return !best||d<best.d?{p,d}:best;
  },null)?.p;
  activate(selected);
}
function schedule(){if(ticking)return;ticking=true;requestAnimationFrame(()=>{update();ticking=false})}
if(panels.length){window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);update();}
