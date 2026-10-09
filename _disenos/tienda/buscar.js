/* El buscador. Vive en el navegador: no hay servidor detras, asi que
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
  function escoger(c){
    var hay = chips.filter(function(o){ return o.dataset.cat === c; })[0];
    if(!hay) return false;
    chips.forEach(function(o){ o.classList.remove('on'); });
    hay.classList.add('on');
    cat = c;
    pintar();
    return true;
  }
  q.addEventListener('input', pintar);
  chips.forEach(function(ch){
    ch.addEventListener('click', function(){ escoger(ch.dataset.cat); });
  });
  /* Las bandas de la portada llegan aqui con la categoria en la direccion,
     por ejemplo «catalogo/#impuestos». Hay que abrir el catalogo con ese
     filtro ya puesto: si no, la banda dice «ver lo de este oficio» y enseña
     todo. Si la direccion trae algo que no existe, no se toca nada. */
  function porLaDireccion(){
    var c = (location.hash || '').replace('#', '');
    if(c) escoger(c);
  }
  porLaDireccion();
  window.addEventListener('hashchange', porLaDireccion);
})();
