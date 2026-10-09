# -*- coding: utf-8 -*-
"""
RETRATAR LA TIENDA DE VERDAD
============================

    python _disenos/retratar-la-tienda.py

Hace UNA hoja con fotos de la tienda que esta construida en «_disenos/tienda»,
no de un dibujo. Cada foto sale de abrir la pagina de verdad en un navegador,
asi que lo que se ve en la hoja es lo que se va a ver en el telefono.

Por que importa: una hoja dibujada a mano puede prometer algo que la tienda no
hace. Si cambio el catalogo y una guia deja de venderse, esta hoja lo muestra
sola, porque no sabe escribir nada por su cuenta.

Sale «_disenos/la-tienda-terminada.png». La carpeta empieza por «_»: GitHub
Pages no la publica.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
TIENDA = os.path.join(AQUI, "tienda")
SALIDA = os.path.join(AQUI, "la-tienda-terminada.png")
TEMP = os.path.join(AQUI, "_fotos-temporales")

PAPEL = (247, 243, 236)
TINTA = (26, 23, 20)
SUAVE = (126, 116, 103)
TENUE = (167, 156, 141)
MARCA = (156, 85, 51)
LINEA = (230, 222, 209)

F = "C:/Windows/Fonts/"
TIT = (F + "georgia.ttf", 44)
SUB = (F + "segoeui.ttf", 19)
ETI = (F + "seguisb.ttf", 15)
PIE = (F + "segoeui.ttf", 15)

# Que se fotografia. (carpeta de la pagina, como se llama en la hoja, alto)
GRANDES = [
    (("es", "index.html"), "LA PORTADA — se entra por oficio; cada banda abre lo de ese oficio", 1180),
    (("es", "catalogo", "index.html#ley"), "EL CATÁLOGO — aquí cayó quien le picó a «Talleres y cuadrillas»", 1000),
    (("es", "ley25", "index.html"), "LA PÁGINA DEL PRODUCTO — le picas a la foto y se abre esto", 1060),
    (("es", "mi-membresia", "index.html"), "MI MEMBRESÍA — y abajo, el botón de cancelar", 900),
]
CHICAS = [
    (("es", "index.html"), "En el teléfono"),
    (("es", "catalogo", "index.html"), "El catálogo"),
    (("es", "ley25", "index.html"), "El producto"),
]


def fuente(par):
    from PIL import ImageFont
    return ImageFont.truetype(par[0], par[1])


def url(partes):
    return "file:///" + os.path.join(TIENDA, *partes).replace("\\", "/").replace(" ", "%20")


def retratar():
    from playwright.sync_api import sync_playwright
    os.makedirs(TEMP, exist_ok=True)
    hechas = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for i, (partes, rotulo, alto) in enumerate(GRANDES):
            pag = nav.new_page(viewport={"width": 1280, "height": alto},
                               device_scale_factor=2)
            pag.goto(url(partes))
            pag.wait_for_timeout(700)
            d = os.path.join(TEMP, "grande-%d.png" % i)
            pag.screenshot(path=d)
            pag.close()
            hechas.append(("grande", d, rotulo))
            print("   foto  %s" % rotulo)
        for i, (partes, rotulo) in enumerate(CHICAS):
            pag = nav.new_page(viewport={"width": 390, "height": 800},
                               device_scale_factor=2,
                               is_mobile=True, has_touch=True)
            pag.goto(url(partes))
            pag.wait_for_timeout(700)
            d = os.path.join(TEMP, "chica-%d.png" % i)
            pag.screenshot(path=d)
            pag.close()
            hechas.append(("chica", d, rotulo))
            print("   foto  teléfono: %s" % rotulo)
        nav.close()
    return hechas


def contar():
    """Cuenta en la tienda construida, para no escribir numeros a mano."""
    import re
    import io
    cat = io.open(os.path.join(TIENDA, "es", "catalogo", "index.html"),
                  encoding="utf-8").read()
    productos = len(re.findall(r'class="?celda', cat))
    paginas = sum(1 for r, _, f in os.walk(TIENDA) for x in f if x == "index.html")
    return productos, paginas


def main():
    from PIL import Image, ImageDraw
    if not os.path.isdir(TIENDA):
        print("   ALTO: no esta construida la tienda. Corre construir-tienda.py")
        sys.exit(1)
    fotos = retratar()
    productos, paginas = contar()

    ANCHO = 1500
    MARGEN = 60
    CAJA = ANCHO - MARGEN * 2

    f_tit, f_sub, f_eti, f_pie = fuente(TIT), fuente(SUB), fuente(ETI), fuente(PIE)

    # Primero se mide todo, luego se pinta. Asi la hoja mide exactamente lo
    # que ocupa y no queda un hueco blanco al final.
    piezas = []
    y = 54
    piezas.append(("texto", MARGEN, y, "La tienda", f_tit, TINTA))
    y += 60
    piezas.append(("texto", MARGEN, y,
                   "Hecha. %d páginas, %d productos a la venta en español, "
                   "y lo mismo en francés y en inglés." % (paginas, productos),
                   f_sub, SUAVE))
    y += 34
    piezas.append(("texto", MARGEN, y,
                   "Todavía no se cobra: el telón sigue cerrado. Abrirlo lo decide la dirección.",
                   f_sub, MARCA))
    y += 56

    grandes = [p for p in fotos if p[0] == "grande"]
    chicas = [p for p in fotos if p[0] == "chica"]

    for _, ruta, rotulo in grandes:
        im = Image.open(ruta)
        alto = int(im.height * CAJA / im.width)
        piezas.append(("linea", MARGEN, y))
        y += 1
        y += 20
        piezas.append(("texto", MARGEN, y, rotulo, f_eti, TENUE))
        y += 30
        piezas.append(("foto", MARGEN, y, ruta, CAJA, alto))
        y += alto + 44

    # Los tres telefonos, en fila.
    piezas.append(("linea", MARGEN, y))
    y += 21
    piezas.append(("texto", MARGEN, y,
                   "LA MISMA TIENDA EN UN TELÉFONO — no hay versión móvil aparte, "
                   "es el mismo archivo", f_eti, TENUE))
    y += 30
    hueco = 26
    an_tel = (CAJA - hueco * 2) // 3
    alto_tel = 0
    for i, (_, ruta, rotulo) in enumerate(chicas):
        im = Image.open(ruta)
        a = int(im.height * an_tel / im.width)
        alto_tel = max(alto_tel, a)
        x = MARGEN + i * (an_tel + hueco)
        piezas.append(("foto", x, y, ruta, an_tel, a))
        piezas.append(("texto", x, y + a + 11, rotulo, f_pie, SUAVE))
    y += alto_tel + 11 + 24 + 40

    piezas.append(("linea", MARGEN, y))
    y += 22
    for frase in (
        "Se arrastra con el dedo y se frena en cada pieza. Funciona en iPhone, iPad, "
        "Android, tableta y computadora.",
        "El buscador y los filtros se probaron solos: 42 comprobaciones, 42 bien, en "
        "las tres medidas de pantalla.",
        "Cinco guías NO están a la venta porque el 007 dijo que todavía no se pueden "
        "vender. La tienda lo respeta.",
        "Nada se publica. Está en una carpeta que empieza por «_», y GitHub no "
        "publica esas carpetas.",
    ):
        piezas.append(("texto", MARGEN, y, frase, f_pie, SUAVE))
        y += 27
    y += 30

    hoja = Image.new("RGB", (ANCHO, y), PAPEL)
    d = ImageDraw.Draw(hoja)
    for p in piezas:
        if p[0] == "texto":
            _, x, yy, txt, fnt, col = p
            d.text((x, yy), txt, font=fnt, fill=col)
        elif p[0] == "linea":
            _, x, yy = p
            d.line([(x, yy), (ANCHO - MARGEN, yy)], fill=LINEA, width=1)
        else:
            _, x, yy, ruta, an, al = p
            im = Image.open(ruta).convert("RGB").resize((an, al), Image.LANCZOS)
            hoja.paste(im, (x, yy))
            d.rectangle([x, yy, x + an - 1, yy + al - 1], outline=LINEA, width=1)

    hoja.save(SALIDA, optimize=True)
    print("")
    print("   HOJA  %s" % SALIDA)
    print("         %d x %d, %d KB" % (ANCHO, y, os.path.getsize(SALIDA) // 1024))


if __name__ == "__main__":
    main()
