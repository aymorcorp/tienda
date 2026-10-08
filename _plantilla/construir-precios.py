# -*- coding: utf-8 -*-
"""
CONSTRUIR LA PAGINA DE PRECIOS
==============================

    python _plantilla/construir-precios.py

Arma precios/index.html a partir de _fichas/precios.json. **Ningun precio se
escribe a mano en esta pagina.**

POR QUE EXISTE ESTE PROGRAMA. Hasta el 8 de octubre de 2026 la pagina de
precios era un texto escrito a mano el 7 de octubre a las 22:27, parcheado a
mano tres veces el 8. Por eso el español usaba coma decimal («29,99 USD») y el
archivo de precios dice punto, y por eso un precio podia cambiar en el archivo
y quedarse viejo en la pagina. Lo encontro el 555 y pidio que hubiera una sola
fuente. Esta es.

EL FORMATO, que tambien sale del archivo:
  - español e ingles: punto decimal y «USD» detras de la cifra -> 29.99 USD
  - frances: coma decimal y «$ US» detras -> 29,99 $ US

LO QUE NO VA EN ESTA PAGINA, por decision de la direccion del 8 de octubre:
  - Aymor Prospection: la estan rehaciendo, no aparece hasta que ella lo diga.
  - Leonie, y la palabra «Proximamente» o parecidas: el telon simplemente no se
    abre.
  - El descuento del primer mes de Aymor Cuisine y el del telefono adicional de
    Quorum: no existen. Lo dice _descuento en el archivo y este programa se
    detiene si alguien los vuelve a meter.
"""
import datetime
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
T = os.path.dirname(AQUI)
FICHA = os.path.join(T, "_fichas", "precios.json")
PAGINA = os.path.join(T, "precios", "index.html")

MESES = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
}

# Las aplicaciones que NO van en esta pagina, y por que.
FUERA = {
    "aymor-prospection": "la direccion la esta rehaciendo (8 oct 2026)",
}


def parar(motivo):
    print("")
    print("  NO SE ARMO LA PAGINA DE PRECIOS")
    print("  " + motivo.replace("\n", "\n  "))
    print("")
    sys.exit(1)


def plata(n, idioma):
    """La cifra, escrita como se escribe en cada idioma."""
    x = "%.2f" % n
    if idioma == "fr":
        return x.replace(".", ",") + " $ US"
    return x + " USD"


def fecha(idioma):
    hoy = datetime.date.today()
    mes = MESES[idioma][hoy.month - 1]
    if idioma == "en":
        return "%s %d, %d" % (mes, hoy.day, hoy.year)
    if idioma == "fr":
        return "%d %s %d" % (hoy.day, mes, hoy.year)
    return "%d de %s de %d" % (hoy.day, mes, hoy.year)


# ---------------------------------------------------------------- las palabras
PALABRAS = {
    "es": dict(
        titulo="Precios", actualizado="Última actualización",
        moneda="Todos los precios están en dólares estadounidenses (USD). "
               "Cada tabla dice si es por mes, el primer mes o el año.",
        impuestos="Los impuestos, si corresponden, se muestran al pagar.",
        hMes="Al mes", thApp="Aplicación", thMes="Al mes",
        hFormas="Dos formas de empezar",
        formas="Eliges una. No se juntan.",
        hPrimero="Primer mes con descuento",
        thPrimero="Primer mes", thDescuento="Descuento",
        descuento="50 % de descuento en tu primer mes",
        hAnual="El año: once meses pagados, doce meses usados",
        thAnual="El año",
        quorum="<strong>Quorum</strong> se cobra por teléfono que marca horas, "
               "no por empleado. El primer reporte de cada semana está "
               "incluido. Cualquier reporte adicional que pidas dentro de esa "
               "misma semana cuesta {reporte}. La cuenta se reinicia cada "
               "semana.",
        cambios="Los precios pueden cambiar. Si cambian, se te avisa con al "
                "menos 30 días de anticipación antes de que se te cobre el "
                "nuevo precio. Un periodo ya pagado no cambia de precio.",
        pie="Aymor Applis, un negocio registrado en Quebec",
        apps={"impeccable": "Impeccable — negocios de limpieza",
              "crm-orbite": "Orbite — negocios de servicio",
              "quorum": "Quorum — negocios con personal por hora",
              "aymor-detailing": "Aymor Detailing — detallado de autos",
              "aymor-studio": "Aymor Studio — fotógrafos y estudios chicos",
              "aymor-cuisine": "Aymor Cuisine — recetas"},
        qMes="{mes} el primer teléfono, y {extra} cada teléfono adicional, hasta cinco",
        qPrimero="Quorum, primer teléfono",
        qAnual="{anual} el primer teléfono, {anualExtra} cada teléfono adicional",
        dsBase="Aymor Detailing · Aymor Studio, Base",
        dsPro="Aymor Detailing · Aymor Studio, Pro",
        dsElite="Aymor Detailing · Aymor Studio, Elite",
        ds="Base {mes} · Pro {pro} · Elite {elite}",
        dsAnual="Base {anual} · Pro {anualPro} · Elite {anualElite}",
        dsJuntos="Aymor Detailing · Aymor Studio"),
    "fr": dict(
        titulo="Prix", actualizado="Dernière mise à jour",
        moneda="Tous les prix sont en dollars américains (USD). Chaque tableau "
               "indique s'il s'agit du prix par mois, du premier mois ou de "
               "l'année.",
        impuestos="Les taxes, si elles s'appliquent, sont indiquées au moment "
                  "du paiement.",
        hMes="Par mois", thApp="Application", thMes="Par mois",
        hFormas="Deux façons de commencer",
        formas="Vous en choisissez une. Elles ne se combinent pas.",
        hPrimero="Premier mois avec rabais",
        thPrimero="Premier mois", thDescuento="Rabais",
        descuento="50 % de rabais le premier mois",
        hAnual="À l'année : onze mois payés, douze mois utilisés",
        thAnual="À l'année",
        quorum="<strong>Quorum</strong> se facture par téléphone qui poinçonne "
               "des heures, pas par employé. Le premier rapport de chaque "
               "semaine est inclus. Tout rapport additionnel demandé dans la "
               "même semaine coûte {reporte}. Le compte repart chaque semaine.",
        cambios="Les prix peuvent changer. S'ils changent, vous êtes avisé au "
                "moins 30 jours avant qu'on vous facture le nouveau prix. Une "
                "période déjà payée ne change pas de prix.",
        pie="Aymor Applis, une entreprise immatriculée au Québec",
        apps={"impeccable": "Impeccable — entreprises de ménage",
              "crm-orbite": "Orbite — entreprises de services",
              "quorum": "Quorum — entreprises avec personnel à l'heure",
              "aymor-detailing": "Aymor Detailing — esthétique automobile",
              "aymor-studio": "Aymor Studio — photographes et petits studios",
              "aymor-cuisine": "Aymor Cuisine — recettes"},
        qMes="{mes} pour le premier téléphone, et {extra} par téléphone "
             "additionnel, jusqu'à cinq",
        qPrimero="Quorum, premier téléphone",
        qAnual="{anual} le premier téléphone, {anualExtra} par téléphone additionnel",
        dsBase="Aymor Detailing · Aymor Studio, Base",
        dsPro="Aymor Detailing · Aymor Studio, Pro",
        dsElite="Aymor Detailing · Aymor Studio, Elite",
        ds="Base {mes} · Pro {pro} · Elite {elite}",
        dsAnual="Base {anual} · Pro {anualPro} · Elite {anualElite}",
        dsJuntos="Aymor Detailing · Aymor Studio"),
    "en": dict(
        titulo="Prices", actualizado="Last updated",
        moneda="All prices are in US dollars (USD). Each table says whether it "
               "is per month, the first month or the year.",
        impuestos="Taxes, if they apply, are shown at payment.",
        hMes="Per month", thApp="Application", thMes="Per month",
        hFormas="Two ways to start",
        formas="You pick one. They do not combine.",
        hPrimero="First month with a discount",
        thPrimero="First month", thDescuento="Discount",
        descuento="50% off your first month",
        hAnual="Yearly: eleven months paid, twelve months used",
        thAnual="Yearly",
        quorum="<strong>Quorum</strong> is billed per phone that punches "
               "hours, not per employee. The first report of each week is "
               "included. Any additional report requested within that same "
               "week costs {reporte}. The count resets each week.",
        cambios="Prices can change. If they change, you are told at least 30 "
                "days before the new price is charged to you. A period already "
                "paid for does not change price.",
        pie="Aymor Applis, a business registered in Quebec",
        apps={"impeccable": "Impeccable — cleaning businesses",
              "crm-orbite": "Orbite — service businesses",
              "quorum": "Quorum — businesses with hourly staff",
              "aymor-detailing": "Aymor Detailing — car detailing",
              "aymor-studio": "Aymor Studio — photographers and small studios",
              "aymor-cuisine": "Aymor Cuisine — recipes"},
        qMes="{mes} for the first phone, and {extra} for each additional "
             "phone, up to five",
        qPrimero="Quorum, first phone",
        qAnual="{anual} for the first phone, {anualExtra} for each additional phone",
        dsBase="Aymor Detailing · Aymor Studio, Base",
        dsPro="Aymor Detailing · Aymor Studio, Pro",
        dsElite="Aymor Detailing · Aymor Studio, Elite",
        ds="Base {mes} · Pro {pro} · Elite {elite}",
        dsAnual="Base {anual} · Pro {anualPro} · Elite {anualElite}",
        dsJuntos="Aymor Detailing · Aymor Studio"),
}

PROHIBIDAS = [
    (r"Pr[óo]ximamente|Prochainement|Coming soon", "«Próximamente»"),
    (r"Prospection", "Aymor Prospection"),
    (r"L[ée]onie", "Léonie"),
    (r"gratis|gratuit|\bfree\b", "«gratis»"),
    (r"mitad de precio|half price|moiti[ée] prix", "«mitad de precio»"),
]


def seccion(idioma, p):
    w = PALABRAS[idioma]
    q, im, cr = p["quorum"], p["impeccable"], p["crm-orbite"]
    de, st, cu = p["aymor-detailing"], p["aymor-studio"], p["aymor-cuisine"]
    d = lambda n: plata(n, idioma)
    f = []
    f.append('<section data-lang="%s"%s>' % (idioma, "" if idioma == "es" else " hidden"))
    f.append("<h1>%s</h1>" % w["titulo"])
    f.append('<p class="updated">%s: %s</p>' % (w["actualizado"], fecha(idioma)))
    f.append('<div class="card">')
    f.append("<p>%s</p>" % w["moneda"])
    f.append("<p>%s</p>" % w["impuestos"])

    f.append("<h2>%s</h2>" % w["hMes"])
    f.append("<table>")
    f.append("  <tr><th>%s</th><th>%s</th></tr>" % (w["thApp"], w["thMes"]))
    f.append("  <tr><td>%s</td><td>%s</td></tr>" % (w["apps"]["impeccable"], d(im["mes"])))
    f.append("  <tr><td>%s</td><td>%s</td></tr>" % (w["apps"]["crm-orbite"], d(cr["mes"])))
    f.append("  <tr><td>%s</td><td>%s</td></tr>"
             % (w["apps"]["quorum"],
                w["qMes"].format(mes=d(q["mes"]), extra=d(q["extra"]))))
    for clave, app in (("aymor-detailing", de), ("aymor-studio", st)):
        f.append("  <tr><td>%s</td><td>%s</td></tr>"
                 % (w["apps"][clave],
                    w["ds"].format(mes=d(app["mes"]), pro=d(app["pro"]),
                                   elite=d(app["elite"]))))
    f.append("  <tr><td>%s</td><td>%s</td></tr>" % (w["apps"]["aymor-cuisine"], d(cu["mes"])))
    f.append("</table>")

    f.append("<h2>%s</h2>" % w["hFormas"])
    f.append("<p>%s</p>" % w["formas"])
    f.append("<h3>%s</h3>" % w["hPrimero"])
    f.append("<table>")
    f.append("  <tr><th>%s</th><th>%s</th><th>%s</th></tr>"
             % (w["thApp"], w["thPrimero"], w["thDescuento"]))
    f.append("  <tr><td>Impeccable</td><td>%s</td><td>%s</td></tr>" % (d(im["mitad"]), w["descuento"]))
    f.append("  <tr><td>Orbite</td><td>%s</td><td>%s</td></tr>" % (d(cr["mitad"]), w["descuento"]))
    f.append("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (w["qPrimero"], d(q["mitad"]), w["descuento"]))
    f.append("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (w["dsBase"], d(de["mitad"]), w["descuento"]))
    f.append("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (w["dsPro"], d(de["mitadPro"]), w["descuento"]))
    f.append("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (w["dsElite"], d(de["mitadElite"]), w["descuento"]))
    f.append("</table>")

    f.append("<h3>%s</h3>" % w["hAnual"])
    f.append("<table>")
    f.append("  <tr><th>%s</th><th>%s</th></tr>" % (w["thApp"], w["thAnual"]))
    f.append("  <tr><td>Impeccable</td><td>%s</td></tr>" % d(im["anual"]))
    f.append("  <tr><td>Orbite</td><td>%s</td></tr>" % d(cr["anual"]))
    f.append("  <tr><td>Quorum</td><td>%s</td></tr>"
             % w["qAnual"].format(anual=d(q["anual"]), anualExtra=d(q["anualExtra"])))
    f.append("  <tr><td>%s</td><td>%s</td></tr>"
             % (w["dsJuntos"],
                w["dsAnual"].format(anual=d(de["anual"]), anualPro=d(de["anualPro"]),
                                    anualElite=d(de["anualElite"]))))
    f.append("  <tr><td>Aymor Cuisine</td><td>%s</td></tr>" % d(cu["anual"]))
    f.append("</table>")

    f.append("<p>%s</p>" % w["quorum"].format(reporte=d(q["reporteExtra"])))
    f.append("<p>%s</p>" % w["cambios"])
    f.append("</div>")
    f.append('<p class="updated" style="margin-top:20px">%s — '
             '<a href="mailto:aymorcorp@gmail.com">aymorcorp@gmail.com</a></p>' % w["pie"])
    f.append("</section>")
    return "\n".join(f)


def main():
    p = json.load(io.open(FICHA, encoding="utf-8"))["apps"]
    for clave, porque in FUERA.items():
        if clave in p:
            del p[clave]
    faltan = [k for k in ("quorum", "impeccable", "crm-orbite", "aymor-detailing",
                          "aymor-studio", "aymor-cuisine") if k not in p]
    if faltan:
        parar("al archivo de precios le faltan: " + ", ".join(faltan))

    pagina = io.open(PAGINA, encoding="utf-8").read()
    i = pagina.find('<section data-lang="es"')
    j = pagina.rfind("</section>")
    if i < 0 or j < 0:
        parar("no reconozco la pagina de precios: no encuentro sus secciones")
    cuerpo = "\n\n".join(seccion(idi, p) for idi in ("es", "fr", "en"))
    nueva = pagina[:i] + cuerpo + pagina[j + len("</section>"):]

    # Nada prohibido, antes de escribir
    texto = re.sub(r"<[^>]+>", " ", nueva)
    for patron, nombre in PROHIBIDAS:
        m = re.search(patron, texto, re.I)
        if m:
            parar("la pagina diria %s («%s»). Eso no va en la pagina de precios."
                  % (nombre, m.group(0)))

    io.open(PAGINA, "w", encoding="utf-8", newline="\n").write(nueva)
    print("")
    print("  PAGINA DE PRECIOS ARMADA desde _fichas/precios.json")
    print("  %d bytes, tres idiomas." % len(nueva.encode("utf-8")))
    print("")
    for idi, ejemplo in (("es", "29.99 USD"), ("fr", "29,99 $ US"), ("en", "29.99 USD")):
        k = nueva.find('<section data-lang="%s"' % idi)
        trozo = nueva[k:k + 2600]
        print("  %s: el mensual de Quorum sale como «%s»  %s"
              % (idi, ejemplo, "bien" if ejemplo in trozo else "*** NO ***"))
    print("")
    for clave, porque in FUERA.items():
        print("  fuera %s: %s" % (clave, porque))


if __name__ == "__main__":
    main()
