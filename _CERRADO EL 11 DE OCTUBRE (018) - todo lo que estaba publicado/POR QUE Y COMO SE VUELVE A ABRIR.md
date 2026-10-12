# Todo lo que estaba publicado, cerrado

**11 de octubre de 2026. Orden de la dirección: «cierra todas las tiendas,
todas las aplicaciones».**

Nada se borró. Todo está aquí dentro, entero, en la misma forma en que estaba
publicado. Esta carpeta empieza por `_`, y GitHub Pages no publica las
carpetas que empiezan por `_`.

---

## Qué se cerró

| Lo que ya no abre | Qué era |
|---|---|
| `/tienda/` | La portada de la tienda (se cerró primero, el mismo día) |
| `/tienda/privacidad/` · `/terminos/` · `/reembolso/` · `/precios/` | Las cuatro páginas generales |
| `/tienda/quorum/…` | Privacidad, términos y soporte de Quorum |
| `/tienda/prose/…` | Privacidad y soporte de Prose |
| `/tienda/impeccable/…` · `/orbite/…` · `/crm-orbite/…` | Sus privacidades y soportes |
| `/tienda/aymor-detailing/…` | Sus términos |
| `sitemap.xml` y `robots.txt` | El mapa que le daba todo eso a los buscadores |

Las páginas de venta de las siete apps ya estaban cerradas desde antes.

---

## Lo que esto rompe, dicho claro

Se lo advertí a la dirección dos veces antes de hacerlo, y ella lo ordenó
igual sabiéndolo. Queda escrito para que nadie se lleve una sorpresa:

**1. El botón de privacidad DENTRO de dos apps ya compiladas lleva ahora a un
error.** Son **Quorum** y **Orbite**: tienen la dirección escrita dentro del
programa, en `android/app/src/main/assets/public/index.html`. Eso **no se
arregla volviendo a subir la página**: hay que volver a compilar la app, o
volver a abrir esta carpeta.

**2. Apple exige una dirección de privacidad viva para poder enviar.** Hoy no
hay ninguna. Antes de mandar cualquier app a Apple, esto tiene que volver.

**3. Paddle pide términos, reembolso y privacidad accesibles** para aprobar un
dominio. Ya nos rechazó el dominio el 8 de octubre por verlo «en
construcción»; sin estas páginas no se puede volver a pedir.

---

## Cómo se vuelve a abrir

Se mueve de vuelta a la raíz lo que haga falta y se sube. No hay nada más.

    git mv "_CERRADO EL 11 DE OCTUBRE (018) - todo lo que estaba publicado/privacidad" .
    git commit -m "Vuelve a abrir la política de privacidad"
    git push

Se puede abrir **solo una**. No hay que abrirlo todo para abrir la de Quorum.

---

## Lo que se comprobó antes de cerrar

La dirección pidió: «revisa que ninguna llave se haya quedado ahí».

**Ninguna, nunca.** Se revisaron los 121 cambios del historial del
repositorio, no solo lo que había hoy: ni una clave de API, ni un token, ni un
`.env`, ni un `.pem`, ni un archivo de firma. Nunca entró ninguno.

Lo que sí hubo alguna vez, y **hoy ya no está en ningún archivo**: el nombre
completo de la dirección y un teléfono, en un archivo de pruebas que
comprobaba justamente que no aparecieran; y el número de empresa, en una
ficha. Los tres salieron en su momento. Siguen en el historial porque
reescribirlo lo decidió la dirección que no, y eso no cambió hoy.

                                                  018, 11 de octubre de 2026
