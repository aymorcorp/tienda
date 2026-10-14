/* LOS TRES FORMULARIOS: ESCRIBENOS, PROBADORES Y DARME DE BAJA.

   No mandan nada. ARMAN un correo con lo que la persona escribio y lo abren en
   su propio programa de correo; ella le da enviar.

   POR QUE ASI, Y NO MANDANDOLO DESDE AQUI. No hay servidor ni llave de correo
   puesta. Se podria inventar un sitio donde guardar lo que la gente escribe,
   pero entonces hay que cuidarlo, declararlo en la politica de privacidad, y
   poder borrarlo cuando alguien lo pida. Esto no guarda nada en ninguna parte,
   y la persona VE exactamente lo que va a mandar antes de mandarlo.

   El dia que haya llave de correo se cambia por un envio de verdad sin tocar
   ni un texto de la pagina.

   Y si alguien tiene los programas apagados, los formularios no se quedan
   mudos: debajo de cada uno esta el correo escrito, para escribir a mano. */
(function(){
  var cartas = [].slice.call(document.querySelectorAll('form.carta'));
  if(!cartas.length) return;

  function valor(id){
    var e = document.getElementById(id);
    if(!e) return null;
    if(e.type === 'checkbox') return e.checked;
    return (e.value || '').trim();
  }

  /* Lo que se escribe en el correo: el rotulo que la persona leyo y lo que
     contesto. Asi quien lo reciba lee lo mismo que ella vio, y no un nombre
     de campo que no significa nada. */
  function rotulo(id){
    var l = document.querySelector('label[for=' + id + ']');
    return l ? l.textContent.trim() : id;
  }

  cartas.forEach(function(f){
    f.addEventListener('submit', function(ev){
      ev.preventDefault();
      var lineas = [], asunto = document.title;

      [].slice.call(f.querySelectorAll('input, select, textarea'))
        .forEach(function(e){
          if(!e.id) return;
          var v = valor(e.id);
          if(v === '' || v === null) return;
          if(e.type === 'checkbox'){
            if(!v) return;
            var lab = e.closest('label');
            lineas.push((lab ? lab.textContent.trim() : e.id) + ': si');
            return;
          }
          lineas.push(rotulo(e.id) + ': ' + v);
        });

      if(!lineas.length) return;

      var para = f.dataset.para || 'aymorcorp@gmail.com';
      var carta = 'mailto:' + para
        + '?subject=' + encodeURIComponent(asunto)
        + '&body=' + encodeURIComponent(lineas.join('\n\n'));

      /* Se deja apuntado en el propio formulario lo que se va a mandar,
         antes de mandarlo. No es adorno: es lo unico que permite COMPROBAR
         desde fuera que el correo lleva las palabras que la persona
         escribio. Sin esto, la prueba solo podria ver que el formulario no
         se recargo, y un programa que no hace nada tambien pasa esa
         prueba. */
      f.dataset.carta = carta;
      location.href = carta;
    });
  });
})();
