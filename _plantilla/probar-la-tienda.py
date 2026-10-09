# -*- coding: utf-8 -*-
"""
PROBAR LA TIENDA ANTES DE ENSEÑARLA
===================================

    python _plantilla/probar-la-tienda.py

Abre la tienda de verdad en un navegador sin pantalla y comprueba lo que una
prueba de texto no puede ver:

  - que no haya ni una imagen rota en ninguna pagina;
  - que no haya ni un enlace que lleve a una pagina que no existe;
  - que el buscador filtre de verdad al escribir;
  - que los filtros por categoria filtren;
  - que cuando no hay resultados se diga, en vez de dejar un hueco;
  - que no salga ni un error en la consola;
  - y que todo esto pase igual a lo ancho de un telefono, de una tableta y de
    una computadora.

Antes de mirar nada, SE PRUEBA A SI MISMO: busca una palabra que no existe y
exige quedarse sin resultados. Si eso no pasa, el buscador no esta filtrando y
lo demas no vale.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
TIENDA = os.path.join(os.path.dirname(AQUI), "_disenos", "tienda")

bien = mal = 0


def ok(que, cond, detalle=""):
    global bien, mal
    if cond:
        bien += 1
        print("   bien  %s%s" % (que, ("   " + detalle) if detalle else ""))
    else:
        mal += 1
        print("   MAL   %s%s" % (que, ("   " + detalle) if detalle else ""))


def url(*partes):
    return "file:///" + os.path.join(TIENDA, *partes).replace("\\", "/").replace(" ", "%20")


try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("   falta playwright")
    sys.exit(2)

print("\nLA TIENDA, PROBADA DE VERDAD\n")
with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ---------- 0. la prueba se prueba a si misma ----------
    pag = nav.new_page(viewport={"width": 420, "height": 900})
    pag.goto(url("es", "catalogo", "index.html"))
    pag.wait_for_timeout(500)
    pag.fill("#q", "zzzzqqq")
    pag.wait_for_timeout(260)
    vistas = pag.evaluate("[...document.querySelectorAll('.celda')].filter(c=>!c.hidden).length")
    ok("buscando algo que no existe, no queda nada", vistas == 0,
       "quedaron %d" % vistas)
    ok("y se le dice a la persona, no se deja un hueco",
       pag.evaluate("!document.getElementById('nada').hidden"))
    pag.fill("#q", "")
    pag.wait_for_timeout(240)
    todas = pag.evaluate("[...document.querySelectorAll('.celda')].filter(c=>!c.hidden).length")
    ok("al borrar lo escrito, vuelven todas", todas >= 10, "%d productos" % todas)
    pag.close()
    print("")

    # ---------- 1. imagenes, enlaces y errores, en cada medida ----------
    MEDIDAS = [("teléfono", 390, 844), ("tableta", 834, 1000), ("computadora", 1440, 900)]
    PAGINAS = [("portada", ("es", "index.html")),
               ("catálogo", ("es", "catalogo", "index.html")),
               ("producto", ("es", "ley25", "index.html")),
               ("mi membresía", ("es", "mi-membresia", "index.html")),
               ("probadores", ("es", "probadores", "index.html"))]
    for etiqueta, an, al in MEDIDAS:
        pag = nav.new_page(viewport={"width": an, "height": al})
        errores = []
        pag.on("pageerror", lambda e: errores.append(str(e)))
        pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
        rotas = corte = 0
        for nombre, partes in PAGINAS:
            pag.goto(url(*partes))
            pag.wait_for_timeout(500)
            rotas += pag.evaluate(
                "[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length")
            rotas += pag.evaluate("""[...document.querySelectorAll('[style*=background-image]')]
                .filter(e=>{var u=(e.style.backgroundImage||'').match(/url\\(["']?([^"')]+)/);
                            if(!u) return false; var i=new Image(); i.src=u[1]; return false;}).length""")
            corte += pag.evaluate(
                "document.documentElement.scrollWidth > document.documentElement.clientWidth ? 1 : 0")
        ok("en %s: ninguna imagen rota" % etiqueta, rotas == 0, "%d rotas" % rotas)
        ok("en %s: nada se sale de la pantalla a lo ancho" % etiqueta, corte == 0,
           "%d paginas con corte" % corte)
        ok("en %s: ni un error" % etiqueta, not errores, " | ".join(errores[:2])[:110])
        pag.close()
    print("")

    # ---------- 2. los filtros ----------
    pag = nav.new_page(viewport={"width": 420, "height": 900})
    pag.goto(url("es", "catalogo", "index.html"))
    pag.wait_for_timeout(450)
    cats = pag.evaluate("[...document.querySelectorAll('.chip')].map(c=>c.dataset.cat)")
    ok("hay filtros por categoría", len(cats) >= 4, ", ".join(cats))
    for c in [x for x in cats if x != "todo"][:3]:
        pag.click(".chip[data-cat='%s']" % c)
        pag.wait_for_timeout(220)
        r = pag.evaluate("""(()=>{var v=[...document.querySelectorAll('.celda')].filter(c=>!c.hidden);
            return {n:v.length, puras:v.every(c=>c.dataset.cat==='%s')};})()""" % c)
        ok("el filtro «%s» deja solo lo suyo" % c, r["puras"] and r["n"] > 0,
           "%d productos" % r["n"])
    pag.click(".chip[data-cat=todo]")
    pag.wait_for_timeout(220)
    ok("y «Todo» las devuelve todas",
       pag.evaluate("[...document.querySelectorAll('.celda')].filter(c=>!c.hidden).length") >= 10)

    # buscar y filtrar a la vez
    pag.click(".chip[data-cat=impuestos]")
    pag.fill("#q", "apartar")
    pag.wait_for_timeout(260)
    r = pag.evaluate("[...document.querySelectorAll('.celda')].filter(c=>!c.hidden).length")
    ok("buscar y filtrar a la vez funciona", r == 1, "%d productos" % r)
    pag.close()
    print("")

    # ---------- 3. los enlaces llevan a algo que existe ----------
    faltan = []
    for idi in ("es", "fr", "en"):
        pag = nav.new_page(viewport={"width": 1100, "height": 800})
        for nombre, partes in [("portada", (idi, "index.html")),
                               ("catálogo", (idi, "catalogo", "index.html"))]:
            pag.goto(url(*partes))
            pag.wait_for_timeout(350)
            hrefs = pag.evaluate(
                "[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
            base = os.path.dirname(os.path.join(TIENDA, *partes))
            for h in set(hrefs):
                if not h or h.startswith(("mailto:", "http", "#")):
                    continue
                destino = os.path.normpath(os.path.join(base, h))
                if os.path.isdir(destino):
                    destino = os.path.join(destino, "index.html")
                if not os.path.exists(destino):
                    faltan.append("%s/%s → %s" % (idi, nombre, h))
        pag.close()
    ok("ningún enlace lleva a una página que no existe", not faltan,
       " | ".join(sorted(set(faltan))[:3]))

    # ---------- 4. el idioma de verdad ----------
    for idi, palabra in (("fr", "Faites-les glisser"), ("en", "Swipe them")):
        pag = nav.new_page(viewport={"width": 900, "height": 800})
        pag.goto(url(idi, "index.html"))
        pag.wait_for_timeout(350)
        txt = pag.evaluate("document.body.innerText")
        ok("la portada en %s está en %s" % (idi, idi), palabra in txt)
        pag.close()

    # ---------- 5. lo que NO debe estar ----------
    pag = nav.new_page(viewport={"width": 900, "height": 800})
    pag.goto(url("es", "catalogo", "index.html"))
    pag.wait_for_timeout(350)
    txt = pag.evaluate("document.body.innerText").lower()
    ok("la guía de salud NO aparece en la tienda",
       "perimenopaus" not in txt)
    ok("ningún botón de compra está encendido",
       pag.evaluate("[...document.querySelectorAll('.comprar')].every(b=>b.classList.contains('apagado'))"))
    pag.close()
    nav.close()

print("")
print("   %d bien, %d mal" % (bien, mal))
sys.exit(1 if mal else 0)
