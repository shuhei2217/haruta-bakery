from pathlib import Path
import json, re, html, shutil

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "ino-bankin-preview"
DATA = ROOT / "paint-demos" / "sites.json"
OUT = ROOT / "deploy-paint"

def esc(v):
    return html.escape(str(v), quote=True)

def replace_service(s, key, icon, num, title, body):
    signals = [title, "ご相談", "住まい"]
    block = (
        f'<article class="service-panel" data-service="{key}">'
        f'<div class="service-panel-icon"><svg class="icon-svg" aria-hidden="true"><use href="#icon-{icon}"/></svg></div>'
        f'<p class="service-no">{num}</p><h3>{esc(title)}</h3><p>{esc(body)}</p>'
        f'<div class="service-signals">' + "".join(f'<span>{esc(x)}</span>' for x in signals) + '</div>'
        f'<span class="service-keyword">{esc("・".join(signals))}</span></article>'
    )
    return re.sub(rf'<article class="service-panel" data-service="{key}">[\s\S]*?</article>', block, s, count=1)

def build_site(src, c):
    s = src
    name, short, location = c["name"], c["short"], c["location"]
    phone = c["phone"]
    digits = re.sub(r"\D", "", phone)
    summary = "・".join(x[0] for x in c["services"])
    colors = c["colors"]

    s = re.sub(r'<title>[\s\S]*?</title>', f'<title>{esc(name)}｜{esc(location)}の塗装・住まいのご相談</title>', s, count=1)
    s = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{esc(location)}の{esc(name)}。{esc(summary)}のご相談に対応。" />', s, count=1)
    s = re.sub(r'href="styles\.css[^"]*"', 'href="../demo-shared/styles.css?v=20260926"', s, count=1)
    s = re.sub(r'src="script\.js[^"]*"', 'src="../demo-shared/script.js?v=20260926"', s, count=1)
    s = s.replace('images/', '../demo-shared/images/')
    s = s.replace('fill="#082c59"', f'fill="{colors[0]}"').replace('fill="#d51c17"', f'fill="{colors[1]}"').replace('fill="#e52a20"', f'fill="{colors[1]}"')
    override = f'''<style>:root{{--navy:{colors[0]};--navy2:{colors[2]};--navy3:{colors[0]};--red:{colors[1]};--red2:{colors[3]}}}
.header-action,.cta{{background:linear-gradient(180deg,var(--red),var(--red2))}}
.headline-c{{font-size:clamp(38px,5.4vw,72px)}}@media(max-width:640px){{.headline-c{{font-size:clamp(31px,9.5vw,45px)}}}}</style>'''
    s = s.replace('</head>', override + '</head>', 1)

    s = s.replace('aria-label="井野板金工業 トップへ"', f'aria-label="{esc(short)} トップへ"')
    s = re.sub(r'<span class="brand-copy">[\s\S]*?</span>', f'<span class="brand-copy"><small>{esc(c["tag"])}</small><strong>{esc(short)}</strong></span>', s, count=1)
    s = s.replace('<a href="#strengths">井野板金工業について</a>', f'<a href="#strengths">{esc(short)}について</a>')
    s = s.replace('0582948544', digits).replace('058-294-8544', phone)

    s = re.sub(r'<p class="hero-small">[\s\S]*?</p>', f'<p class="hero-small">{esc(c["heroSmall"])}</p>', s, count=1)
    s = re.sub(r'<div class="headline-line headline-a">[\s\S]*?</div>', '<div class="headline-line headline-a"><span>屋根・外壁</span><b>の</b></div>', s, count=1)
    s = re.sub(r'<div class="headline-line headline-b">[\s\S]*?</div>', '<div class="headline-line headline-b">ご相談は</div>', s, count=1)
    s = re.sub(r'<div class="headline-line headline-c">[\s\S]*?</div>', f'<div class="headline-line headline-c"><span>{esc(short)}</span><small>へ</small></div>', s, count=1)
    s = re.sub(r'<p class="hero-sub">[\s\S]*?</p>', f'<p class="hero-sub">{esc(c["heroSub"])}</p>', s, count=1)
    s = re.sub(r'<p class="hero-desc">[\s\S]*?</p>', f'<p class="hero-desc">{esc(c["heroDesc"])}</p>', s, count=1)

    s = re.sub(r'<section class="trust-band" aria-label="[^"]*">', f'<section class="trust-band" aria-label="{esc(short)}の基本情報">', s, count=1)
    s = re.sub(r'<div><small>LOCATION</small><strong>[\s\S]*?</strong><p>[\s\S]*?</p></div>', f'<div><small>LOCATION</small><strong>{esc(location)}に拠点</strong><p>地域の住まいの塗装・外まわりをご相談いただけます。</p></div>', s, count=1)
    s = re.sub(r'<div><small>SERVICE</small><strong>[\s\S]*?</strong><p>[\s\S]*?</p></div>', f'<div><small>SERVICE</small><strong>{esc(summary)}</strong><p>確認できた事業内容をご案内しています。</p></div>', s, count=1)
    s = re.sub(r'<header class="section-head center">\s*<p class="eyebrow">SERVICE</p>[\s\S]*?</header>', f'<header class="section-head center"><p class="eyebrow">SERVICE</p><h2>事業内容</h2><p>{esc(summary)}についてご相談いただけます。</p></header>', s, count=1)

    keys = [("sheetmetal","sheetmetal","01"),("roof","roof","02"),("wall","wall","03")]
    for i, (key, icon, num) in enumerate(keys):
        title, body = c["services"][i]
        s = replace_service(s, key, icon, num, title, body)
    s = re.sub(r'<h3 class="service-vertical-title" id="serviceStickyTitle">[\s\S]*?</h3>', f'<h3 class="service-vertical-title" id="serviceStickyTitle">{esc(c["services"][0][0])}</h3>', s, count=1)
    s = re.sub(r'<p class="service-vertical-copy" id="serviceStickyCopy">[\s\S]*?</p>', f'<p class="service-vertical-copy" id="serviceStickyCopy">{esc(c["services"][0][1])}</p>', s, count=1)

    s = s.replace('<h2>建物の外まわりを、<br>板金の技術で支える。</h2>', f'<h2>{esc(c["craftTitle"])}</h2>')
    s = re.sub(r'<p class="craft-lead">[\s\S]*?</p>', f'<p class="craft-lead">{esc(c["craftLead"])}</p>', s, count=1)
    craft_lines = '<div class="craft-lines">' + ''.join(f'<div><span>0{i+1}</span><strong>{esc(t)}</strong><p>{esc(b)}</p></div>' for i,(t,b) in enumerate(c["services"])) + '</div>'
    s = re.sub(r'<div class="craft-lines">[\s\S]*?</div>\s*</div>\s*</div>\s*</section>', craft_lines + '</div></div></section>', s, count=1)

    concerns = '''<div class="concern-list">
<div class="concern-item"><b>01</b><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-wall"/></svg></i><span>外壁の色あせ・<br>汚れが気になる</span></div>
<div class="concern-item"><b>02</b><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-crack"/></svg></i><span>ひび・剥がれが<br>気になる</span></div>
<div class="concern-item"><b>03</b><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-roof"/></svg></i><span>屋根の傷みが<br>心配</span></div>
<div class="concern-item"><b>04</b><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-help"/></svg></i><span>どこに相談すれば<br>いいか分からない</span></div>
</div>'''
    s = re.sub(r'<div class="concern-list">[\s\S]*?</div>\s*</div>\s*</section>', concerns + '</div></section>', s, count=1)

    s = re.sub(r'<header class="section-head center"><p class="eyebrow">ABOUT</p><h2>[\s\S]*?</h2></header>', f'<header class="section-head center"><p class="eyebrow">ABOUT</p><h2>{esc(short)}について</h2></header>', s, count=1)
    old = [
        ("建築板金の専門性","建物の外まわりに関わる建築板金を中心に、屋根・外壁についてご相談いただけます。"),
        ("屋根・外壁をまとめて相談","どこへ相談すればよいか分からない外まわりの症状も、まずは気になる箇所をお伝えください。"),
        ("岐阜市に拠点","岐阜市北島に所在地を置く建築板金会社です。対応地域についてはお電話でご確認いただけます。"),
    ]
    for i,(ot,ob) in enumerate(old):
        nt, nb = c["strengths"][i]
        s = s.replace(f'<h3>{ot}</h3>\n            <p>{ob}</p>', f'<h3>{esc(nt)}</h3>\n            <p>{esc(nb)}</p>')

    s = re.sub(r'<div class="area-heading">[\s\S]*?</div>\s*<div class="area-contact">', f'<div class="area-heading"><p class="eyebrow">AREA</p><h2>対応エリア</h2><p>{esc(c["area"])}</p></div><div class="area-contact">', s, count=1)

    flow = f'''<ol class="flow-list flow-list-updated flow-list-final">
<li><span>01</span><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-phone"/></svg></i><h3>お電話で相談</h3><p>{esc(summary)}について、気になることをお伝えください。</p></li>
<li><span>02</span><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-help"/></svg></i><h3>状況をお伝え</h3><p>気になる箇所や現在の状況をお聞かせください。</p></li>
<li><span>03</span><i><svg class="icon-svg" aria-hidden="true"><use href="#icon-doc"/></svg></i><h3>内容に応じてご案内</h3><p>ご相談内容に応じて、必要な確認や次のご案内をします。</p></li>
</ol>'''
    s = re.sub(r'<ol class="flow-list flow-list-updated flow-list-final">[\s\S]*?</ol>', flow, s, count=1)

    rows = []
    for k,v in c["rows"]:
        if "電話" in k or k == "携帯":
            rows.append(f'<div><dt>{esc(k)}</dt><dd><a href="tel:{digits}">{esc(v)}</a></dd></div>')
        else:
            rows.append(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>')
    s = re.sub(r'<dl>[\s\S]*?</dl>', '<dl>' + ''.join(rows) + '</dl>', s, count=1)

    faq = [
        ("どんな工事を相談できますか？", f'{summary}についてご相談いただけます。'),
        ("対応エリアはどこですか？", c["area"]),
        ("まず電話で相談できますか？", f'{phone}までご相談ください。'),
        ("掲載されていない情報は？", "施工事例・料金・資格など未確認の情報は、正式制作時に確認して追加します。"),
    ]
    faq_html = '<div class="faq-list">' + ''.join(f'<details><summary><span>Q</span>{esc(q)}<b>＋</b></summary><p>{esc(a)}</p></details>' for q,a in faq) + '</div>'
    s = re.sub(r'<div class="faq-list">[\s\S]*?</div>\s*</div>\s*</section>', faq_html + '</div></section>', s, count=1)

    s = s.replace('<p>屋根・外壁・建築板金のことなら</p>', f'<p>{esc(summary)}のことなら</p>')
    s = s.replace("井野板金工業株式会社", name).replace("井野板金工業", short)
    s = re.sub(r'<div class="company-art company-art-photo" role="img" aria-label="[^"]*"><span>[^<]*</span></div>', '<div class="company-art company-art-photo" role="img" aria-label="塗装・住まいの工事イメージ"><span>施工イメージ</span></div>', s, count=1)
    s = s.replace('alt="屋根・外壁・建築板金を表現したイメージ"', 'alt="外壁・屋根・住まいの工事を表現したイメージ"')
    s = s.replace('alt="実在する住宅の金属屋根・外壁のイメージ"', 'alt="住宅の屋根・外壁のイメージ"')
    s = s.replace('建築板金・屋根工事イメージ', '屋根・外壁工事イメージ')
    return s

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shared = OUT / "demo-shared"
    shared.mkdir()
    shutil.copy2(SRC_DIR / "styles.css", shared / "styles.css")
    shutil.copy2(ROOT / "demo-shared" / "script.js", shared / "script.js")
    shutil.copytree(SRC_DIR / "images", shared / "images")

    src = (SRC_DIR / "index.html").read_text(encoding="utf-8")
    sites = json.loads(DATA.read_text(encoding="utf-8"))
    for c in sites:
        d = OUT / c["slug"]
        d.mkdir()
        (d / "index.html").write_text(build_site(src, c), encoding="utf-8")
    print(f"built {len(sites)} painting demo sites")

if __name__ == "__main__":
    main()
