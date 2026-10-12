#!/bin/sh
# ABRIR SOLO LO LEGAL — nada de tienda
# ====================================
# 12 de octubre de 2026.
#
# Para qué: si hay una app en revisión en Apple, su política de privacidad y
# su página de soporte TIENEN que estar abiertas. Apple no deja pasar una app
# cuya dirección de privacidad da error.
#
# Esto devuelve SOLO las páginas legales. No abre la portada de la tienda, ni
# ninguna página de venta: ésas siguen cerradas.
#
# Cómo se corre, desde esta carpeta:
#     sh "ABRIR SOLO LO LEGAL.sh"
#
# Después hay que poner el repositorio en público otra vez, porque con cuenta
# gratuita un repositorio privado no publica páginas. Eso lo hace el 018 con
# un comando, o se hace desde GitHub: Settings → General → Change visibility.
#
# Para volver a cerrarlo: se mueven de vuelta a la carpeta «_CERRADO…».

set -e
G="_CERRADO EL 11 DE OCTUBRE (018) - todo lo que estaba publicado"

for d in privacidad terminos reembolso quorum prose impeccable orbite \
         crm-orbite aymor-detailing; do
  if [ -d "$G/$d" ]; then
    git mv "$G/$d" "$d"
    echo "   abierta: $d"
  fi
done

# El mapa del sitio vuelve también: sin él los buscadores no encuentran nada.
[ -f "$G/sitemap.xml" ] && git mv "$G/sitemap.xml" sitemap.xml && echo "   abierto: sitemap.xml"
[ -f "$G/robots.txt" ] && git mv "$G/robots.txt" robots.txt && echo "   abierto: robots.txt"

echo ""
echo "   LA PORTADA Y LOS PRECIOS NO SE ABREN: siguen guardados."
echo "   Eso es a propósito. Lo legal es lo que Apple exige; la tienda, no."
echo ""
echo "   Falta subirlo y volver a poner el repositorio en público."
