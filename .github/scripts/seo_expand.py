from pathlib import Path
import json, re

root = Path('.')
index = root / 'index.html'
s = index.read_text(encoding='utf-8')

old_hero = '            Construyo identidades visuales que <em>respiran</em>, comunican y permanecen. Branding estratégico para marcas que quieren dejar de parecerse a las demás.'
new_hero = '            Branding, identidad visual, diseño gráfico y contenido audiovisual para marcas en <strong>Perú</strong>. Construyo sistemas visuales que <em>respiran</em>, comunican y permanecen.'
if old_hero in s:
    s = s.replace(old_hero, new_hero, 1)

services_marker = '<!-- ============================================================ SERVICES -->'
local_section = '''<!-- ============================================================ SEO LOCAL / PERÚ -->
<section class="seo-local" aria-labelledby="seo-local-title">
    <div class="seo-local__eyebrow">Estudio creativo · Lima, Perú</div>
    <h2 id="seo-local-title">Branding, diseño gráfico y contenido audiovisual <em>para marcas en Perú</em>.</h2>
    <p>Adriana Branding acompaña a negocios, emprendimientos y marcas que necesitan construir una identidad clara y llevarla de forma coherente a piezas gráficas, redes sociales y contenido en movimiento. El trabajo se desarrolla desde Lima y está disponible para proyectos en todo Perú.</p>
    <nav class="seo-local__links" aria-label="Servicios creativos en Perú">
        <a href="/branding-peru/" data-cursor="hover">Branding en Perú ↗</a>
        <a href="/diseno-grafico-peru/" data-cursor="hover">Diseño gráfico en Perú ↗</a>
        <a href="/contenido-audiovisual-peru/" data-cursor="hover">Contenido audiovisual en Perú ↗</a>
    </nav>
</section>

'''
if 'id="seo-local-title"' not in s and services_marker in s:
    s = s.replace(services_marker, local_section + services_marker, 1)

replacements = {
    '<h3 class="service__title">Brand<em>ing</em></h3>': '<h3 class="service__title"><a href="/branding-peru/" data-cursor="hover">Brand<em>ing</em></a></h3>',
    '<h3 class="service__title">Dise<em>ño</em></h3>': '<h3 class="service__title"><a href="/diseno-grafico-peru/" data-cursor="hover">Dise<em>ño</em></a></h3>',
    '<h3 class="service__title">Audio<em>visual</em></h3>': '<h3 class="service__title"><a href="/contenido-audiovisual-peru/" data-cursor="hover">Audio<em>visual</em></a></h3>',
}
for old, new in replacements.items():
    if old in s:
        s = s.replace(old, new, 1)

css_marker = '/* ============================================================\n   SERVICES'
seo_css = '''/* ============================================================
   SEO LOCAL — visible, editorial and integrated with the brand
   ============================================================ */
.seo-local {
    padding: 90px 40px;
    max-width: 1440px;
    margin: 0 auto;
    border-top: 1px solid var(--line);
}
.seo-local__eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 24px;
}
.seo-local h2 {
    max-width: 1100px;
    font-family: var(--font-display);
    font-size: clamp(38px, 5vw, 76px);
    line-height: 0.98;
    letter-spacing: -0.035em;
    font-weight: 400;
    text-wrap: balance;
}
.seo-local h2 em { font-style: italic; font-weight: 400; }
.seo-local p {
    max-width: 800px;
    margin-top: 32px;
    font-size: clamp(16px, 1.4vw, 20px);
    line-height: 1.6;
    color: var(--gray-3);
}
.seo-local__links {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 34px;
}
.seo-local__links a {
    border: 1px solid var(--ink);
    border-radius: 999px;
    padding: 11px 18px;
    font-family: var(--font-mono);
    font-size: 12px;
    letter-spacing: 0.04em;
    transition: background .25s var(--ease-out), color .25s var(--ease-out), transform .25s var(--ease-out);
}
.seo-local__links a:hover {
    background: var(--ink);
    color: var(--paper);
    transform: translateY(-2px);
}
.service__title a { display: inline-block; }
@media (max-width: 900px) {
    .seo-local { padding: 70px 20px; }
    .seo-local__links { flex-direction: column; align-items: flex-start; }
}

'''
if '.seo-local {' not in s and css_marker in s:
    s = s.replace(css_marker, seo_css + css_marker, 1)

schema_match = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', s, re.S)
if schema_match:
    try:
        data = json.loads(schema_match.group(1))
        data['hasOfferCatalog'] = {
            '@type': 'OfferCatalog',
            'name': 'Servicios creativos de Adriana Branding',
            'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Branding e identidad visual en Perú', 'url': 'https://adrianabranding.com/branding-peru/'}},
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Diseño gráfico en Perú', 'url': 'https://adrianabranding.com/diseno-grafico-peru/'}},
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Contenido audiovisual en Perú', 'url': 'https://adrianabranding.com/contenido-audiovisual-peru/'}},
            ]
        }
        pretty = json.dumps(data, ensure_ascii=False, indent=2)
        s = s[:schema_match.start(1)] + pretty + s[schema_match.end(1):]
    except Exception as e:
        print('Schema enrichment skipped:', e)

index.write_text(s, encoding='utf-8')

services = [
    {
        'slug': 'branding-peru',
        'label': 'Branding',
        'title': 'Branding e Identidad Visual en Perú | Adriana Branding',
        'h1': 'Branding e identidad visual para marcas en Perú.',
        'description': 'Servicio de branding e identidad visual en Perú: estrategia de marca, naming, logo, paleta, tipografía, sistema visual y manual de uso con Adriana Branding.',
        'intro': 'Una marca no se construye solamente con un logo. Se construye con decisiones visuales y conceptuales capaces de mantenerse coherentes cuando la marca crece, publica, vende y conversa con su audiencia.',
        'sections': [
            ('¿Qué incluye un proyecto de branding?', 'El proceso puede integrar investigación y dirección conceptual, naming cuando el proyecto lo requiere, diseño de logotipo, selección cromática, tipografías, recursos gráficos y lineamientos de aplicación. El objetivo es crear un sistema visual que pueda vivir con coherencia en distintos formatos.'),
            ('Identidad visual pensada para el uso real', 'La identidad debe funcionar fuera de una presentación bonita. Por eso se piensa desde aplicaciones reales: redes sociales, piezas comerciales, material corporativo, campañas y otros puntos de contacto de la marca. Cada decisión busca que el sistema sea reconocible y flexible.'),
            ('¿Para quién es?', 'Para emprendimientos que están definiendo su identidad, negocios que crecieron sin una línea visual consistente y marcas que necesitan ordenar o renovar su presencia. Adriana Branding trabaja desde Lima con proyectos en todo Perú.'),
            ('Del concepto al sistema visual', 'El trabajo parte de entender el negocio, su personalidad y el contexto en el que compite. A partir de esa base se desarrolla una dirección visual y, posteriormente, un conjunto de recursos que permiten que la marca conserve su carácter sin importar el formato.'),
        ],
        'tags': ['Estrategia visual', 'Logo', 'Paleta', 'Tipografía', 'Manual de marca', 'Sistema visual'],
        'other': [('Diseño gráfico', '/diseno-grafico-peru/'), ('Audiovisual', '/contenido-audiovisual-peru/')],
    },
    {
        'slug': 'diseno-grafico-peru',
        'label': 'Diseño gráfico',
        'title': 'Diseño Gráfico en Perú | Adriana Branding',
        'h1': 'Diseño gráfico para marcas y negocios en Perú.',
        'description': 'Diseño gráfico en Perú para marcas y negocios: flyers, banners, redes sociales, packaging, piezas editoriales y comunicación visual con Adriana Branding.',
        'intro': 'El diseño gráfico convierte una identidad en comunicación cotidiana. Una buena pieza no solo debe verse bien: debe respetar la marca, ordenar la información y funcionar en el formato y contexto donde será vista.',
        'sections': [
            ('Piezas que sostienen la identidad', 'Flyers, banners, piezas para redes sociales, materiales editoriales, packaging y recursos comerciales se desarrollan como extensiones de una misma identidad. Esto evita que la marca cambie de personalidad en cada publicación o campaña.'),
            ('Diseño para redes y campañas', 'Cada formato tiene sus propias reglas de lectura. El trabajo considera jerarquía, ritmo, legibilidad y adaptación a formatos digitales, manteniendo la personalidad de la marca y priorizando una comunicación clara.'),
            ('Diseño editorial y corporativo', 'Catálogos, presentaciones, documentos y otras piezas de información necesitan estructura, consistencia tipográfica y una narrativa visual ordenada. El diseño ayuda a que contenidos complejos sean más claros y memorables.'),
            ('Servicio desde Lima para Perú', 'Adriana Branding desarrolla proyectos de diseño gráfico desde Lima para emprendimientos, negocios, marcas personales y empresas de distintas partes de Perú, trabajando de forma remota cuando el proyecto lo permite.'),
        ],
        'tags': ['Flyers', 'Social media', 'Banners', 'Editorial', 'Packaging', 'Piezas corporativas'],
        'other': [('Branding', '/branding-peru/'), ('Audiovisual', '/contenido-audiovisual-peru/')],
    },
    {
        'slug': 'contenido-audiovisual-peru',
        'label': 'Audiovisual',
        'title': 'Contenido Audiovisual y Reels en Perú | Adriana Branding',
        'h1': 'Contenido audiovisual para marcas en Perú.',
        'description': 'Contenido audiovisual en Perú: edición de video, reels, motion graphics y piezas para redes sociales alineadas con la identidad visual de tu marca.',
        'intro': 'Cuando una identidad entra en movimiento también necesita reglas. La edición, el ritmo, la tipografía y los recursos gráficos deben sentirse parte de la misma marca que vive en sus piezas estáticas.',
        'sections': [
            ('Edición de video y reels', 'El contenido se edita pensando en ritmo, claridad y retención, pero también en identidad. Los reels y piezas cortas pueden integrar tipografía, recursos gráficos y decisiones de montaje coherentes con la marca.'),
            ('Motion graphics con identidad', 'El movimiento no tiene por qué sentirse como una capa separada. Animaciones, títulos, transiciones y recursos gráficos pueden construirse a partir del mismo lenguaje visual para que cada pieza refuerce el reconocimiento de marca.'),
            ('Contenido para redes sociales', 'Las piezas audiovisuales se plantean según el canal y el objetivo de comunicación. El formato vertical, las aperturas rápidas y la legibilidad móvil son parte del proceso, sin sacrificar consistencia visual.'),
            ('Producción y postproducción desde Lima', 'Adriana combina experiencia en diseño con producción y postproducción audiovisual. Atiende proyectos para marcas en Lima y otras ciudades de Perú, con flujos de trabajo remotos cuando la producción lo permite.'),
        ],
        'tags': ['Reels', 'Edición', 'Motion graphics', 'Video social', 'Postproducción', 'Identidad en movimiento'],
        'other': [('Branding', '/branding-peru/'), ('Diseño gráfico', '/diseno-grafico-peru/')],
    },
]

def page_html(x):
    canonical = f"https://adrianabranding.com/{x['slug']}/"
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Service',
        '@id': canonical + '#service',
        'name': x['h1'].rstrip('.'),
        'url': canonical,
        'description': x['description'],
        'areaServed': {'@type': 'Country', 'name': 'Perú'},
        'provider': {
            '@type': 'ProfessionalService',
            '@id': 'https://adrianabranding.com/#business',
            'name': 'Adriana Branding',
            'url': 'https://adrianabranding.com/',
            'telephone': '+51940708161',
            'email': 'adrianabrandingpe@gmail.com',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Lima', 'addressCountry': 'PE'}
        }
    }
    sections = ''.join(f'<section class="content-block"><h2>{h}</h2><p>{p}</p></section>' for h, p in x['sections'])
    tags = ''.join(f'<span>{t}</span>' for t in x['tags'])
    other = ''.join(f'<a href="{url}">{name} ↗</a>' for name, url in x['other'])
    return f'''<!DOCTYPE html>
<html lang="es-PE">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{x['title']}</title>
<meta name="description" content="{x['description']}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<link rel="canonical" href="{canonical}" />
<link rel="alternate" hreflang="es-PE" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="es_PE" />
<meta property="og:site_name" content="Adriana Branding" />
<meta property="og:title" content="{x['title']}" />
<meta property="og:description" content="{x['description']}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="https://adrianabranding.com/assets/logo/LOGO-HERO-DARK.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/png" href="/assets/logo/LOGOCUADRADO-01.png" />
<link rel="preload" href="/assets/fonts/CalSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/CalSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<style>
@font-face{{font-family:'Cal Sans';src:url('/assets/fonts/CalSans-Regular.woff2') format('woff2');font-weight:400;font-display:swap}}
@font-face{{font-family:'Cal Sans';src:url('/assets/fonts/CalSans-SemiBold.woff2') format('woff2');font-weight:600;font-display:swap}}
:root{{--yellow:#FFB800;--ink:#0E0F11;--paper:#F6F4EE;--gray:#66645e;--line:rgba(14,15,17,.14)}}
*{{box-sizing:border-box;margin:0;padding:0}} html{{scroll-behavior:smooth}}
body{{font-family:'Cal Sans',system-ui,sans-serif;background:var(--paper);color:var(--ink);line-height:1.55}}
a{{color:inherit;text-decoration:none}}
.top{{padding:24px 40px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line)}}
.brand img{{height:50px;width:auto}} .back{{font-size:13px;letter-spacing:.05em;text-transform:uppercase}}
.hero{{padding:110px 40px 90px;max-width:1440px;margin:auto}}
.kicker{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin-bottom:28px}}
h1{{font-size:clamp(54px,8vw,120px);line-height:.9;letter-spacing:-.045em;font-weight:400;max-width:1250px}}
.lead{{font-size:clamp(20px,2.1vw,30px);line-height:1.35;max-width:850px;margin-top:46px;color:#393936}}
.tags{{display:flex;flex-wrap:wrap;gap:10px;margin-top:34px}} .tags span{{border:1px solid var(--ink);border-radius:999px;padding:9px 14px;font-size:12px}}
.main{{max-width:1440px;margin:auto;padding:0 40px 100px;display:grid;grid-template-columns:1fr 1fr;gap:0 80px}}
.content-block{{padding:56px 0;border-top:1px solid var(--line)}} .content-block h2{{font-size:clamp(30px,3.4vw,52px);line-height:1;letter-spacing:-.025em;font-weight:400;margin-bottom:20px}}
.content-block p{{font-size:18px;line-height:1.65;color:#484741;max-width:650px}}
.cta{{background:var(--yellow);padding:90px 40px;text-align:center}} .cta h2{{font-size:clamp(46px,7vw,100px);line-height:.92;letter-spacing:-.04em;font-weight:400}}
.cta p{{font-size:18px;margin:24px auto 30px;max-width:660px}} .actions{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.actions a{{background:var(--ink);color:var(--yellow);padding:15px 22px;border-radius:999px}}
.related{{padding:50px 40px;max-width:1440px;margin:auto;display:flex;justify-content:space-between;gap:20px;border-top:1px solid var(--line)}}
.related strong{{font-size:14px;text-transform:uppercase;letter-spacing:.1em}} .related nav{{display:flex;gap:20px;flex-wrap:wrap}}
footer{{padding:30px 40px;border-top:1px solid var(--line);font-size:13px;color:var(--gray);display:flex;justify-content:space-between;gap:20px}}
@media(max-width:800px){{.top,.hero,.main,.cta,.related,footer{{padding-left:20px;padding-right:20px}} .top{{padding-top:18px;padding-bottom:18px}} .brand img{{height:40px}} .hero{{padding-top:80px;padding-bottom:70px}} .main{{grid-template-columns:1fr}} .related,footer{{flex-direction:column}}}}
</style>
</head>
<body>
<header class="top"><a class="brand" href="/" aria-label="Adriana Branding, inicio"><img src="/assets/logo/LOGOHORIZONTAL-NAV-DARK.png" alt="Adriana Branding" /></a><a class="back" href="/">← Ver portafolio</a></header>
<main>
<section class="hero"><div class="kicker">{x['label']} · Lima, Perú · Servicios para todo Perú</div><h1>{x['h1']}</h1><p class="lead">{x['intro']}</p><div class="tags">{tags}</div></section>
<div class="main">{sections}</div>
<section class="cta"><h2>Construyamos una marca que se reconozca.</h2><p>Cuéntame qué estás creando, qué necesitas comunicar y en qué etapa está tu proyecto.</p><div class="actions"><a href="mailto:adrianabrandingpe@gmail.com">Correo ↗</a><a href="https://wa.me/51940708161" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a><a href="https://www.instagram.com/adriana.branding?igsi=MTBmMGRqbjdudnF1bA==" target="_blank" rel="noopener noreferrer">Instagram ↗</a></div></section>
<section class="related"><strong>Explora otros servicios</strong><nav>{other}<a href="/#work">Ver proyectos ↗</a></nav></section>
</main>
<footer><span>Adriana Branding · Lima, Perú</span><span>Branding · Diseño · Audiovisual</span></footer>
</body>
</html>'''

for x in services:
    d = root / x['slug']
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(page_html(x), encoding='utf-8')

sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://adrianabranding.com/</loc><lastmod>2026-08-25</lastmod><priority>1.0</priority></url>
  <url><loc>https://adrianabranding.com/branding-peru/</loc><lastmod>2026-08-25</lastmod><priority>0.9</priority></url>
  <url><loc>https://adrianabranding.com/diseno-grafico-peru/</loc><lastmod>2026-08-25</lastmod><priority>0.9</priority></url>
  <url><loc>https://adrianabranding.com/contenido-audiovisual-peru/</loc><lastmod>2026-08-25</lastmod><priority>0.9</priority></url>
</urlset>
'''
(root / 'sitemap.xml').write_text(sitemap, encoding='utf-8')

for f in [root/'index.html', root/'branding-peru/index.html', root/'diseno-grafico-peru/index.html', root/'contenido-audiovisual-peru/index.html', root/'sitemap.xml']:
    if not f.exists() or f.stat().st_size < 100:
        raise SystemExit(f'Invalid generated file: {f}')

print('SEO expansion generated successfully.')
