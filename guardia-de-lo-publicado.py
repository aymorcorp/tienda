# -*- coding: utf-8 -*-
"""
EL GUARDIA DE LO PUBLICADO
==========================
Revisa TODAS las paginas de la tienda contra las reglas de la casa. Se corre
antes de subir y despues de subir.

   python guardia-de-lo-publicado.py            revisa los archivos de aqui
   python guardia-de-lo-publicado.py --en-vivo   los baja de internet y revisa

POR QUE EXISTE. El 8 de octubre de 2026 la direccion encontro que la politica
de privacidad PUBLICADA de Aymor Cuisine decia «el tope de carbohidratos por
comida del modo diabetes»: nombraba una enfermedad como funcion del producto.
Mis comprobaciones de entonces miraban idiomas, enlaces, precios y nombres,
pero NO palabras de salud. Sus palabras: «se supone que te aprendiste que no
puede haber nada que sea de salud. Hazte responsable».

Un guardia en un solo sitio en vez de la misma prueba copiada en cinco
generadores: el dia que haya una regla nueva se agrega aqui y vale para todas.

LAS SEIS REGLAS
   1. Nada de salud ni de dieta.           Ni enfermedades, ni regimenes.
   2. Ningun precio fuera de .00/.50/.99.  Regla de la direccion del 7 de oct.
   3. Ni el nombre ni el telefono ni el domicilio de la direccion.
      SALVO en los Terminos de una app que se venda a PERSONAS: ahi la ley de
      consumo de Quebec los exige y van a proposito (capitulo 6 del libro).
   4. Google Play no se menciona.           Solo Apple y nuestra pagina.
   5. Ninguna pagina de soporte nombra a Paddle ni dice como se paga.
   6. Ni formularios ni cajas de pago en las paginas legales.

CADA REGLA SE PRUEBA A SI MISMA antes de valer: al final se le da un texto que
DEBE cazar y otro que debe dejar pasar. Un guardia que no sabe decir «no» no
sirve de nada.
"""
import io
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = "https://aymorcorp.github.io/tienda/"
EN_VIVO = "--en-vivo" in sys.argv

SALUD = re.compile(
    r"diabet|insulin|glucem|glyc|colesterol|cholest|hipertens|presi[oó]n arterial|"
    r"blood pressure|dieta\b|diet\b|r[eé]gimen|adelgaz|weight loss|perder peso|keto|"
    r"cetog|ayuno|fasting|celi[aá]|celiac|intoleran", re.I)
# «medico», «enfermedad», «salud» y «alergia» NO entran en la lista negra: en un
# aviso que dice «esto no es consejo medico» o «si tienes alergia, consulta a tu
# profesional de la salud» esas palabras PROTEGEN al cliente. Lo que no se
# permite es nombrar una enfermedad o un regimen como funcion del producto.
PRECIO = re.compile(r"\b\d{1,4}[.,]\d\d\b")
# TODOS LOS PRECIOS TERMINAN EN .99. Lo fijo la hoja «Lo que todo ingeniero debe
# saber hoy» del 8 de octubre de 2026: Apple solo acepta los precios de su lista
# y ahi .00, .50, .49, .63 y .89 son viejos. Antes este guardia dejaba pasar
# .00 y .50 porque esa era la regla del 7 de octubre. Ya no.
CENTAVOS_BUENOS = ("99",)
# LAS FRASES PROHIBIDAS que la hoja nombra una por una. La lista viva la lleva
# Legal en el anexo E del libro; estas son las que mas se repiten.
PROHIBIDAS = [
    (r"al instante|instantly|instantan", "«al instante»"),
    # «rápido» a secas marcaba falso: «antes de escribir, por si es rápido» es
    # un titulillo, no una promesa. Lo que no se vale es prometer velocidad del
    # servicio, y eso tiene su propia forma.
    # «tout de suite» y «right away» salieron del patron: marcaban el
    # titulillo «L'essentiel, tout de suite», que habla del texto y no de la
    # velocidad del servicio. Quedan las formas que si prometen rapidez.
    (r"mucho antes|much sooner|bien avant|en minutos|within minutes|"
     r"en quelques minutes|m[aá]s r[aá]pido que|faster than|enseguida",
     "promete velocidad"),
    (r"sin l[ií]mite|unlimited|illimit", "«sin límite»"),
    (r"\bel mejor\b|\bla mejor\b|\bthe best\b|\ble meilleur\b|\bla meilleure\b", "«el mejor»"),
    (r"la ley exige|the law requires|la loi exige", "«la ley exige»"),
    (r"cumple la Ley 25|complies with Law 25|conforme à la loi 25", "«cumple la Ley 25»"),
    (r"n[uú]mero propio|our own number|num[eé]ro propre", "«número propio»"),
    (r"hecho en Montreal|made in Montreal|fait à Montréal", "«hecho en Montreal»"),
    (r"mitad de precio|half price|moitié prix", "«mitad de precio»"),
    (r"\bgratis\b|\bfree\b|\bgratuit", "«gratis»"),
    (r"mes de regalo|free month|mois cadeau", "«un mes de regalo»"),
    (r"respondemos en un m[aá]ximo de|reply within|r[eé]pondons dans un d[eé]lai",
     "promete un plazo de respuesta"),
]
NOMBRE = re.compile(r"Leonor|Ayluardo|Troncoso|Morales|C[aá]rdenas")
# El telefono se escribe de muchas formas: (514) 800-3924, 514-800-3924,
# 514.800.3924, +1 514 800 3924. El patron tiene que aguantar los parentesis y
# varios espacios: mi primera version no cazaba «(514) 800-3924» y lo descubrio
# la prueba que el guardia se hace a si mismo.
TELEFONO = re.compile(r"\(?\b(?:514|438|450|579|581|819|873)\b\)?[\s.\-]{0,3}\d{3}[\s.\-]{0,3}\d{4}\b")
POSTAL = re.compile(r"\b[A-Z]\d[A-Z] ?\d[A-Z]\d\b")
CALLE = re.compile(r"Ashdale|\bavenue\b.{0,24}\d|\bavenida\b.{0,24}\d", re.I)
PAGO = re.compile(r"<form|buy\.stripe|paddle\.js|data-product|checkout\.", re.I)


def solo_texto(h):
    """Fuera la hoja de estilo y los guiones: ahi hay colores como #E9E4D6 que
    parecen un codigo postal, y numeros como 14px que parecen precios. Me marco
    falso tres veces el 8 de octubre antes de aprenderlo."""
    h = re.sub(r"<style[^>]*>.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<script[^>]*>.*?</script>", " ", h, flags=re.S | re.I)
    # Y fuera las etiquetas: en los nombres de clase y en las direcciones hay
    # palabras como «free» que no las lee nadie. Marcaron falso a la primera.
    h = re.sub(r"<[^>]+>", " ", h)
    return h


def paginas():
    """Las carpetas con index.html, menos las de trabajo."""
    fuera = ("_fichas", "_marca", "_plantilla", "_paginas-de-venta", ".git")
    for raiz, _, arch in os.walk(AQUI):
        if any(("%s%s" % (os.sep, f)) in raiz or raiz.endswith(f) for f in fuera):
            continue
        if "index.html" in arch:
            rel = os.path.relpath(raiz, AQUI).replace(os.sep, "/")
            yield ("" if rel == "." else rel + "/")


def lee(ruta):
    if EN_VIVO:
        with urllib.request.urlopen(BASE + ruta) as r:
            return r.read().decode("utf-8", "replace")
    return io.open(os.path.join(AQUI, ruta.replace("/", os.sep), "index.html"),
                   encoding="utf-8", errors="replace").read()


def revisa(ruta, html):
    """Devuelve la lista de lo que esta mal. Vacia es que esta bien."""
    t = solo_texto(html)
    mal = []
    es_terminos_de_consumo = ruta in ("aymor-cuisine/terminos/",)

    for m in set(SALUD.findall(t)):
        mal.append("palabra de salud o dieta: «%s»" % m)
    for p in set(PRECIO.findall(t)):
        if p.split(",")[-1].split(".")[-1] not in CENTAVOS_BUENOS:
            mal.append("precio que no termina en .99: %s" % p)
    for patron, comoSeLlama in PROHIBIDAS:
        if re.search(patron, t, re.I):
            mal.append("frase prohibida: %s" % comoSeLlama)
    if not es_terminos_de_consumo:
        if NOMBRE.search(t):
            mal.append("el nombre de la direccion")
        if TELEFONO.search(t):
            mal.append("un telefono")
        if POSTAL.search(t) or CALLE.search(t):
            mal.append("un domicilio")
    if "Google Play" in t:
        mal.append("menciona Google Play")
    if ruta.endswith("soporte/") and re.search(r"paddle", t, re.I):
        mal.append("una pagina de soporte nombra a Paddle")
    if PAGO.search(html):
        mal.append("un formulario o una caja de pago")
    return mal


# ─────────────────────── primero el guardia se prueba a si mismo ────────────
print("  PRIMERO EL GUARDIA SE PRUEBA A SI MISMO")
ATAQUES = [
    ("una funcion que nombra una enfermedad", "x/", "<p>el modo diabetes cuenta los carbohidratos</p>", True),
    ("un precio en .89", "x/", "<p>329,89 USD al año</p>", True),
    ("el nombre de la direccion", "x/", "<p>Maria Leonor Ayluardo Troncoso</p>", True),
    ("un telefono", "x/", "<p>llama al (514) 800-3924</p>", True),
    ("un domicilio", "x/", "<p>avenue Ashdale, H4W 2B7</p>", True),
    ("Google Play", "x/", "<p>disponible en Google Play</p>", True),
    ("Paddle en una pagina de soporte", "x/soporte/", "<p>el cobro lo hace Paddle</p>", True),
    ("un formulario", "x/", "<form><input></form>", True),
    ("un aviso que protege, con «salud» dentro", "x/",
     "<p>consulta a tu profesional de la salud</p>", False),
    ("un aviso que dice que no da consejo medico", "x/",
     "<p>la app no da consejo médico: solo cuenta</p>", False),
    ("un color de la hoja de estilo", "x/",
     "<style>a{color:#E9E4D6}</style><p>hola</p>", False),
    ("un precio en .50, que ya es viejo", "x/", "<p>4,50 USD</p>", True),
    ("una frase que promete rapidez", "x/", "<p>se manda al instante</p>", True),
    ("que promete un plazo de respuesta", "x/",
     "<p>te respondemos en un máximo de 30 días</p>", True),
    ("«mitad de precio» en vez del porcentaje", "x/", "<p>primer mes a mitad de precio</p>", True),
    ("un precio bueno", "x/", "<p>29,99 USD y 149,99 USD</p>", False),
]
fallo_propio = 0
for nombre, ruta, html, debe_cazar in ATAQUES:
    cazo = bool(revisa(ruta, html))
    bien = cazo == debe_cazar
    if not bien:
        fallo_propio += 1
    print("     %-8s %s" % ("la caza" if debe_cazar else "lo deja", nombre)
          + ("" if bien else "   <<< EL GUARDIA FALLA AQUI"))
if fallo_propio:
    print()
    print("  EL GUARDIA NO SIRVE: falla %d de sus propias pruebas." % fallo_propio)
    sys.exit(1)
print("     Las %d en orden. Ahora su resultado vale algo." % len(ATAQUES))
print()

# ─────────────────────────────── y ahora las paginas ────────────────────────
print("  LAS PAGINAS%s" % (" EN VIVO" if EN_VIVO else " DE ESTA CARPETA"))
print("  " + "-" * 62)
total = malas = 0
for ruta in sorted(paginas()):
    try:
        html = lee(ruta)
    except Exception as e:
        print("     %-34s no se pudo leer: %s" % (ruta or "(portada)", e))
        malas += 1
        continue
    total += 1
    fallos = revisa(ruta, html)
    if fallos:
        malas += 1
        print("     %-34s MAL" % (ruta or "(portada)"))
        for f in fallos:
            print("        " + f)
    else:
        print("     %-34s bien" % (ruta or "(portada)"))

print()
print("  %d paginas revisadas, %d con algo que arreglar." % (total, malas))
sys.exit(1 if malas else 0)
