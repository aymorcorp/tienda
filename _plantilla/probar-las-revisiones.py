# -*- coding: utf-8 -*-
"""
PROBAR LAS REVISIONES DE LA TIENDA
==================================

    python _plantilla/probar-las-revisiones.py

El constructor tiene cuatro revisiones que impiden publicar algo mal. Este
programa las prueba ROMPIENDO LA TIENDA A PROPOSITO y comprobando que cada una
se da cuenta.

POR QUE EXISTE. El 30 de septiembre de 2026, a un chat de la casa le paso que su
comprobacion automatica pasaba siempre en verde: media una constante de un
diseno anterior que ya no existia en el dibujo. Llevaba dias sin medir nada y
nadie se entero, porque una revision que siempre dice que si nunca llama la
atencion.

    Una revision que nunca se ha visto fallar no es una revision, es una
    esperanza.

El constructor de la tienda cambia seguido -- en un solo dia le entraron el
robots.txt, el enlace bajo el precio y un cambio de textos. Cualquiera de esos
cambios pudo haber dejado una revision sin medir. Por eso esto se corre DESPUES
de tocar el constructor, y no se confia en que siga sirviendo porque servia ayer.

COMO LEERLO. Cada prueba rompe la ficha de una manera y espera que el programa
SE DETENGA. Si alguna dice "PASO EN VERDE", esa revision dejo de servir y hay
que arreglarla antes de publicar nada.

LA FICHA SE RESTAURA SIEMPRE, incluso si esto revienta a la mitad.
"""

import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHA = os.path.join(RAIZ, "_fichas", "quorum.json")

# Cada prueba: como se llama, que se cambia, y por que tiene que atajarlo.
PRUEBAS = [
    ("falta una traduccion",
     '"fine": "Funciona en cualquier teléfono',
     '"letraChica": "Funciona en cualquier teléfono',
     "Una pagina a la que le falta un renglon en un idioma no se publica."),

    ("se colo un telefono",
     '"boton": "Escríbenos por correo"',
     '"boton": "Llámanos al 263-566-2243"',
     "Regla de la casa: ningun telefono va en material de venta."),

    ("aparece el nombre viejo",
     '"producto": "Quorum — una aplicación de Aymor Applis"',
     '"producto": "Quorum — una aplicación de Aymor Apps"',
     "La casa se llama Aymor Applis, en los tres idiomas."),

    ("un precio que no existe",
     '"cifra": "{p.mes}",',
     '"cifra": "{p.trimestre}",',
     "Ningun precio se escribe de memoria: sale de precios.json o no sale."),
]


def construye():
    """Corre el constructor y dice si se detuvo, y con que motivo."""
    r = subprocess.run([sys.executable, os.path.join("_plantilla", "construir.py")],
                       cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    motivo = ""
    for linea in r.stdout.splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("-") and "NO SE PUDO" not in linea:
            motivo = linea
    return r.returncode != 0, motivo


def main():
    bueno = io.open(FICHA, encoding="utf-8").read()
    fallaron = []
    try:
        print("")
        print("  ROMPIENDO LA TIENDA A PROPOSITO")
        print("  " + "-" * 60)
        for nombre, viejo, nuevo, porque in PRUEBAS:
            if bueno.count(viejo) < 1:
                print("  %-26s NO SE PUDO PROBAR" % nombre)
                print("      el texto que se iba a romper ya no esta en la ficha;")
                print("      hay que actualizar esta prueba, no ignorarla.")
                fallaron.append(nombre)
                continue
            io.open(FICHA, "w", encoding="utf-8", newline="\n").write(
                bueno.replace(viejo, nuevo, 1))   # una sola vez basta
            paro, motivo = construye()
            print("  %-26s %s" % (nombre, "se detuvo" if paro else "*** PASO EN VERDE ***"))
            if paro:
                print("      dijo: " + motivo[:100])
            else:
                print("      " + porque)
                print("      ESA REVISION DEJO DE SERVIR.")
                fallaron.append(nombre)

        # No todo es atajar errores: armar la tienda dos veces seguidas, sin
        # tocar nada en medio, tiene que dar exactamente el mismo resultado.
        # Hasta el 1 de octubre de 2026 no era asi -- el sitemap se ponia la
        # fecha de hoy en todas las paginas cada vez -- y eso le decia a los
        # buscadores que cinco paginas habian cambiado cuando no habia
        # cambiado ninguna, ademas de esconder los cambios de verdad.
        mapa = os.path.join(RAIZ, "sitemap.xml")
        construye()
        antes = io.open(mapa, encoding="utf-8").read()
        construye()
        igual = antes == io.open(mapa, encoding="utf-8").read()
        print("  %-26s %s" % ("armar dos veces da igual",
                              "si" if igual else "*** CAMBIA SOLO ***"))
        if not igual:
            print("      El sitemap cambia aunque no haya cambiado ninguna pagina.")
            print("      Eso le miente a los buscadores y tapa los cambios de verdad.")
            fallaron.append("armar dos veces da igual")
    finally:
        # Pase lo que pase, la ficha vuelve a estar como estaba.
        io.open(FICHA, "w", encoding="utf-8", newline="\n").write(bueno)
        construye()

    print("")
    if fallaron:
        print("  HAY %d REVISION(ES) QUE YA NO SIRVEN: %s" % (len(fallaron), ", ".join(fallaron)))
        print("  No publiques hasta arreglarlas.")
        print("")
        sys.exit(1)
    print("  Las cuatro revisiones siguen sabiendo decir que no,")
    print("  y armar la tienda dos veces seguidas da lo mismo.")
    print("  La ficha quedo como estaba.")
    print("")


if __name__ == "__main__":
    main()
