# Paginas de venta guardadas, no publicadas

## OJO: EL GUION BAJO NO ESCONDE DE GITHUB

Esta hoja decia, hasta el 29 de septiembre de 2026, que **nadie de fuera puede
abrir** estas paginas. **Eso era falso**, y lo habia escrito yo. Lo dejo aqui
para que nadie vuelva a creerlo.

Lo que el guion bajo hace de verdad: Jekyll no publica las carpetas que empiezan
con `_`, asi que `aymorcorp.github.io` no sirve estas paginas y dan 404. Eso si
funciona.

Lo que NO hace: esconderlas del repositorio. **Este repositorio es publico**, y
GitHub sirve todos sus archivos, se publiquen en el sitio o no. Comprobado el 29
de septiembre:

    api.github.com/repos/aymorcorp/tienda                             -> 200 (publico)
    raw.githubusercontent.com/.../_paginas-de-venta/<app>/index.html  -> 200

O sea que estas paginas no son inalcanzables: son **no-enlazadas**. Un cliente no
llega por casualidad; alguien que quiera mirar, si. Y los buscadores indexan
GitHub.

## Que se hizo con eso

Por decision del 555 el 29 de septiembre: el trabajo sin publicar sale del
repositorio publico y vive en la carpeta de cada aplicacion hasta el estreno.

  - **Impeccable** y **Orbite** ya salieron. Estan en
    `Aymor Apps - Proyectos/<app>/pagina-de-venta/`.
  - Las demas las mueve cada chat.

Para volver a publicar una el dia que se abra el telon, se copia de la carpeta de
su aplicacion a la raiz del repositorio (`impeccable/`, `crm-orbite/`...) y se
devuelve su tarjeta a la portada (`index.html`).

Un aviso para quien mueva las suyas: borrarlas de aqui **no las borra del
historial de git**, y de ahi se pueden recuperar. Se decidio no reescribir el
historial: es trabajo real por una exposicion menor, tratandose de paginas a
medio hacer. Si alguna llega a tener algo de verdad sensible, hay que volver a
mirarlo.

## Lo que SI se queda publicado, a proposito

Las politicas de privacidad (`impeccable/privacidad/`, `crm-orbite/privacidad/` y
las demas). Google Play y Apple exigen una direccion publica y abierta de la
politica para poder subir la aplicacion; si se caen, no se puede publicar en
ninguna de las dos tiendas. No venden nada ni ensenan la aplicacion: solo dicen
que datos guarda.

-- chat 016

---

**29 de septiembre de 2026, chat 018:** la página de venta de **Quorum** salió de
esta carpeta y volvió a `quorum/`, publicada. Fue decisión de la dueña y del 555:
Paddle necesita ver una página de venta real para verificar el negocio, y Quorum
ya pasó sus pruebas.

-- chat 018
