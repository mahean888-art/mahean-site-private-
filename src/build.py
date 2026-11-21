# -*- coding: utf-8 -*-
# Rebuild on the user's ORIGINAL upload design, with the latest content.
import re, sys, io, json, base64, html, importlib.util
from PIL import Image
import os
SRC = os.path.dirname(os.path.abspath(__file__)) + '/'
ORIG = SRC + 'base.html'
spec = importlib.util.spec_from_file_location('content', SRC + 'content.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
out = sys.argv[1]
s = open(ORIG, encoding='utf-8').read()

def sub_once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)

# ---- images
META = json.load(open(SRC + 'assets/photos/meta.json'))
def embed(key, caption):
    m = META[key]; f = SRC + 'assets/photos/' + os.path.basename(m['file'])
    if f.endswith('.gif'):
        data = open(f, 'rb').read(); mime = 'image/gif'; cls = ' class="pixel"'
    else:
        im = Image.open(f).convert('RGB'); im.thumbnail((1000, 1000))
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=80, optimize=True, progressive=True)
        data = buf.getvalue(); mime = 'image/jpeg'; cls = ''
    uri = 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode())
    artist = html.escape(m['artist'].replace('derivative work:', '').strip()[:60])
    credit = f'<a href="{m["page"]}">{artist} &middot; {m["license"]}</a>'
    return (f'<figure class="photo"><img{cls} src="{uri}" alt="" loading="lazy">'
            f'<figcaption>{caption} <span class="credit">{credit}</span></figcaption></figure>')
IMG_RE = re.compile(r'\{IMG:([a-z]+)\|(.*?)\}', re.S)

# ---- background: the same artwork, cleanly set in deep space on the right
bg = base64.b64encode(open(SRC + 'art/engraved.jpg', 'rb').read()).decode()
s, n = re.subn(r"url\('data:image/jpeg;base64,[^']+'\) 80% center / cover no-repeat;\n  opacity: \.48;",
               "url('data:image/jpeg;base64," + bg + "') right center / cover no-repeat;\n  opacity: 1;", s, count=1)
assert n == 1

# ---- sidebar directory: clean human-readable labels, no repetitive file icons
a = s.index('<div class="folders">'); e = s.index('</div><p class="foot">', a) + len('</div>')
int_items = ''.join(f'<li><a href="#{sl}" data-title="{html.unescape(t)}">{t}</a></li>' for sl, t, _, _ in C.INTERESTS)
folders_html = (
    '<div class="folders">'
    '<section class="folder"><div class="tab">Home</div><div class="body"><ul>'
    '<li><a href="#about" data-title="About">About</a></li>'
    '</ul></div></section>'
    f'<section class="folder"><div class="tab">Interests</div><div class="body"><ul>{int_items}</ul></div></section>'
    '<section class="folder"><div class="tab">Archive</div><div class="body"><ul>'
    '<li><a href="#notes" data-title="Notes">Notes</a></li>'
    '<li><a href="#bookshelf" data-title="Bookshelf">Bookshelf</a></li>'
    '</ul></div></section>'
    '</div>'
)
s = s[:a] + folders_html + s[e:]

# ---- about
portrait = re.search(r'<img class="portrait"[^>]*>', s).group(0)
def about_html():
    paras = ''.join(f'<p class="{c}">{t}</p>\n' if c else f'<p>{t}</p>\n' for c, t in C.ABOUT_PARAS)
    items = ''.join(f'<li><a class="int-title" href="#{sl}">{t}</a>' + ''.join(f'<p>{x}</p>' for x in short) + '</li>'
                    for sl, t, short, _ in C.INTERESTS)
    return ('<header class="intro">\n' + portrait + '\n<div><h1>Mahean<br>Magamemnon</h1></div>\n</header>\n' + paras +
            '<div class="contact"><a href="mailto:mahean888@gmail.com">mahean888@gmail.com</a><a href="https://x.com/maheanmm">X / maheanmm</a></div>\n'
            '<section class="interests"><h2>Interests</h2><ul>' + items + '</ul></section>')
a = s.index('<main id="content" tabindex="-1">') + len('<main id="content" tabindex="-1">')
b = s.index('</main>', a); s = s[:a] + about_html() + s[b:]
a = s.index('<template id="page-about">') + len('<template id="page-about">\n')
b = s.index('</template>', a); s = s[:a] + about_html() + '\n' + s[b:]

# ---- interest pages replace Page 1-4
s, n = re.subn(r'<template id="page-(?!about|notes|bookshelf)[a-z0-9-]+">.*?</template>\n', '', s, flags=re.S); assert n == 9, n
N = len(C.INTERESTS)
def page(i, sl, t, body):
    body = IMG_RE.sub(lambda m: embed(m.group(1), m.group(2)), body)
    return (f'<template id="page-{sl}">\n<p class="crumb"><a href="#about">Interests</a> <span>{i} / {N}</span></p>'
            f'<h1 class="page-title">{t}</h1><div class="sub">{body}</div>'
            f'<p class="back"><a href="#about">&larr; About</a></p>\n</template>')
k = s.index('<template id="page-notes">')
s = s[:k] + '\n'.join(page(i, sl, t, body) for i, (sl, t, _, body) in enumerate(C.INTERESTS, 1)) + '\n' + s[k:]
s = s.replace('<h2>notes</h2>', '<h2>Notes</h2>').replace('<h2>bookshelf</h2>', '<h2>Bookshelf</h2>')

sub_once('inset: 0 0 0 50%;\n  z-index: -1;', 'inset: 0;\n  z-index: -1;')
sub_once('linear-gradient(90deg, #1b3550 0%, rgba(27,53,80,.7) 50%, rgba(27,53,80,.35))', 'linear-gradient(90deg, rgba(12,12,12,.10) 0%, rgba(12,12,12,.22) 28%, rgba(12,12,12,.22) 52%, rgba(12,12,12,0) 70%)')
# favicon from the portrait
pm = re.search(r'<img class="portrait" src="data:image/jpeg;base64,([^"]+)"', s)
pim = Image.open(io.BytesIO(base64.b64decode(pm.group(1)))).convert('RGB')
w0, h0 = pim.size; side = min(w0, h0)
pim = pim.crop(((w0-side)//2, 0, (w0+side)//2, side)).resize((128, 128), Image.LANCZOS)
fb = io.BytesIO(); pim.save(fb, 'PNG', optimize=True)
fav = 'data:image/png;base64,' + base64.b64encode(fb.getvalue()).decode()
s = s.replace('<title>', f'<link rel="icon" type="image/png" href="{fav}"><link rel="apple-touch-icon" href="{fav}">\n<title>', 1)
# ---- meta
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Mahean Magamemnon. Founder of Foresight Machines; studying computational sciences at Minerva University.">', s)

# ---- CSS refinements (appended to the original stylesheet)
css = open(SRC + 'orig_refine.css', encoding='utf-8').read()
a = s.index('</style>'); s = s[:a] + css + '\n' + s[a:]

# ---- script: original hash navigation + widgets
js = open(SRC + 'app.js', encoding='utf-8').read()
js = js.replace("window.scrollTo(0, 0);\n  mountWidgets();", "window.scrollTo(0, 0);\n  if (document.activeElement && document.activeElement.closest('.has-sub')) document.activeElement.blur();\n  mountWidgets();")
a = s.index('<script>'); b = s.index('</script>') + len('</script>')
s = s[:a] + '<script>\n' + js + '\n</script>' + s[b:]

# every outside link opens in a new tab
s = re.sub(r'<a href="(https?://[^"]+)"(?![^>]*target=)', r'<a href="\1" target="_blank" rel="noopener noreferrer"', s)
open(out, 'w', encoding='utf-8').write(s)
print('ok', len(s))
