# Paginas de venta guardadas, no publicadas

Aqui viven las paginas de venta de Impeccable y de Orbite. **El codigo esta en la
tienda, pero nadie de fuera las puede abrir**, que es exactamente lo que pidio
Leonor el 27 de septiembre de 2026: la regla del telon. Ninguna aplicacion se le
ensena a un cliente real hasta que las siete pasen el examen final juntas.

Como funciona: GitHub Pages usa Jekyll, y Jekyll **no publica** las carpetas que
empiezan con guion bajo. Por eso esta carpeta se llama `_paginas-de-venta`. Los
archivos siguen en el repositorio, con todo su historial; simplemente no se
sirven.

**Para volver a publicarlas el dia que se abra el telon**, desde la raiz del
repositorio:

    git mv "_paginas-de-venta/impeccable/index.html" impeccable/index.html
    git mv "_paginas-de-venta/crm-orbite/index.html" crm-orbite/index.html

y devolver las tarjetas de Impeccable y de Orbite a la portada (`index.html`).

**Lo que NO se bajo, a proposito:** las politicas de privacidad
(`impeccable/privacidad/` y `crm-orbite/privacidad/`). Google Play y Apple exigen
una direccion publica y abierta de la politica para poder subir la aplicacion; si
se caen, no se puede publicar en ninguna de las dos tiendas. No venden nada ni
ensenan la aplicacion: solo dicen que datos guarda. Si el 555 quiere que tambien
se bajen, se bajan igual de rapido.

-- chat 016

---

**Añadido el 28 de septiembre de 2026 por el chat 018:** aquí adentro está también
la página de venta de **Quorum** (`_paginas-de-venta/quorum/`), que se había quedado
fuera de esta operación y seguía siendo alcanzable desde la portada. Su tarjeta
también salió de `index.html`. Para devolverla el día del estreno:

    git mv "_paginas-de-venta/quorum/index.html" quorum/index.html
    git mv "_paginas-de-venta/quorum/og-image.png" quorum/og-image.png

y devolver su tarjeta a la portada. Su política de privacidad
(`quorum/privacidad/`) se queda publicada, por la misma razón que las otras dos.

-- chat 018
