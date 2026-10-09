# -*- coding: utf-8 -*-
"""
CONSTRUIR LA TIENDA
===================

    python _plantilla/construir-tienda.py

Arma la tienda entera a partir de _plantilla/catalogo.json. **Ninguna pagina se
escribe a mano.** Para meter el producto numero 5000 se añade un renglon al
catalogo y se corre esto.

QUE ARMA, en los tres idiomas:
    <idioma>/index.html                la portada: por oficio, y el estante
    <idioma>/catalogo/index.html       todo, con categorias y buscador
    <idioma>/<producto>/index.html     la pagina de cada producto, con galeria
    <idioma>/mi-membresia/index.html   la cuenta, y ahi vive cancelar
    <idioma>/trabaja-con-nosotros/
    <idioma>/probadores/
    buscar.json                        el indice del buscador

DONDE LO DEJA: en _disenos/tienda/. La carpeta empieza por «_», asi que GitHub
Pages NO la publica. El telon lo abre la direccion, nadie mas.

COMO CUMPLE LO QUE PIDIO LA DIRECCION
  - Telefono, tableta y computadora, Apple y Android: una sola pagina que se
    acomoda sola, de 320 puntos de ancho en adelante. No hay version movil
    aparte y no se usa nada que solo tenga un navegador.
  - Se desliza con el dedo: los estantes y las galerias se arrastran y se
    frenan en cada pieza (scroll-snap), que es lo que hace el telefono solo.
  - Le picas a una foto y se abre su pagina, con mas fotos y todo lo que trae.
  - Se paga aqui, y aqui se cancela: el boton de cancelar vive al final de
    «Mi membresia», discreto pero encontrable.
  - Abajo del todo: trabaja con nosotros, y los probadores.

LO QUE NO HACE, A PROPOSITO
  - No enciende ningun boton de compra. El telon esta abajo.
  - No inventa un precio. Mientras la direccion no diga cuanto cuesta una
    guia, dice «precio por definir» y el boton esta apagado.
  - No publica lo que no debe: la guia de salud no sale hasta que Legal la
    mire, y el programa lo dice en pantalla al construir.
"""
import io
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
TIENDA = os.path.dirname(AQUI)
CATALOGO = os.path.join(AQUI, "catalogo.json")
SALIDA = os.path.join(TIENDA, "_disenos", "tienda")
GUIAS = r"C:\Users\beby2\OneDrive\Desktop\Carpeta del equipo\Catalogo de Guias"
IDIOMAS = ["es", "fr", "en"]

PALABRAS = {
    "es": dict(
        h1a="Lo que nadie te explicó de ", h1b="tener un negocio",
        lead="Guías que se leen en una tarde y aplicaciones que se usan toda la semana. Hechas en Quebec, en el idioma en que trabajas.",
        buscar="Buscar en el catálogo", masLeidas="Las más leídas",
        arrastra="Arrástralas con el dedo", verOficio="Ver lo de este oficio",
        volver="Volver al catálogo", comprar="Comprar", trae="Qué trae dentro",
        pagoUnico="pago único · PDF y EPUB · 3 idiomas",
        porDefinir="Precio por definir", telon="El botón se enciende cuando la dirección abra la tienda.",
        catalogo="Todo el catálogo", todo="Todo", productos="productos",
        laTienda="La tienda", tuCuenta="Tu cuenta", laCasa="Aymor Applis", loLegal="Lo legal",
        apps="Aplicaciones", guias="Guías y libros", porOficio="Por oficio",
        miMembresia="Mi membresía", volverBajar="Volver a bajar lo que compré",
        misFacturas="Mis facturas", quienes="Quiénes somos",
        trabaja="Trabaja con nosotros", probador="Sé probador de nuestras apps",
        escribenos="Escríbenos", precios="Precios", terminos="Términos",
        privacidad="Privacidad", reembolsos="Reembolsos",
        pie="Aymor Applis — un negocio registrado en Quebec",
        memTitulo="Mi membresía", memVacio="Todavía no has comprado nada.",
        memExplica="Aquí vas a ver lo que compraste, volver a bajarlo, cambiar tu tarjeta y bajar tus facturas.",
        memCancelar="Cancelar mi suscripción", memCancelaNota="Puedes cancelar cuando quieras. Lo que ya pagaste sigue funcionando hasta que se acabe el periodo, y tus datos no se borran.",
        trabTitulo="Trabaja con nosotros",
        trabLead="Somos chicos y trabajamos en francés, inglés y español. Si te late lo que hacemos, escríbenos y cuéntanos qué sabes hacer.",
        probTitulo="Sé probador de nuestras apps",
        probLead="Antes de sacar una aplicación la probamos con gente de verdad, en su propio teléfono y en su propio trabajo. Si quieres ser de los primeros, escríbenos y te avisamos del siguiente lanzamiento.",
        probQue="Qué significa", probPuntos=["Usar la app en tu trabajo durante unos días", "Decirnos qué no se entiende y qué se rompe", "Nada de compromiso: dejas de probar cuando quieras"]),
    "fr": dict(
        h1a="Ce que personne ne vous a expliqué sur ", h1b="avoir une entreprise",
        lead="Des guides qui se lisent en un après-midi et des applications qui servent toute la semaine. Faits au Québec, dans la langue où vous travaillez.",
        buscar="Chercher dans le catalogue", masLeidas="Les plus lus",
        arrastra="Faites-les glisser du doigt", verOficio="Voir ce métier",
        volver="Retour au catalogue", comprar="Acheter", trae="Ce qu'il contient",
        pagoUnico="paiement unique · PDF et EPUB · 3 langues",
        porDefinir="Prix à déterminer", telon="Le bouton s'allume quand la direction ouvrira la boutique.",
        catalogo="Tout le catalogue", todo="Tout", productos="produits",
        laTienda="La boutique", tuCuenta="Votre compte", laCasa="Aymor Applis", loLegal="Le légal",
        apps="Applications", guias="Guides et livres", porOficio="Par métier",
        miMembresia="Mon abonnement", volverBajar="Retélécharger mes achats",
        misFacturas="Mes factures", quienes="Qui nous sommes",
        trabaja="Travailler avec nous", probador="Devenir testeur de nos applis",
        escribenos="Écrivez-nous", precios="Prix", terminos="Conditions",
        privacidad="Confidentialité", reembolsos="Remboursements",
        pie="Aymor Applis — une entreprise immatriculée au Québec",
        memTitulo="Mon abonnement", memVacio="Vous n'avez encore rien acheté.",
        memExplica="Ici vous verrez vos achats, vous pourrez les retélécharger, changer votre carte et obtenir vos factures.",
        memCancelar="Annuler mon abonnement", memCancelaNota="Vous pouvez annuler quand vous voulez. Ce qui est déjà payé fonctionne jusqu'à la fin de la période, et vos données ne sont pas effacées.",
        trabTitulo="Travailler avec nous",
        trabLead="Nous sommes petits et nous travaillons en français, en anglais et en espagnol. Si ce qu'on fait vous parle, écrivez-nous.",
        probTitulo="Devenir testeur de nos applications",
        probLead="Avant de sortir une application, on la teste avec du vrai monde, sur leur téléphone et dans leur travail. Pour être des premiers, écrivez-nous.",
        probQue="Ce que ça veut dire", probPuntos=["Utiliser l'application dans votre travail quelques jours", "Nous dire ce qui ne se comprend pas et ce qui casse", "Aucun engagement : vous arrêtez quand vous voulez"]),
    "en": dict(
        h1a="What nobody explained to you about ", h1b="running a business",
        lead="Guides you can read in an afternoon and apps you use all week. Made in Quebec, in the language you work in.",
        buscar="Search the catalogue", masLeidas="Most read",
        arrastra="Swipe them with your finger", verOficio="See this trade",
        volver="Back to the catalogue", comprar="Buy", trae="What's inside",
        pagoUnico="one-time · PDF and EPUB · 3 languages",
        porDefinir="Price to be set", telon="The button turns on when the owner opens the store.",
        catalogo="The whole catalogue", todo="All", productos="products",
        laTienda="The store", tuCuenta="Your account", laCasa="Aymor Applis", loLegal="Legal",
        apps="Apps", guias="Guides and books", porOficio="By trade",
        miMembresia="My membership", volverBajar="Download my purchases again",
        misFacturas="My invoices", quienes="Who we are",
        trabaja="Work with us", probador="Test our apps",
        escribenos="Write to us", precios="Prices", terminos="Terms",
        privacidad="Privacy", reembolsos="Refunds",
        pie="Aymor Applis — a business registered in Quebec",
        memTitulo="My membership", memVacio="You have not bought anything yet.",
        memExplica="Here you will see what you bought, download it again, change your card and get your invoices.",
        memCancelar="Cancel my subscription", memCancelaNota="You can cancel whenever you want. What you already paid for keeps working until the period ends, and your data is not deleted.",
        trabTitulo="Work with us",
        trabLead="We are small and we work in French, English and Spanish. If what we do speaks to you, write to us.",
        probTitulo="Test our apps",
        probLead="Before releasing an app we test it with real people, on their own phone and in their own work. To be among the first, write to us.",
        probQue="What it means", probPuntos=["Use the app in your work for a few days", "Tell us what is unclear and what breaks", "No commitment: stop whenever you want"]),
}

CSS = open(os.path.join(AQUI, "tienda.css"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(AQUI, "tienda.css")) else ""


def parar(motivo):
    print("\n  NO SE ARMO LA TIENDA\n  " + motivo.replace("\n", "\n  ") + "\n")
    sys.exit(1)


def marco(idi, titulo, cuerpo, profundidad=1, clase=""):
    w = PALABRAS[idi]
    # DOS CAMINOS DISTINTOS, y confundirlos fue el error que cazo la prueba:
    #   «arriba»  llega a la raiz de la tienda  -> la hoja de estilo y los idiomas
    #   «dentro»  llega a la raiz del IDIOMA    -> el catalogo, la membresia, el pie
    # Desde es/catalogo/, la raiz de la tienda es ../../ y la del idioma es ../
    arriba = "../" * profundidad
    dentro = "../" * (profundidad - 1)
    idis = "".join("<a href='%s%s/'%s>%s</a>"
                   % (arriba, o, " class=on" if o == idi else "", o.upper())
                   for o in IDIOMAS)
    pie_cols = [
        (w["laTienda"], [(w["catalogo"], "catalogo/"), (w["apps"], "catalogo/"),
                         (w["guias"], "catalogo/"), (w["porOficio"], "")]),
        (w["tuCuenta"], [(w["miMembresia"], "mi-membresia/"),
                         (w["volverBajar"], "mi-membresia/"), (w["misFacturas"], "mi-membresia/")]),
        (w["laCasa"], [(w["quienes"], ""), (w["trabaja"], "trabaja-con-nosotros/"),
                       (w["probador"], "probadores/"), (w["escribenos"], "")]),
        (w["loLegal"], [(w["precios"], ""), (w["terminos"], ""),
                        (w["privacidad"], ""), (w["reembolsos"], "")]),
    ]
    cols = "".join(
        "<div><h5>%s</h5>%s</div>"
        % (t, "".join("<a href='%s%s'>%s</a>" % (dentro, d, n) for n, d in ls))
        for t, ls in pie_cols)
    return ("<!doctype html><html lang=%s><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1,viewport-fit=cover'>"
            "<title>%s</title><link rel=stylesheet href='%stienda.css'></head>"
            "<body class='%s'>"
            "<div class=barra><div class=centro>"
            "<a class=marca href='%s'>AYMOR APPLIS</a>"
            "<a class=buscar href='%scatalogo/'>%s</a>"
            "<span class=idiomas>%s</span></div></div>"
            "%s"
            "<footer><div class=centro><div class=cols>%s</div>"
            "<p class=cierre>%s · aymorcorp@gmail.com</p></div></footer></body></html>"
            % (idi, titulo, arriba, clase, dentro or "./", dentro, w["buscar"], idis,
               cuerpo, cols, PALABRAS[idi]["pie"]))


def tarjeta(idi, p, a_enlace="", a_img="", precio_txt=""):
    """El camino al enlace y el camino a la imagen NO son el mismo. Desde el
       catalogo, el producto esta al lado (../ley25/) pero las imagenes estan
       dos pisos arriba (../../img/). Los tenia juntos y las imagenes del
       catalogo no cargaban: lo cazo probar-la-tienda.py."""
    return ("<a class=libro href='%s%s/'>"
            "<div class=obj style=\"background-image:url('%simg/%s-mockup.jpg')\"></div>"
            "<h4>%s</h4><p>%s</p><b>%s</b></a>"
            % (a_enlace, p["id"], a_img, p["carpeta"], p[idi]["titulo"],
               p["_catnombre"], precio_txt))


def construir():
    d = json.load(io.open(CATALOGO, encoding="utf-8"))
    cats, oficios = d["categorias"], d["oficios"]
    todos = d["productos"]
    fuera = [p for p in todos if not p.get("publicar")]
    vivos = [p for p in todos if p.get("publicar")]
    if not vivos:
        parar("el catalogo no tiene ni un producto publicable")

    os.makedirs(SALIDA, exist_ok=True)
    img = os.path.join(SALIDA, "img")
    os.makedirs(img, exist_ok=True)
    for p in todos:
        for origen, mote in (("MOCKUP_3D.jpg", "mockup"),
                             ("ES/COVER_1280x720.jpg", "cover"),
                             ("ES/THUMB_600x600.jpg", "thumb")):
            o = os.path.join(GUIAS, p["carpeta"], *origen.split("/"))
            dst = os.path.join(img, "%s-%s.jpg" % (p["carpeta"], mote))
            if os.path.exists(o) and not os.path.exists(dst):
                shutil.copy2(o, dst)
    io.open(os.path.join(SALIDA, "tienda.css"), "w", encoding="utf-8",
            newline="\n").write(CSS)

    indice = []
    for idi in IDIOMAS:
        w = PALABRAS[idi]
        for p in vivos:
            p["_catnombre"] = cats[p["cat"]][idi]
        base = os.path.join(SALIDA, idi)
        os.makedirs(base, exist_ok=True)

        # ---------- portada ----------
        bandas = "".join(
            "<a class=of href='catalogo/'>"
            "<div class=fondo style=\"background-image:url('../img/%s-mockup.jpg')\"></div>"
            "<div class=velo style=\"background:linear-gradient(170deg,%s66 0%%,%sE6 78%%)\"></div>"
            "<h3>%s</h3><span>%s →</span></a>"
            % (o["imagen"], o["color"], o["color"], o[idi], w["verOficio"])
            for o in oficios)
        estante = "".join(tarjeta(idi, p, "", "../", w["porDefinir"]) for p in vivos[:8])
        io.open(os.path.join(base, "index.html"), "w", encoding="utf-8", newline="\n").write(
            marco(idi, "Aymor Applis",
                  "<div class=centro><div class=saludo>"
                  "<h1>%s<i>%s</i>.</h1><p>%s</p></div></div>"
                  "<div class=centro><div class=oficios>%s</div>"
                  "<div class=titulo><h2>%s</h2><span>%s</span></div></div>"
                  "<div class=estante sangrado>%s</div>"
                  % (w["h1a"], w["h1b"], w["lead"], bandas,
                     w["masLeidas"], w["arrastra"], estante)))

        # ---------- catalogo ----------
        usadas = []
        for c in cats:
            if any(p["cat"] == c for p in vivos):
                usadas.append(c)
        chips = ("<a class='chip on' data-cat=todo>%s</a>" % w["todo"]) + "".join(
            "<a class=chip data-cat='%s'>%s</a>" % (c, cats[c][idi]) for c in usadas)
        rejilla = "".join(
            "<div class=celda data-cat='%s' data-busca='%s'>%s</div>"
            % (p["cat"], (p[idi]["titulo"] + " " + p[idi]["lead"] + " " + p["_catnombre"]).lower(),
               tarjeta(idi, p, "../", "../../", w["porDefinir"]))
            for p in vivos)
        io.open(os.path.join(base, "catalogo"), "w") if False else None
        os.makedirs(os.path.join(base, "catalogo"), exist_ok=True)
        io.open(os.path.join(base, "catalogo", "index.html"), "w", encoding="utf-8", newline="\n").write(
            marco(idi, w["catalogo"],
                  "<div class=centro><div class=saludo chico>"
                  "<h1>%s</h1><p>%d %s</p></div>"
                  "<input class=campo id=q placeholder='%s' autocomplete=off>"
                  "<div class=chips>%s</div>"
                  "<div class=rejilla id=rej>%s</div>"
                  "<p class=nada id=nada hidden>—</p></div>"
                  "<script src='../../buscar.js'></script>"
                  % (w["catalogo"], len(vivos), w["productos"], w["buscar"], chips, rejilla),
                  profundidad=2))

        # ---------- cada producto ----------
        for p in vivos:
            carpeta = os.path.join(base, p["id"])
            os.makedirs(carpeta, exist_ok=True)
            fotos = "".join(
                "<img src='../../img/%s-%s.jpg' alt='' loading=lazy>" % (p["carpeta"], m)
                for m in ("mockup", "cover", "thumb"))
            puntos = "".join("<i%s></i>" % (" class=on" if k == 0 else "") for k in range(3))
            trae = "".join("<li>%s</li>" % x for x in p[idi]["trae"])
            io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8", newline="\n").write(
                marco(idi, p[idi]["titulo"] + " — Aymor Applis",
                      "<div class=centro><a class=volver href='../catalogo/'>← %s</a>"
                      "<div class=ficha><div>"
                      "<div class=galeria>%s</div><div class=puntos>%s</div></div>"
                      "<div><div class=cat>%s · %s</div><h1>%s</h1>"
                      "<p class=lead>%s</p>"
                      "<div class=precio><b>%s</b><span>%s</span></div>"
                      "<span class='comprar apagado'>%s</span>"
                      "<p class=telon>%s</p>"
                      "<div class=trae><h3>%s</h3><ul>%s</ul></div>"
                      "</div></div></div>"
                      % (w["volver"], fotos, puntos, p["_catnombre"], w["guias"],
                         p[idi]["titulo"], p[idi]["lead"], w["porDefinir"],
                         w["pagoUnico"], w["comprar"], w["telon"], w["trae"], trae),
                      profundidad=2))
            indice.append({"id": p["id"], "idi": idi, "t": p[idi]["titulo"],
                           "c": p["_catnombre"]})

        # ---------- mi membresia, con cancelar al final ----------
        os.makedirs(os.path.join(base, "mi-membresia"), exist_ok=True)
        io.open(os.path.join(base, "mi-membresia", "index.html"), "w", encoding="utf-8", newline="\n").write(
            marco(idi, w["memTitulo"],
                  "<div class=centro><div class=saludo chico><h1>%s</h1>"
                  "<p>%s</p></div>"
                  "<div class=caja><p class=vacio>%s</p></div>"
                  "<div class=cancelar><a>%s</a><p>%s</p></div></div>"
                  % (w["memTitulo"], w["memExplica"], w["memVacio"],
                     w["memCancelar"], w["memCancelaNota"]),
                  profundidad=2))

        # ---------- trabaja con nosotros ----------
        os.makedirs(os.path.join(base, "trabaja-con-nosotros"), exist_ok=True)
        io.open(os.path.join(base, "trabaja-con-nosotros", "index.html"), "w",
                encoding="utf-8", newline="\n").write(
            marco(idi, w["trabTitulo"],
                  "<div class=centro><div class=saludo><h1>%s</h1><p>%s</p></div>"
                  "<p class=correo><a href='mailto:aymorcorp@gmail.com'>aymorcorp@gmail.com</a></p></div>"
                  % (w["trabTitulo"], w["trabLead"]), profundidad=2))

        # ---------- probadores ----------
        os.makedirs(os.path.join(base, "probadores"), exist_ok=True)
        puntos_p = "".join("<li>%s</li>" % x for x in w["probPuntos"])
        io.open(os.path.join(base, "probadores", "index.html"), "w",
                encoding="utf-8", newline="\n").write(
            marco(idi, w["probTitulo"],
                  "<div class=centro><div class=saludo><h1>%s</h1><p>%s</p></div>"
                  "<div class=trae><h3>%s</h3><ul>%s</ul></div>"
                  "<p class=correo><a href='mailto:aymorcorp@gmail.com'>aymorcorp@gmail.com</a></p></div>"
                  % (w["probTitulo"], w["probLead"], w["probQue"], puntos_p),
                  profundidad=2))

    io.open(os.path.join(SALIDA, "buscar.js"), "w", encoding="utf-8", newline="\n").write(BUSCADOR)

    print("")
    print("  TIENDA ARMADA en _disenos/tienda (no se publica)")
    print("  %d productos × %d idiomas = %d paginas de producto"
          % (len(vivos), len(IDIOMAS), len(vivos) * len(IDIOMAS)))
    print("  mas portada, catalogo, membresia, trabajo y probadores en cada idioma")
    if fuera:
        print("")
        for p in fuera:
            print("  FUERA DEL CATALOGO: %s" % p["es"]["titulo"])
            print("     %s" % p.get("_por_que_no", "sin razon escrita"))


BUSCADOR = """/* El buscador. Vive en el navegador: no hay servidor detras, asi que
   funciona igual con trece productos que con cinco mil, y no cuesta nada.
   Filtra por lo que se escribe y por la categoria escogida. */
(function(){
  var q = document.getElementById('q');
  var rej = document.getElementById('rej');
  var nada = document.getElementById('nada');
  if(!q || !rej) return;
  var celdas = [].slice.call(rej.querySelectorAll('.celda'));
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  var cat = 'todo';
  function pintar(){
    var t = q.value.trim().toLowerCase();
    var vistas = 0;
    celdas.forEach(function(c){
      var ok = (cat === 'todo' || c.dataset.cat === cat) &&
               (!t || c.dataset.busca.indexOf(t) >= 0);
      c.hidden = !ok;
      if(ok) vistas++;
    });
    if(nada) nada.hidden = vistas > 0;
  }
  q.addEventListener('input', pintar);
  chips.forEach(function(ch){
    ch.addEventListener('click', function(){
      chips.forEach(function(o){ o.classList.remove('on'); });
      ch.classList.add('on');
      cat = ch.dataset.cat;
      pintar();
    });
  });
})();
"""

if __name__ == "__main__":
    construir()
