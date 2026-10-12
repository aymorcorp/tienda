/* EL GUARDIAN DEL BOTON DE PAGAR.

   Dos casillas sin marcar, y una de ellas manda sobre el boton.

   La de ACEPTAR: hasta que la persona la marca ella, el boton no se puede
   picar. La ley federal de Estados Unidos pide un si expreso, y una casilla
   que ya viene marcada no es el si de nadie — es un si que alguien puso en su
   nombre. Por eso la casilla no se marca aqui tampoco: ni al cargar, ni
   «porque ya la marco la vez pasada».

   La del NEGOCIO: no manda sobre nada. Lo que responda se escribe en el boton
   y de ahi viaja DENTRO de la compra, para que quede guardado con su fecha
   donde importa — en la compra, no en una base de datos nuestra.

   Y si alguien apaga los programas del navegador, el boton se queda sin poder
   picarse. Eso es a proposito: antes que cobrarle a alguien que no acepto
   nada, no se le cobra. */
(function(){
  var bloques = [].slice.call(document.querySelectorAll('.antesdepagar'));
  bloques.forEach(function(b){
    var acepto = b.querySelector('.cajaacepto');
    var negocio = b.querySelector('.cajanegocio');
    var boton = b.querySelector('button.comprar');
    var falta = b.querySelector('.faltaaceptar');
    if(!acepto) return;

    /* Las casillas se vacian al cargar. Algunos navegadores las dejan como
       estaban al volver atras, y eso convertiria un si viejo en un si de hoy. */
    acepto.checked = false;
    if(negocio) negocio.checked = false;

    function mirar(){
      if(boton){
        boton.disabled = !acepto.checked;
        boton.classList.toggle('apagado', !acepto.checked);
        /* Lo que la persona dijo, escrito en el boton. De ahi lo toma el
           cobro y lo mete dentro de la compra. */
        boton.dataset.negocio = (negocio && negocio.checked) ? 'si' : 'no';
      }
      if(falta) falta.hidden = acepto.checked;
    }
    acepto.addEventListener('change', mirar);
    if(negocio) negocio.addEventListener('change', mirar);
    mirar();
  });
})();
