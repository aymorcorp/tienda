# -*- coding: utf-8 -*-
"""
CONSTRUIR LA TIENDA
===================

Arma las paginas de la tienda a partir de las fichas. Nadie escribe una pagina
a mano: se llena una ficha en _fichas/ y se corre este programa.

    python _plantilla/construir.py

Que hace, en orden:

  1. Lee los precios oficiales de _fichas/precios.json. Ningun precio se
     escribe dentro de un texto: en los textos se pone {p.mes} o {p.anual} y
     aqui se reemplaza por la cifra, ya escrita como se escribe en cada idioma.
  2. Lee cada ficha de _fichas/*.json.
  3. Arma la portada (index.html) con una tarjeta por aplicacion.
  4. Arma la pagina de venta de cada aplicacion que tenga "pagina": true.
     Si la ficha dice "publicada": false, la pagina se guarda en
     _paginas-de-venta/<app>/ y nadie de fuera la puede abrir: es el telon.
  5. Revisa que ningun idioma se haya quedado sin traducir, y que ninguna
     pagina lleve un telefono. Si algo falta, se detiene y lo dice.

Nada de esto cuesta dinero: siguen siendo archivos sueltos en GitHub Pages.
"""

import io, json, os, re, sys, shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHAS = os.path.join(RAIZ, "_fichas")
PLANTILLA = os.path.join(RAIZ, "_plantilla")
TELON = os.path.join(RAIZ, "_paginas-de-venta")

AVISO = ("<!-- ESTA PAGINA NO SE EDITA A MANO.\n"
         "     Se arma sola con: python _plantilla/construir.py\n"
         "     Lo que quieras cambiar, cambialo en _fichas/{ficha} y vuelve a correrlo.\n"
         "     Si editas aqui, el siguiente que construya la tienda borra tu cambio. -->\n")


# ─────────────────────────────────────────────────────────────
#  Errores que se explican solos
# ─────────────────────────────────────────────────────────────
class ErrorDeFicha(Exception):
    pass


def exige(condicion, mensaje):
    if not condicion:
        raise ErrorDeFicha(mensaje)


# ─────────────────────────────────────────────────────────────
#  Los precios
# ─────────────────────────────────────────────────────────────
def cargar_precios():
    with io.open(os.path.join(FICHAS, "precios.json"), encoding="utf-8") as f:
        return json.load(f)


def escribe_cifra(numero, idioma, precios):
    """1649.89 en frances es '1 649,89 $ US'; en ingles 'US$1,649.89'."""
    entero, dec = ("%.2f" % float(numero)).split(".")
    coma = " " if idioma == "fr" else ","
    grupos = []
    while len(entero) > 3:
        grupos.insert(0, entero[-3:])
        entero = entero[:-3]
    grupos.insert(0, entero)
    texto = coma.join(grupos) + precios["_decimal"].get(idioma, ".") + dec
    return precios["_formato"].get(idioma, "US${n}").replace("{n}", texto)


def precios_de(app, idioma, precios):
    tabla = precios["apps"].get(app, {})
    return {k: escribe_cifra(v, idioma, precios) for k, v in tabla.items()}


PRECIO_EN_TEXTO = re.compile(r"\{p\.([A-Za-z]+)\}")


def meter_precios(valor, tabla, donde):
    """Cambia {p.mes} por la cifra, en cualquier texto de la ficha."""
    if isinstance(valor, str):
        def uno(m):
            clave = m.group(1)
            exige(clave in tabla,
                  "en %s se pide el precio {p.%s} y no existe en precios.json" % (donde, clave))
            return tabla[clave]
        return PRECIO_EN_TEXTO.sub(uno, valor)
    if isinstance(valor, list):
        return [meter_precios(v, tabla, donde) for v in valor]
    if isinstance(valor, dict):
        return {k: meter_precios(v, tabla, donde) for k, v in valor.items()}
    return valor


# ─────────────────────────────────────────────────────────────
#  Aplanar: de arbol a claves con punto, para el cambia-idiomas
# ─────────────────────────────────────────────────────────────
def aplanar(arbol, prefijo=""):
    plano = {}
    if isinstance(arbol, dict):
        for k, v in arbol.items():
            if k.startswith("_"):
                continue
            plano.update(aplanar(v, prefijo + k + "." if prefijo == "" else prefijo + k + "."))
    elif isinstance(arbol, list):
        for i, v in enumerate(arbol):
            plano.update(aplanar(v, prefijo + str(i) + "."))
    else:
        plano[prefijo[:-1]] = arbol
    return plano


# ─────────────────────────────────────────────────────────────
#  La plantilla: {{clave}}, {{{crudo}}}, repetir y si
# ─────────────────────────────────────────────────────────────
MARCA = re.compile(r"<!--\s*(repetir|si|no):([^>]+?)\s*-->|<!--\s*/(repetir|si|no)\s*-->")


def trocear(texto):
    """Convierte la plantilla en un arbol de pedazos."""
    pos, pila = 0, [[]]
    for m in MARCA.finditer(texto):
        pila[-1].append(("texto", texto[pos:m.start()]))
        pos = m.end()
        if m.group(1):
            pila.append([])
            pila[-1].append(("__abre__", m.group(1), m.group(2).strip()))
        else:
            bloque = pila.pop()
            cab = bloque[0]
            exige(cab[1] == m.group(3),
                  "la plantilla cierra <!--/%s--> donde abrio <!--%s-->" % (m.group(3), cab[1]))
            pila[-1].append((cab[1], cab[2], bloque[1:]))
    pila[-1].append(("texto", texto[pos:]))
    exige(len(pila) == 1, "en la plantilla quedo un bloque sin cerrar")
    return pila[0]


def buscar(ruta, item, ctx):
    """Una ruta con puntos. Si empieza con punto, es del elemento de la lista."""
    if ruta.startswith("."):
        base, ruta = item, ruta[1:]
    else:
        base = ctx
    if ruta == "":
        return base
    for parte in ruta.split("."):
        if isinstance(base, dict):
            if parte not in base:
                return None
            base = base[parte]
        elif isinstance(base, list):
            if not parte.isdigit() or int(parte) >= len(base):
                return None
            base = base[int(parte)]
        else:
            return None
    return base


def escapar(v):
    return (str(v).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


CLAVE = re.compile(r"\{\{\{([^}]+)\}\}\}|\{\{([^}]+)\}\}")


def pintar(pedazos, ctx, item=None, clave_base="", donde="la plantilla"):
    salida = []
    for p in pedazos:
        if p[0] == "texto":
            def uno(m):
                crudo = m.group(1)
                ruta = (crudo or m.group(2)).strip()
                if ruta == "_clave":
                    return clave_base
                v = buscar(ruta, item, ctx)
                exige(v is not None, "en %s se pide {{%s}} y la ficha no lo trae" % (donde, ruta))
                return str(v) if crudo else escapar(v)
            salida.append(CLAVE.sub(uno, p[1]))
        elif p[0] == "repetir":
            lista = buscar(p[1], item, ctx) or []
            raiz = clave_base if p[1].startswith(".") else ""
            nombre = p[1].lstrip(".")
            for i, elem in enumerate(lista):
                sub = (raiz + "." if raiz else "") + nombre + "." + str(i)
                salida.append(pintar(p[2], ctx, elem, sub, donde))
        elif p[0] in ("si", "no"):
            v = buscar(p[1], item, ctx)
            hay = bool(v) and v != []
            if (p[0] == "si") == hay:
                salida.append(pintar(p[2], ctx, item, clave_base, donde))
    return "".join(salida)


def construir(nombre_plantilla, ctx, donde):
    with io.open(os.path.join(PLANTILLA, nombre_plantilla), encoding="utf-8") as f:
        return pintar(trocear(f.read()), ctx, None, "", donde)


# ─────────────────────────────────────────────────────────────
#  Revisiones antes de publicar
# ─────────────────────────────────────────────────────────────
TELEFONO = re.compile(r"(wa\.me|whatsapp\.com|\+?1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4})")


def revisar(html, donde):
    malo = TELEFONO.search(html)
    exige(not malo,
          "%s lleva un telefono (%s). Regla de la casa del 28 de septiembre: ningun "
          "telefono va en material de venta; el contacto del cliente es el correo."
          % (donde, malo.group(0) if malo else ""))
    exige("Aymor Apps" not in html,
          "%s todavia dice 'Aymor Apps'. La casa se llama Aymor Applis, en los tres idiomas."
          % donde)


def mismas_claves(textos, donde):
    """Todos los idiomas tienen que traer exactamente los mismos renglones."""
    idiomas = list(textos.keys())
    base = set(aplanar(textos[idiomas[0]]).keys())
    for idioma in idiomas[1:]:
        suyas = set(aplanar(textos[idioma]).keys())
        faltan = base - suyas
        sobran = suyas - base
        exige(not faltan, "a %s le falta en %s: %s" % (donde, idioma, ", ".join(sorted(faltan))))
        exige(not sobran, "a %s le sobra en %s: %s" % (donde, idioma, ", ".join(sorted(sobran))))


# ─────────────────────────────────────────────────────────────
#  Cargar las fichas
# ─────────────────────────────────────────────────────────────
def cargar_fichas(precios):
    fichas = []
    for nombre in sorted(os.listdir(FICHAS)):
        if not nombre.endswith(".json") or nombre == "precios.json" or nombre.startswith("EJEMPLO"):
            continue
        if nombre == "tienda.json":
            continue
        ruta = os.path.join(FICHAS, nombre)
        with io.open(ruta, encoding="utf-8") as f:
            try:
                ficha = json.load(f)
            except ValueError as e:
                raise ErrorDeFicha("la ficha %s no se puede leer: %s" % (nombre, e))
        ficha["_archivo"] = nombre
        exige("carpeta" in ficha, "a la ficha %s le falta 'carpeta'" % nombre)
        exige("nombre" in ficha, "a la ficha %s le falta 'nombre'" % nombre)
        exige("textos" in ficha, "a la ficha %s le falta 'textos'" % nombre)
        # Una app puede tener su pagina en tres idiomas y su tarjeta en cuatro:
        # "idiomasDePagina" dice cuales llevan la pagina completa. Los demas solo
        # tienen que traer la tarjeta de la portada.
        completos = ficha.get("idiomasDePagina") or list(ficha["textos"].keys())
        for i in completos:
            exige(i in ficha["textos"],
                  "la ficha %s dice que su pagina va en %s y no trae esos textos" % (nombre, i))
        mismas_claves({i: ficha["textos"][i] for i in completos}, "la ficha " + nombre)
        base = set(aplanar(ficha["textos"][completos[0]].get("tarjeta", {})).keys())
        for i in ficha["textos"]:
            if i in completos:
                continue
            suyas = set(aplanar(ficha["textos"][i].get("tarjeta", {})).keys())
            exige(suyas == base,
                  "en la ficha %s, el idioma %s solo lleva la tarjeta de la portada, "
                  "y sus renglones no son los mismos que los de %s"
                  % (nombre, i, completos[0]))
        ficha["_completos"] = completos
        fichas.append(ficha)
    return fichas


def textos_con_precio(ficha, precios):
    """Los mismos textos, ya con las cifras adentro, idioma por idioma."""
    listos = {}
    for idioma, arbol in ficha["textos"].items():
        tabla = precios_de(ficha.get("precio", ficha["carpeta"]), idioma, precios)
        listos[idioma] = meter_precios(arbol, tabla, "la ficha " + ficha["_archivo"])
    return listos


def diccionario_js(textos):
    """El diccionario que lleva la pagina para cambiar de idioma."""
    plano = {i: aplanar(a) for i, a in textos.items()}
    return json.dumps(plano, ensure_ascii=False, indent=2, sort_keys=True)


# ─────────────────────────────────────────────────────────────
#  Armar
# ─────────────────────────────────────────────────────────────
def main():
    precios = cargar_precios()
    with io.open(os.path.join(FICHAS, "tienda.json"), encoding="utf-8") as f:
        tienda = json.load(f)
    mismas_claves(tienda["textos"], "la ficha tienda.json")

    with io.open(os.path.join(PLANTILLA, "estilo.css"), encoding="utf-8") as f:
        css = f.read()

    fichas = cargar_fichas(precios)
    hechas = []
    avisos = []

    # ---- La pagina de venta de cada aplicacion ----
    for ficha in fichas:
        if not ficha.get("pagina"):
            continue
        todos = textos_con_precio(ficha, precios)
        textos = {i: todos[i] for i in ficha["_completos"]}
        principal = ficha.get("idiomaPrincipal", "fr")
        exige(principal in textos,
              "la ficha %s dice que su idioma principal es '%s' y no trae esos textos"
              % (ficha["_archivo"], principal))
        ctx = dict(ficha)
        ctx.update(textos[principal])
        ctx["css"] = css
        ctx["botonesIdioma"] = [{"codigo": i, "nombre": tienda["idiomas"][i]} for i in textos]
        ctx["diccionario"] = diccionario_js(textos)
        ctx["principal"] = principal
        ctx["tienda"] = tienda.get("comun", {})
        html = AVISO.replace("{ficha}", ficha["_archivo"]) + construir(
            "pagina.html", ctx, "la pagina de " + ficha["nombre"])
        revisar(html, "la pagina de " + ficha["nombre"])

        publicada = ficha.get("publicada", False)
        destino = os.path.join(RAIZ if publicada else TELON, ficha["carpeta"])
        contrario = os.path.join(TELON if publicada else RAIZ, ficha["carpeta"], "index.html")
        if not os.path.isdir(destino):
            os.makedirs(destino)
        with io.open(os.path.join(destino, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        if os.path.isfile(contrario):
            os.remove(contrario)
        hechas.append((ficha["nombre"], os.path.relpath(destino, RAIZ),
                       "publicada" if publicada else "con el telon abajo"))

    # ---- La portada ----
    tarjetas = [f for f in fichas if f.get("tarjeta", {}).get("mostrar", True)]
    orden = {"disponible": 0, "pronto": 1}
    tarjetas.sort(key=lambda f: (orden.get(f["tarjeta"].get("estado", "pronto"), 9),
                                 f["nombre"]))
    listas = {}
    for idioma in tienda["textos"]:
        filas = []
        for f in tarjetas:
            t = textos_con_precio(f, precios)
            suyo = idioma
            if suyo not in t:
                suyo = f.get("idiomaPrincipal", "fr")
                avisos.append("la tarjeta de %s no esta en %s: sale en %s"
                              % (f["nombre"], idioma, suyo))
            tj = t[suyo].get("tarjeta", {})
            exige(tj, "a la ficha %s le falta el bloque 'tarjeta' en sus textos"
                  % f["_archivo"])
            filas.append({
                "nombre": f["nombre"],
                "carpeta": f["carpeta"],
                "estado": f["tarjeta"].get("estado", "pronto"),
                "clase": "live" if f["tarjeta"].get("estado") == "disponible" else "soon",
                "enlace": f.get("publicada", False) and f.get("pagina", False),
                "etiqueta": tj.get("etiqueta", ""),
                "que_hace": tj.get("queHace", ""),
                "precio": tj.get("precio", ""),
                "boton": tj.get("boton", ""),
                "_ficha": f["_archivo"],
            })
        listas[idioma] = filas

    principal = tienda.get("idiomaPrincipal", "fr")
    ctx = dict(tienda.get("comun", {}))
    ctx.update(tienda["textos"][principal])
    ctx["css"] = css
    ctx["apps"] = listas[principal]
    ctx["botonesIdioma"] = [{"codigo": i, "nombre": tienda["idiomas"][i]} for i in tienda["textos"]]
    ctx["principal"] = principal
    dicc = {i: aplanar(tienda["textos"][i]) for i in tienda["textos"]}
    for idioma, filas in listas.items():
        for n, fila in enumerate(filas):
            for campo in ("etiqueta", "que_hace", "precio", "boton"):
                dicc[idioma]["apps.%d.%s" % (n, campo)] = fila[campo]
    ctx["diccionario"] = json.dumps(dicc, ensure_ascii=False, indent=2, sort_keys=True)
    portada = AVISO.replace("{ficha}", "tienda.json y la de cada app") + construir(
        "portada.html", ctx, "la portada")
    revisar(portada, "la portada")
    with io.open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(portada)

    # ---- El parte ----
    print("")
    print("  LA TIENDA QUEDO ARMADA")
    print("  " + "-" * 46)
    print("  portada ................ index.html  (%d tarjetas)" % len(tarjetas))
    for nombre, donde, estado in hechas:
        print("  %-22s %s/  (%s)" % (nombre, donde, estado))
    if avisos:
        print("")
        print("  Ojo:")
        for a in sorted(set(avisos)):
            print("    - " + a)
    sin_pagina = [f["nombre"] for f in fichas if not f.get("pagina")]
    if sin_pagina:
        print("")
        print("  Con ficha pero con pagina escrita a mano (no se toco):")
        for n in sin_pagina:
            print("    - " + n)
    print("")


if __name__ == "__main__":
    try:
        main()
    except ErrorDeFicha as e:
        print("")
        print("  NO SE PUDO ARMAR LA TIENDA")
        print("  " + "-" * 46)
        print("  " + str(e))
        print("")
        sys.exit(1)
