# -*- coding: utf-8 -*-
"""
PONER EL NOMBRE DE LA PERSONA RESPONSABLE EN LA LETRA CHICA
===========================================================

    python _plantilla/poner-el-nombre-en-letra-chica.py --ver      enseña que cambiaria
    python _plantilla/poner-el-nombre-en-letra-chica.py --hacerlo  lo cambia

PREPARADO Y SIN APLICAR. Esperando el aviso de 555, que a su vez espera que
la dueña confirme que el nombre va en las siete aplicaciones.

DE DONDE SALE EL TEXTO. Del documento de 002 (Legal), seccion 4, del 2 de
octubre de 2026. La dueña eligio la version "Maria Troncoso" y Legal confirmo
que es valida para una divulgacion publica. Las frases estan copiadas tal
cual, sin reescribir ni una coma: es texto legal, no es mio.

QUE TOCA Y QUE NO. Solo las paginas de Quorum y de la tienda, que son las
mias. Impeccable y Orbite ya lo tienen puesto y publicado por el 003, con la
aprobacion de la dueña; esas no se tocan. Aymor Cuisine es del 019 y tampoco.

POR QUE ESTO ES UN PROGRAMA Y NO UN CAMBIO HECHO A MANO. Porque hacerlo a
mano hoy deja el archivo modificado sin publicar, y de ahi a que se suba por
accidente hay un paso. Asi no hay nada a medias: o esta como estaba, o esta
cambiado del todo, y se ve cual de las dos con --ver.
"""

import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (archivo, como esta hoy, como queda)   -- cada una tiene que estar UNA vez
CAMBIOS = [
    ("quorum/privacidad/index.html",
     "La persona responsable de proteger la información personal dentro de Aymor Applis"
     " puede contactarse en: aymorcorp@gmail.com.",
     "La persona responsable de proteger la información personal dentro de Aymor Applis"
     " es María Troncoso, y puede contactarse en: aymorcorp@gmail.com."),

    ("quorum/privacidad/index.html",
     "La personne responsable de la protection des renseignements personnels au sein"
     " d'Aymor Applis peut être jointe à : aymorcorp@gmail.com.",
     "La personne responsable de la protection des renseignements personnels au sein"
     " d'Aymor Applis est María Troncoso, et peut être jointe à : aymorcorp@gmail.com."),

    ("quorum/privacidad/index.html",
     "The person responsible for protecting personal information within Aymor Applis"
     " can be reached at: aymorcorp@gmail.com.",
     "The person responsible for protecting personal information within Aymor Applis"
     " is María Troncoso, and can be reached at: aymorcorp@gmail.com."),

    ("privacidad/index.html",
     "La persona responsable de proteger la información personal dentro de Aymor Applis"
     " puede contactarse en: aymorcorp@gmail.com.",
     "La persona responsable de proteger la información personal dentro de Aymor Applis"
     " es María Troncoso, y puede contactarse en: aymorcorp@gmail.com."),
]


def main():
    hacerlo = "--hacerlo" in sys.argv
    if not hacerlo and "--ver" not in sys.argv:
        print(__doc__)
        return

    textos = {}
    problemas = []
    for archivo, viejo, nuevo in CAMBIOS:
        ruta = os.path.join(RAIZ, archivo.replace("/", os.sep))
        if archivo not in textos:
            if not os.path.exists(ruta):
                problemas.append("falta %s" % archivo)
                continue
            textos[archivo] = io.open(ruta, encoding="utf-8").read()
        t = textos[archivo]
        if nuevo in t:
            print("  YA ESTABA PUESTO en %s" % archivo)
            continue
        if t.count(viejo) != 1:
            problemas.append("en %s la frase aparece %d veces, esperaba 1:\n      %s"
                             % (archivo, t.count(viejo), viejo[:70]))
            continue
        textos[archivo] = t.replace(viejo, nuevo)
        print("  %s %s" % ("CAMBIADO:" if hacerlo else "cambiaria:", archivo))
        print("      + ...%s" % nuevo[-72:])

    if problemas:
        print("")
        print("  NO SE CAMBIO NADA. Hay %d problema(s):" % len(problemas))
        for p in problemas:
            print("    - " + p)
        print("")
        print("  Que el texto no cuadre quiere decir que la pagina cambio desde que")
        print("  esto se escribio. Hay que mirarla, no forzar el cambio.")
        sys.exit(1)

    if not hacerlo:
        print("")
        print("  Esto fue solo para ver. Nada se toco.")
        print("  Para aplicarlo:  python _plantilla/poner-el-nombre-en-letra-chica.py --hacerlo")
        print("  Y despues hay que subirlo, que es lo que lo publica de verdad.")
        return

    for archivo, texto in textos.items():
        ruta = os.path.join(RAIZ, archivo.replace("/", os.sep))
        io.open(ruta, "w", encoding="utf-8", newline="\n").write(texto)
    print("")
    print("  Hecho en %d archivo(s). TODAVIA NO ESTA PUBLICADO:" % len(textos))
    print("  se publica al subirlo al repositorio, no al guardarlo aqui.")


if __name__ == "__main__":
    main()
