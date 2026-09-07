from pathlib import Path

p = Path('deploy/index.html')
s = p.read_text(encoding='utf-8')

old_qty = "const id='i'+(idc++); qty[id]={name:n,n:0};"
new_qty = "const id='i'+(idc++); qty[id]={name:n,n:0,price:p};"
if old_qty in s:
    s = s.replace(old_qty, new_qty, 1)

old_refresh = """function refreshCount(){
  const n=Object.values(qty).reduce((s,x)=>s+x.n,0);
  selectedEl.innerHTML='選択中：<b>'+n+'</b> 点';
}"""
new_refresh = """function refreshCount(){
  const values=Object.values(qty);
  const n=values.reduce((s,x)=>s+x.n,0);
  const total=values.reduce((s,x)=>s+(x.price==null?0:x.price*x.n),0);
  const hasMarketPrice=values.some(x=>x.n>0 && x.price==null);
  const totalText='¥'+total.toLocaleString()+(hasMarketPrice?' ＋ 時価':'')+'（税込）';
  selectedEl.innerHTML='選択中：<b>'+n+'</b> 点　｜　合計金額：<b>'+totalText+'</b>';
}"""
if old_refresh in s:
    s = s.replace(old_refresh, new_refresh, 1)

s = s.replace('https://www.instagram.com/harutabakery2026/', 'https://www.instagram.com/harutabakery/')
s = s.replace('Instagram（@harutabakery2026）', 'Instagram（@harutabakery）')

p.write_text(s, encoding='utf-8')
