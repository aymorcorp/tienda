# -*- coding: utf-8 -*-
"""
LA TIENDA — PRIMERA VERSION DE VERDAD (C + D)
=============================================

    python _disenos/hacer-la-tienda.py

La direccion escogio «entre la C y la D», asi que esto junta las dos:

  - de la D: la portada se navega POR OFICIO, en bandas de ancho completo, una
    por oficio, con su foto. Nada de rejillas.
  - de la C: dentro, el catalogo es una libreria -- letra con remates, color
    papel, y cada producto puesto como un objeto con su sombra.

LO QUE PIDIO, Y COMO SE CUMPLE

  «Que sirva para telefono, tableta y computadora, de Apple y de Android»
      Una sola pagina que se acomoda sola. No hay version movil aparte: el
      mismo archivo se lee bien de 320 puntos de ancho hasta una pantalla
      grande. Las medidas de letra crecen solas con clamp(), y las rejillas
      cambian de columnas segun quepa. Funciona en Safari de iPhone y iPad,
      en Chrome de Android y en cualquier navegador de computadora: no se usa
      nada que solo tenga uno.

  «Que se deslice con el dedo»
      Los estantes se arrastran con el dedo y se frenan en cada tarjeta
      (scroll-snap), que es lo que hace el telefono de forma natural. Sin
      programas detras: lo hace el propio navegador, asi que no se traba ni
      gasta bateria. Con raton tambien se arrastra, y ademas hay flechas.

  «Le picas a una foto y te despliega otra pagina con mas fotos y toda la
   informacion»
      Cada tarjeta lleva a la pagina del producto: galeria de fotos que se
      pasan con el dedo, lo que es, para quien, que trae dentro, el precio y
      el boton. El boton todavia no cobra -- el telon esta abajo.

Las imagenes son NUESTRAS. Cuando lleguen las fotos compradas, se cambian en
un solo sitio.

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

OFICIOS = [
    ("Talleres y cuadrillas", "01_Ley25", "#1E3348"),
    ("Detallado de autos", "07_Detallado_Automotriz", "#23305A"),
    ("Impuestos y papeles", "08_Cuanto_Apartar", "#1C5B4C"),
    ("Cocina y casa", "05_Fermentos", "#3F5C32"),
    ("Buscar trabajo", "11_Curriculum", "#4A3160"),
]
GUIAS_LISTA = [
    ("01_Ley25", "La Ley 25, explicada", "Ley y papeles"),
    ("08_Cuanto_Apartar", "Cuánto apartar para impuestos", "Impuestos"),
    ("03_CNESST", "La CNESST sin sustos", "Ley y papeles"),
    ("04_7Errores", "Los 7 errores", "Negocio"),
    ("07_Detallado_Automotriz", "Detallado automotriz", "Oficios"),
    ("05_Fermentos", "Fermentos en casa", "Casa"),
    ("11_Curriculum", "Tu currículum", "Trabajo"),
    ("13_Creditos_Ayudas", "Créditos y ayudas", "Negocio"),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --papel:#F7F3EC; --tinta:#1A1714; --suave:#7E7467; --tenue:#A79C8D;
  --marca:#9C5533; --linea:#E6DED1; --blanco:#FFFDF9;
  --ancho:1180px;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
html{-webkit-text-size-adjust:100%}
body{background:var(--papel);color:var(--tinta);font:16px/1.6 var(--sans);
     -webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}
a{color:inherit;text-decoration:none;-webkit-tap-highlight-color:transparent}
.centro{max-width:var(--ancho);margin:0 auto;padding:0 clamp(18px,4vw,40px)}

/* ---------- barra de arriba ---------- */
.barra{position:sticky;top:0;z-index:50;background:rgba(247,243,236,.86);
       backdrop-filter:saturate(1.6) blur(12px);border-bottom:1px solid var(--linea)}
.barra .centro{display:flex;align-items:center;gap:clamp(10px,2vw,20px);
               min-height:58px;padding-top:9px;padding-bottom:9px}
.marca{font-weight:800;font-size:12.5px;letter-spacing:.17em;white-space:nowrap}
.buscar{flex:1;min-width:0;display:flex;align-items:center;gap:8px;background:var(--blanco);
        border:1px solid var(--linea);border-radius:999px;padding:9px 15px;color:var(--tenue);font-size:14px}
.idiomas{display:flex;gap:4px}
.idiomas b{font-size:11.5px;letter-spacing:.08em;color:var(--tenue);padding:5px 7px;border-radius:7px;font-weight:700}
.idiomas b.on{background:var(--tinta);color:var(--papel)}

/* ---------- portada ---------- */
.saludo{padding:clamp(34px,7vw,74px) 0 clamp(20px,4vw,34px)}
.saludo h1{font:400 clamp(32px,7.4vw,62px)/1.04 var(--serif);letter-spacing:-.015em;max-width:17ch}
.saludo h1 i{font-style:italic;color:var(--marca)}
.saludo p{margin-top:clamp(14px,2.4vw,22px);color:var(--suave);
          font-size:clamp(15px,1.7vw,19px);max-width:46ch}

/* ---------- bandas por oficio (de la D) ---------- */
.oficios{display:grid;gap:3px;margin-top:clamp(18px,3vw,30px)}
@media(min-width:900px){.oficios{grid-template-columns:1fr 1fr}}
.of{position:relative;display:flex;flex-direction:column;justify-content:flex-end;
    min-height:clamp(132px,21vw,230px);padding:clamp(16px,2.4vw,26px);overflow:hidden;color:#fff}
.of .fondo{position:absolute;inset:0;background-size:cover;background-position:center;
           transform:scale(1.02);transition:transform .5s ease}
.of:hover .fondo{transform:scale(1.07)}
.of .velo{position:absolute;inset:0}
.of h3{position:relative;font-size:clamp(18px,2.4vw,27px);font-weight:800;letter-spacing:-.02em;
       line-height:1.12;max-width:13ch}
.of span{position:relative;margin-top:7px;font-size:13.5px;color:rgba(255,255,255,.78);font-weight:600}

/* ---------- estante que se arrastra con el dedo ---------- */
.titulo{display:flex;align-items:baseline;gap:14px;padding:clamp(34px,5vw,56px) 0 clamp(14px,2vw,20px)}
.titulo h2{font:400 clamp(23px,3.1vw,34px)/1.1 var(--serif);letter-spacing:-.01em}
.titulo span{color:var(--tenue);font-size:13.5px}
.estante{display:flex;gap:clamp(14px,2vw,26px);overflow-x:auto;padding-bottom:10px;
         scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;
         scrollbar-width:none;scroll-padding-left:clamp(18px,4vw,40px)}
.estante::-webkit-scrollbar{display:none}
.estante>*{scroll-snap-align:start;flex:0 0 clamp(146px,37vw,210px)}
.libro .obj{aspect-ratio:4/3;background-size:cover;background-position:center;border-radius:4px;
            box-shadow:0 22px 38px -18px rgba(26,23,20,.6);transition:transform .35s ease}
.libro:hover .obj{transform:translateY(-5px)}
.libro h4{font:400 clamp(15px,1.7vw,19px)/1.25 var(--serif);margin-top:14px}
.libro p{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--tenue);margin-top:6px}
.libro b{display:block;margin-top:7px;font-size:14px;font-weight:700}

/* ---------- pie ---------- */
footer{margin-top:clamp(40px,7vw,86px);border-top:1px solid var(--linea);
       padding:clamp(28px,4vw,46px) 0 clamp(34px,5vw,56px);color:var(--suave);font-size:14px}
.cols{display:grid;gap:clamp(22px,3vw,30px);grid-template-columns:1fr 1fr}
@media(min-width:760px){.cols{grid-template-columns:repeat(4,1fr)}}
.cols h5{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--tenue);
         margin-bottom:11px;font-weight:700}
.cols a{display:block;padding:4px 0;font-size:14.5px}
.cierre{margin-top:clamp(26px,4vw,40px);padding-top:18px;border-top:1px solid var(--linea);
        color:var(--tenue);font-size:13px}

/* ---------- pagina de producto ---------- */
.volver{padding-top:clamp(16px,3vw,26px);font-size:14px;color:var(--suave);font-weight:600}
.ficha{display:grid;gap:clamp(22px,4vw,46px);padding-top:clamp(16px,3vw,26px)}
@media(min-width:880px){.ficha{grid-template-columns:1.05fr .95fr;align-items:start}}
.galeria{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
         -webkit-overflow-scrolling:touch;scrollbar-width:none;border-radius:6px}
.galeria::-webkit-scrollbar{display:none}
.galeria img{scroll-snap-align:center;flex:0 0 100%;border-radius:6px;
             box-shadow:0 22px 44px -22px rgba(26,23,20,.55)}
.puntos{display:flex;gap:6px;justify-content:center;margin-top:13px}
.puntos i{width:6px;height:6px;border-radius:50%;background:var(--tenue);opacity:.4}
.puntos i.on{opacity:1;background:var(--tinta)}
.ficha h1{font:400 clamp(27px,4.2vw,44px)/1.07 var(--serif);letter-spacing:-.015em}
.ficha .cat{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--tenue);margin-bottom:12px}
.ficha .lead{margin-top:16px;color:var(--suave);font-size:clamp(15px,1.7vw,17.5px)}
.precio{display:flex;align-items:baseline;gap:10px;margin-top:clamp(18px,3vw,28px)}
.precio b{font-size:clamp(25px,3.4vw,33px);font-weight:800;letter-spacing:-.02em}
.precio span{color:var(--tenue);font-size:13.5px}
.comprar{display:block;margin-top:16px;background:var(--tinta);color:var(--papel);text-align:center;
         font-weight:700;font-size:16px;padding:16px;border-radius:12px}
.telon{margin-top:10px;font-size:13px;color:var(--tenue);text-align:center}
.trae{margin-top:clamp(22px,3.4vw,32px);border-top:1px solid var(--linea);padding-top:18px}
.trae h3{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--tenue)}
.trae ul{margin-top:12px;display:grid;gap:9px}
.trae li{list-style:none;padding-left:20px;position:relative;font-size:15px}
.trae li::before{content:'';position:absolute;left:0;top:9px;width:7px;height:7px;
                 border-radius:50%;background:var(--marca)}
"""


def traer():
    os.makedirs(IMG, exist_ok=True)
    for carpeta, *_ in GUIAS_LISTA:
        for origen, mote in (("MOCKUP_3D.jpg", "mockup"), ("ES/COVER_1280x720.jpg", "cover"),
                             ("ES/THUMB_600x600.jpg", "thumb")):
            o = os.path.join(GUIAS, carpeta, *origen.split("/"))
            d = os.path.join(IMG, "%s-%s.jpg" % (carpeta, mote))
            if os.path.exists(o) and not os.path.exists(d):
                shutil.copy2(o, d)


def marco(titulo, cuerpo):
    return ("<!doctype html><html lang=es><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1,viewport-fit=cover'>"
            "<title>%s</title><style>%s</style></head><body>"
            "<div class=barra><div class=centro><span class=marca>AYMOR APPLIS</span>"
            "<span class=buscar>Buscar en el catálogo</span>"
            "<span class=idiomas><b>FR</b><b class=on>ES</b><b>EN</b></span></div></div>"
            "%s"
            "<footer><div class=centro><div class=cols>"
            "<div><h5>La tienda</h5><a>Todo el catálogo</a><a>Aplicaciones</a>"
            "<a>Guías y libros</a><a>Por oficio</a></div>"
            "<div><h5>Tu cuenta</h5><a>Mi membresía</a><a>Volver a bajar lo que compré</a>"
            "<a>Mis facturas</a></div>"
            "<div><h5>Aymor Applis</h5><a>Quiénes somos</a>"
            "<a>Trabaja con nosotros</a><a>Sé probador de nuestras apps</a>"
            "<a>Escríbenos</a></div>"
            "<div><h5>Lo legal</h5><a>Precios</a><a>Términos</a><a>Privacidad</a>"
            "<a>Reembolsos</a></div></div>"
            "<p class=cierre>Aymor Applis — un negocio registrado en Quebec · "
            "aymorcorp@gmail.com</p>"
            "</div></footer></body></html>" % (titulo, CSS, cuerpo))


def portada():
    bandas = "".join(
        "<a class=of href='producto.html'>"
        "<div class=fondo style=\"background-image:url('img/%s-mockup.jpg')\"></div>"
        "<div class=velo style=\"background:linear-gradient(170deg,%s66 0%%,%sE6 78%%)\"></div>"
        "<h3>%s</h3><span>Ver lo de este oficio →</span></a>" % (c, col, col, n)
        for n, c, col in OFICIOS)
    libros = "".join(
        "<a class=libro href='producto.html'>"
        "<div class=obj style=\"background-image:url('img/%s-mockup.jpg')\"></div>"
        "<h4>%s</h4><p>%s</p><b>9.99 USD</b></a>" % (c, t, cat)
        for c, t, cat in GUIAS_LISTA)
    return marco("Aymor Applis",
        "<div class=centro><div class=saludo>"
        "<h1>Lo que nadie te explicó de <i>tener un negocio</i>.</h1>"
        "<p>Guías que se leen en una tarde y aplicaciones que se usan toda la semana. "
        "Hechas en Quebec, en el idioma en que trabajas.</p></div></div>"
        "<div class=centro><div class=oficios>" + bandas + "</div>"
        "<div class=titulo><h2>Las más leídas</h2><span>Arrástralas con el dedo</span></div></div>"
        "<div class=estante style='padding-left:clamp(18px,4vw,40px);padding-right:clamp(18px,4vw,40px)'>"
        + libros + "</div>")


def producto():
    c = "01_Ley25"
    fotos = "".join("<img src='img/%s-%s.jpg' alt=''>" % (c, m)
                    for m in ("mockup", "cover", "thumb"))
    trae = ["Las 9 obligaciones, una por una, con lo que te toca hacer",
            "Qué pasa si te cae una queja, y qué contestar",
            "Los textos que puedes copiar: aviso, consentimiento y respuesta",
            "Qué guardar y por cuánto tiempo",
            "En PDF y EPUB, en español, inglés y francés"]
    return marco("La Ley 25, explicada — Aymor Applis",
        "<div class=centro><div class=volver>← Volver a Ley y papeles</div>"
        "<div class=ficha><div>"
        "<div class=galeria>" + fotos + "</div>"
        "<div class=puntos><i class=on></i><i></i><i></i></div></div>"
        "<div><div class=cat>Ley y papeles · Guía</div>"
        "<h1>La Ley 25, explicada</h1>"
        "<p class=lead>Qué te obliga de verdad la ley de privacidad de Quebec si tienes un "
        "negocio chico, dicho sin palabras de abogado, y qué tienes que hacer esta semana.</p>"
        "<div class=precio><b>9.99 USD</b><span>pago único · PDF y EPUB</span></div>"
        "<a class=comprar>Comprar</a>"
        "<p class=telon>El botón se enciende cuando la dirección abra la tienda.</p>"
        "<div class=trae><h3>Qué trae dentro</h3><ul>"
        + "".join("<li>%s</li>" % x for x in trae) +
        "</ul></div></div></div></div>")


def main():
    traer()
    io.open(os.path.join(AQUI, "tienda.html"), "w", encoding="utf-8",
            newline="\n").write(portada())
    io.open(os.path.join(AQUI, "producto.html"), "w", encoding="utf-8",
            newline="\n").write(producto())
    print("   escritas tienda.html y producto.html")

    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image, ImageDraw
    except ImportError:
        print("   (sin playwright no saco las fotos)")
        return

    MEDIDAS = [("Teléfono", 390, 844), ("Tableta", 834, 1000), ("Computadora", 1440, 900)]
    hechas = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for etiqueta, an, al in MEDIDAS:
            pag = nav.new_page(viewport={"width": an, "height": al}, device_scale_factor=2)
            pag.goto("file:///" + os.path.join(AQUI, "tienda.html")
                     .replace("\\", "/").replace(" ", "%20"))
            pag.wait_for_timeout(900)
            d = os.path.join(AQUI, "_t-%s.png" % an)
            pag.screenshot(path=d)
            hechas.append((etiqueta + " " + str(an), d))
            pag.close()
        pag = nav.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pag.goto("file:///" + os.path.join(AQUI, "producto.html")
                 .replace("\\", "/").replace(" ", "%20"))
        pag.wait_for_timeout(900)
        d = os.path.join(AQUI, "_p-390.png")
        pag.screenshot(path=d)
        hechas.append(("Producto, teléfono", d))
        pag.close()
        nav.close()

    alto = 820
    ims = []
    for etiqueta, f in hechas:
        im = Image.open(f).convert("RGB")
        ims.append((etiqueta, im.resize((int(im.width * alto / im.height), alto))))
    ancho = sum(im.width for _, im in ims) + 20 * (len(ims) + 1)
    hoja = Image.new("RGB", (ancho, alto + 60), (250, 249, 246))
    dib = ImageDraw.Draw(hoja)
    x = 20
    for etiqueta, im in ims:
        hoja.paste(im, (x, 48))
        dib.text((x + 4, 20), etiqueta, fill=(26, 23, 20))
        x += im.width + 20
    hoja.save(os.path.join(AQUI, "la-tienda.png"))
    for _, f in hechas:
        os.remove(f)
    print("   hoja: _disenos/la-tienda.png")


if __name__ == "__main__":
    main()
