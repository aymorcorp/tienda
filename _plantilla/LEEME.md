# La tienda se arma sola

**29 de septiembre de 2026, chat 018.**

Hasta hoy, cada página de venta se escribía a mano: mil y pico de renglones de HTML
por aplicación, con su estilo copiado, su cambia-idiomas copiado y sus precios
escritos a mano en tres idiomas. Cuando cambió el nombre de la casa, hubo
que ir a buscarlo a nueve lugares distintos. Eso es lo que se acabó.

**Ahora, agregar una aplicación a la tienda es llenar una ficha y correr un programa.**

```
python _plantilla/construir.py
```

---

## Dónde vive cada cosa

| Carpeta | Qué hay adentro |
|---|---|
| `_fichas/` | Una ficha por aplicación. Es lo único que se escribe. |
| `_fichas/precios.json` | **Todos los precios oficiales**, copiados del documento del 555. |
| `_fichas/tienda.json` | Lo que es igual en toda la tienda: el nombre de la casa, el correo, los textos de la portada. |
| `_fichas/EJEMPLO-app-nueva.json` | La ficha en blanco, con cada renglón explicado. Cópiala. |
| `_plantilla/pagina.html` | La forma de una página de venta. Una sola, para todas. |
| `_plantilla/portada.html` | La forma de la portada. |
| `_plantilla/estilo.css` | El estilo de toda la tienda. Un color se cambia aquí y cambia en todas. |
| `_plantilla/construir.py` | El programa que arma las páginas. |

Las carpetas que empiezan con guion bajo **no se publican**: GitHub Pages usa Jekyll,
y Jekyll las salta. Por eso las fichas y la plantilla viven en el repositorio, con
todo su historial, sin que nadie de fuera las pueda abrir. Es el mismo truco del
telón.

---

## Agregar una aplicación

1. Copia `_fichas/EJEMPLO-app-nueva.json` con el nombre de tu app: `_fichas/mi-app.json`.
2. Llénala. Los renglones que empiezan con guion bajo (`_nombre`, `_precio`…) son
   notas para quien la llena y no salen en ninguna página.
3. Corre `python _plantilla/construir.py`.
4. Abre la página y revísala con tus propios ojos.

Si algo falta, el programa no arma nada y te dice qué es:

```
  NO SE PUDO ARMAR LA TIENDA
  ----------------------------------------------
  a la ficha mi-app.json le falta en es: preguntas.lista.3.r
```

## Las tres reglas que el programa hace cumplir solo

**1. Ningún precio se escribe de memoria.** En los textos no se escriben cifras: se
escribe `{p.mes}`, `{p.anual}`, `{p.mitad}`, y la cifra sale de `_fichas/precios.json`,
que es copia del documento oficial del 555. La cifra además se escribe como se
escribe en cada idioma: `29,63 $ US` en francés, `US$29.63` en inglés y en español.
Si un precio cambia, se cambia en un solo lugar y se vuelve a armar la tienda.

**2. Ningún teléfono en material de venta.** Regla de la casa del 28 de septiembre.
Si una página sale con un número de teléfono o un enlace de WhatsApp, el programa se
detiene y no publica nada. El contacto del cliente es el correo, y ya.

**3. La casa se llama Aymor Applis.** En los tres idiomas, nunca "Aymor Apps". Si una
página sale con el nombre viejo, el programa también se detiene.

**Y una cuarta, que es de traducción:** todos los idiomas de una página tienen que
traer exactamente los mismos renglones. No se puede publicar una página a la que le
falta un pedazo en español. El programa compara renglón por renglón.

---

## El telón

En la ficha:

- `"publicada": true` → la página se escribe en `mi-app/` y cualquiera la puede abrir.
- `"publicada": false` → la página se escribe en `_paginas-de-venta/mi-app/` y nadie
  de fuera la alcanza.

Cambias esa palabra, vuelves a correr el programa, y la página se mueve sola de un
lado al otro. Ya no hay que acordarse de hacer `git mv` ni de quitar la tarjeta de la
portada a mano.

Las políticas de privacidad **no** las arma este programa y **no** se bajan nunca:
Google Play y Apple exigen una dirección pública y abierta para poder subir la
aplicación.

---

## Las aplicaciones que todavía tienen su página escrita a mano

Impeccable, CRM Orbite y Aymor Cuisine siguen con la página que escribió su chat a
mano. **No las toqué**: son suyas, y funcionan. El día que su dueño quiera pasarlas
a la plantilla, es llenar una ficha y borrar el HTML viejo; el programa avisa cuáles
están así cada vez que corre.

Para que la tienda se vea como una sola tienda de verdad, lo que sí conviene es que
todas terminen aquí. Mientras tanto, nadie pierde nada: una ficha nueva no estorba a
una página vieja.

---

## Qué NO se edita a mano nunca

`index.html` y `quorum/index.html` los escribe el programa. Llevan un aviso arriba
que lo dice. Si alguien los edita a mano, el siguiente que arme la tienda le borra el
cambio sin querer. Lo que se cambia es la ficha.

-- chat 018
