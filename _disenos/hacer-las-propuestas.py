# -*- coding: utf-8 -*-
"""
LAS PROPUESTAS DE PORTADA DE LA TIENDA — SEGUNDA VUELTA
=======================================================

    python _disenos/hacer-las-propuestas.py

LA PRIMERA VUELTA NO SIRVIO y la direccion tenia razon: «el problema es el
diseño y los cuadritos, parece una hoja muy basica». Lo mire y era cierto --
tres de las cinco eran rejillas de cuadritos chiquitos y una era una lista.

Antes de rehacerlas fui a ver como lo hacen los que lo hacen bien (Things,
Linear, Setapp, el 8 de octubre de 2026). Lo que tienen en comun:

  1. ARRIBA, AIRE. Una frase enorme, centrada, fondo suave, dos botones y el
     buscador. Nada mas. Nada de tarjetitas en la primera pantalla.
  2. EL CATALOGO SON ESTANTES QUE SE DESLIZAN DE LADO, con tarjetas GRANDES.
     Setapp tiene cientos de aplicaciones y nunca enseña una cuadricula de
     cuadritos iguales.
  3. CADA PRODUCTO SE VE DISTINTO: su color, su imagen. La riqueza la da la
     variedad de las tarjetas, no el marco.
  4. SECCIONES CLARAS Y OSCURAS ALTERNADAS, para que la pagina respire.
  5. POQUISIMAS PALABRAS.

Las cuatro de abajo siguen esas reglas y se diferencian entre si en el caracter,
no en el acomodo.

Las imagenes son NUESTRAS: las fotos en 3D de las guias ya hechas. Cuando haya
presupuesto de fotografia, las de arriba se cambian por fotos de verdad: hoy
las portadas llevan letras dentro y por eso no sirven de fondo.

La carpeta empieza por «_»: GitHub Pages no la publica.
"""
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(AQUI, "img")
GUIAS = r"C:\Users\beby2\OneDrive\Desktop\Carpeta del equipo\Catalogo de Guias"

# (carpeta, titulo, categoria, color de la tarjeta)
CATALOGO = [
    ("01_Ley25", "La Ley 25, explicada", "Ley y papeles", "#2F4858"),
    ("08_Cuanto_Apartar", "Cuánto apartar para impuestos", "Impuestos", "#1F6F5C"),
    ("03_CNESST", "La CNESST sin sustos", "Ley y papeles", "#8C3B2E"),
    ("07_Detallado_Automotriz", "Detallado automotriz", "Oficios", "#2B3A67"),
    ("04_7Errores", "Los 7 errores", "Negocio", "#7A4E2D"),
    ("05_Fermentos", "Fermentos en casa", "Casa", "#4A6B3A"),
    ("11_Curriculum", "Tu currículum", "Trabajo", "#5B3A6E"),
    ("13_Creditos_Ayudas", "Créditos y ayudas", "Negocio", "#1B5566"),
]

BASE = """
  *{box-sizing:border-box;margin:0;padding:0}
  img{display:block;max-width:100%}
  a{color:inherit;text-decoration:none}
  body{-webkit-font-smoothing:antialiased;overflow-x:hidden}
  .estante{display:flex;gap:14px;overflow-x:auto;padding:0 20px 6px;scrollbar-width:none}
  .estante::-webkit-scrollbar{display:none}
"""


def traer():
    os.makedirs(IMG, exist_ok=True)
    out = []
    for carpeta, titulo, cat, color in CATALOGO:
        o = os.path.join(GUIAS, carpeta, "MOCKUP_3D.jpg")
        d = os.path.join(IMG, "%s-mockup.jpg" % carpeta)
        if os.path.exists(o) and not os.path.exists(d):
            shutil.copy2(o, d)
        if os.path.exists(d):
            out.append((carpeta, titulo, cat, color))
    return out


def pagina(css, cuerpo):
    return ("<!doctype html><html lang=es><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            "<style>%s%s</style></head><body>%s</body></html>" % (BASE, css, cuerpo))


def tarjetas(g, n=5, alto=250):
    """Tarjetas grandes, cada una con su color y el libro dentro."""
    return "".join(
        "<a class=tj style='background:%s'><div class=obj style=\"background-image:url('img/%s-mockup.jpg')\"></div>"
        "<div class=pie><h4>%s</h4><p>%s</p></div></a>" % (color, c, t, cat)
        for c, t, cat, color in g[:n])


# ===================================================== A · CLARA, AIRE Y ESTANTE
def a(g):
    css = """
      body{background:#fff;color:#101114;font:16px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto}
      .nav{display:flex;align-items:center;gap:12px;padding:16px 20px}
      .nav b{font-weight:800;font-size:13.5px;letter-spacing:.02em}
      .nav .bus{flex:1;background:#F2F3F5;border-radius:999px;padding:9px 14px;color:#9095A0;font-size:13px}
      .hero{background:linear-gradient(180deg,#E9F1FB 0%,#F6F4FF 46%,#fff 100%);
            padding:44px 24px 52px;text-align:center}
      .hero h1{font-size:40px;line-height:1.06;font-weight:800;letter-spacing:-.035em}
      .hero p{margin:16px auto 0;color:#5B616E;font-size:15.5px;max-width:28ch}
      .btns{display:flex;gap:10px;justify-content:center;margin-top:24px}
      .btns a{padding:14px 22px;border-radius:999px;font-weight:700;font-size:15px}
      .b1{background:#101114;color:#fff}
      .b2{background:#fff;border:1px solid #DDE0E6}
      h2{padding:34px 20px 4px;font-size:25px;font-weight:800;letter-spacing:-.02em}
      .sub2{padding:0 20px 16px;color:#878C97;font-size:14px}
      .tj{flex:0 0 190px;height:250px;border-radius:20px;position:relative;overflow:hidden}
      .obj{position:absolute;inset:10px 10px 86px;background-size:cover;background-position:center;
           border-radius:14px;filter:saturate(1.05)}
      .pie{position:absolute;left:0;right:0;bottom:0;padding:0 15px 16px;color:#fff}
      .pie h4{font-size:15px;font-weight:700;line-height:1.2}
      .pie p{font-size:11.5px;opacity:.7;margin-top:4px}
      footer{padding:34px 20px 40px;color:#9095A0;font-size:13px}
    """
    return pagina(css,
        "<div class=nav><b>AYMOR APPLIS</b><div class=bus>Buscar en el catálogo</div></div>"
        "<div class=hero><h1>Todo lo que tu<br>negocio necesita,<br>en un solo lugar.</h1>"
        "<p>Aplicaciones y guías hechas en Quebec. Sin contratos.</p>"
        "<div class=btns><a class=b1>Ver el catálogo</a><a class=b2>Cómo funciona</a></div></div>"
        "<h2>Lo que más sirve</h2><p class=sub2>Guías que se leen en una tarde</p>"
        "<div class=estante>" + tarjetas(g) + "</div>"
        "<footer>Aymor Applis — Quebec</footer>")


# ===================================================== B · OSCURA Y CINE
def b(g):
    css = """
      body{background:#08090B;color:#EDEFF2;font:16px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI"}
      .nav{display:flex;align-items:center;gap:12px;padding:16px 20px}
      .nav b{font-weight:800;font-size:13px;letter-spacing:.1em}
      .nav .bus{flex:1;background:rgba(255,255,255,.07);border-radius:999px;padding:9px 14px;
                color:rgba(237,239,242,.42);font-size:13px}
      .hero{position:relative;padding:62px 24px 70px;text-align:center;overflow:hidden}
      .hero::before{content:'';position:absolute;left:50%;top:-180px;width:620px;height:620px;
        transform:translateX(-50%);border-radius:50%;
        background:radial-gradient(circle,rgba(93,124,255,.46) 0%,rgba(8,9,11,0) 66%)}
      .hero h1{position:relative;font-size:44px;line-height:1.02;font-weight:800;letter-spacing:-.04em}
      .hero p{position:relative;margin:18px auto 0;color:rgba(237,239,242,.6);font-size:15.5px;max-width:27ch}
      .btns{position:relative;display:flex;gap:10px;justify-content:center;margin-top:26px}
      .btns a{padding:14px 22px;border-radius:12px;font-weight:700;font-size:15px}
      .b1{background:#5D7CFF;color:#fff}
      .b2{border:1px solid rgba(255,255,255,.18)}
      h2{padding:30px 20px 4px;font-size:24px;font-weight:800;letter-spacing:-.02em}
      .sub2{padding:0 20px 16px;color:rgba(237,239,242,.42);font-size:14px}
      .tj{flex:0 0 196px;height:258px;border-radius:20px;position:relative;overflow:hidden;
          box-shadow:0 14px 40px rgba(0,0,0,.5)}
      .obj{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.92}
      .tj::after{content:'';position:absolute;inset:0;
        background:linear-gradient(180deg,rgba(0,0,0,0) 38%,rgba(0,0,0,.86) 100%)}
      .pie{position:absolute;left:0;right:0;bottom:0;padding:0 15px 16px;z-index:2}
      .pie h4{font-size:15.5px;font-weight:700;line-height:1.2}
      .pie p{font-size:11.5px;color:rgba(255,255,255,.55);margin-top:4px}
      footer{padding:34px 20px 40px;color:rgba(237,239,242,.3);font-size:12.5px}
    """
    return pagina(css,
        "<div class=nav><b>AYMOR APPLIS</b><div class=bus>Buscar</div></div>"
        "<div class=hero><h1>Herramientas<br>para quien trabaja<br>por su cuenta.</h1>"
        "<p>Aplicaciones y guías. Nada de relleno.</p>"
        "<div class=btns><a class=b1>Ver el catálogo</a><a class=b2>Cómo funciona</a></div></div>"
        "<h2>Empieza por aquí</h2><p class=sub2>Lo que más se lee este mes</p>"
        "<div class=estante>" + tarjetas(g) + "</div>"
        "<footer>Aymor Applis — Quebec</footer>")


# ===================================================== C · LIBRERIA
def c(g):
    libros = "".join(
        "<a class=lib><div class=sombra></div>"
        "<div class=obj style=\"background-image:url('img/%s-mockup.jpg')\"></div>"
        "<h4>%s</h4><p>%s</p></a>" % (cc, t, cat) for cc, t, cat, color in g[:5])
    css = """
      body{background:#F7F3EC;color:#1A1714;font:16px/1.6 ui-sans-serif,system-ui}
      .nav{display:flex;align-items:center;gap:12px;padding:20px 24px 0}
      .nav b{font-weight:800;font-size:12.5px;letter-spacing:.18em}
      .nav .bus{margin-left:auto;font-size:13px;color:#8C8276}
      h1{padding:30px 24px 0;font:400 42px/1.04 "Iowan Old Style","Palatino Linotype",Georgia,serif;
         letter-spacing:-.015em}
      h1 i{font-style:italic;color:#9C5533}
      .sub{padding:18px 24px 0;color:#7E7467;font-size:15.5px;max-width:30ch}
      .et{padding:40px 24px 18px;font-size:11px;letter-spacing:.22em;color:#A79C8D;font-weight:700}
      .lib{flex:0 0 164px}
      .obj{height:215px;background-size:cover;background-position:center;border-radius:3px;
           box-shadow:0 18px 34px -14px rgba(26,23,20,.55)}
      .lib h4{font:400 17px/1.24 "Iowan Old Style",Georgia,serif;margin-top:16px}
      .lib p{font-size:10.5px;letter-spacing:.17em;text-transform:uppercase;color:#A79C8D;margin-top:7px}
      footer{padding:40px 24px;color:#A79C8D;font-size:13px}
    """
    return pagina(css,
        "<div class=nav><b>AYMOR APPLIS</b><span class=bus>Buscar</span></div>"
        "<h1>Lo que nadie te explicó de <i>tener un negocio</i>.</h1>"
        "<p class=sub>Guías que se leen en una tarde y herramientas que se usan toda la semana.</p>"
        "<div class=et>LAS MÁS LEÍDAS</div>"
        "<div class=estante>" + libros + "</div>"
        "<footer>Aymor Applis — Quebec</footer>")


# ===================================================== D · BANDAS POR OFICIO
def d(g):
    oficios = [("Talleres y cuadrillas", "01_Ley25", "#223B53"),
               ("Detallado de autos", "07_Detallado_Automotriz", "#2B3A67"),
               ("Impuestos y papeles", "08_Cuanto_Apartar", "#1F6F5C"),
               ("Cocina y casa", "05_Fermentos", "#4A6B3A")]
    bandas = "".join(
        "<a class=banda style=\"background-image:linear-gradient(90deg,%s 0%%,%scc 42%%,rgba(0,0,0,.25) 100%%),"
        "url('img/%s-mockup.jpg')\"><span>%s</span><em>Ver lo de este oficio →</em></a>"
        % (col, col, c, n) for n, c, col in oficios)
    css = """
      body{background:#101114;color:#fff;font:16px/1.5 ui-sans-serif,system-ui}
      .nav{display:flex;align-items:center;padding:18px 22px}
      .nav b{font-weight:800;font-size:13px;letter-spacing:.1em}
      .nav span{margin-left:auto;font-size:13px;color:rgba(255,255,255,.5)}
      h1{padding:26px 22px 0;font-size:38px;line-height:1.04;font-weight:800;letter-spacing:-.035em}
      .sub{padding:16px 22px 26px;color:rgba(255,255,255,.55);font-size:15.5px;max-width:29ch}
      .banda{display:block;position:relative;height:138px;background-size:cover;background-position:center;
             padding:22px;margin-bottom:3px}
      .banda span{display:block;font-size:23px;font-weight:800;letter-spacing:-.02em;line-height:1.1;max-width:14ch}
      .banda em{position:absolute;left:22px;bottom:20px;font-style:normal;font-size:13px;
                color:rgba(255,255,255,.72);font-weight:600}
      footer{padding:30px 22px 40px;color:rgba(255,255,255,.35);font-size:13px}
    """
    return pagina(css,
        "<div class=nav><b>AYMOR APPLIS</b><span>Buscar</span></div>"
        "<h1>Escoge a qué<br>te dedicas.</h1>"
        "<p class=sub>Te enseñamos solo lo tuyo: apps y guías de tu oficio.</p>"
        + bandas + "<footer>Aymor Applis — Quebec</footer>")


NOMBRES = {1: "A · CLARA, CON AIRE", 2: "B · OSCURA, DE NOCHE",
           3: "C · DE LIBRERIA", 4: "D · POR OFICIO"}


def main():
    g = traer()
    if len(g) < 5:
        print("   ALTO: solo %d imagenes" % len(g))
        sys.exit(1)
    print("   %d guias con imagen propia" % len(g))
    for n, f in ((1, a), (2, b), (3, c), (4, d)):
        io.open(os.path.join(AQUI, "propuesta-%d.html" % n), "w",
                encoding="utf-8", newline="\n").write(f(g))
    print("   cuatro portadas escritas")

    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image, ImageDraw
    except ImportError:
        print("   (sin playwright no saco las fotos)")
        return
    fotos = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pag = nav.new_page(viewport={"width": 420, "height": 880}, device_scale_factor=2)
        for n in range(1, 5):
            pag.goto("file:///" + os.path.join(AQUI, "propuesta-%d.html" % n)
                     .replace("\\", "/").replace(" ", "%20"))
            pag.wait_for_timeout(900)
            dd = os.path.join(AQUI, "propuesta-%d.png" % n)
            pag.screenshot(path=dd)
            fotos.append(dd)
        nav.close()
    alto = 860
    ims = [Image.open(f).convert("RGB") for f in fotos]
    ims = [im.resize((int(im.width * alto / im.height), alto)) for im in ims]
    ancho = sum(im.width for im in ims) + 20 * (len(ims) + 1)
    hoja = Image.new("RGB", (ancho, alto + 62), (250, 250, 249))
    dib = ImageDraw.Draw(hoja)
    x = 20
    for i, im in enumerate(ims, 1):
        hoja.paste(im, (x, 50))
        dib.text((x + 4, 22), NOMBRES[i], fill=(17, 17, 20))
        x += im.width + 20
    hoja.save(os.path.join(AQUI, "las-propuestas.png"))
    print("   hoja: _disenos/las-propuestas.png")


if __name__ == "__main__":
    main()
