/* EL BUSCADOR Y LOS FILTROS, HECHOS PARA CINCO MIL.

   Antes miraba las cajas pintadas en la pantalla. Con diecisiete daba igual;
   con cinco mil, la pagina pesaria 4.3 MB y el navegador tendria que mirar
   cinco mil cajas en cada letra que se escribe.

   Ahora la tienda entera vive en «indice.js», un archivo aparte que se
   baja una vez y se queda guardado. Filtrar es mirar una lista en memoria —
   igual de rapido con cinco mil que con diecisiete— y solo se PINTAN las que
   se ven: de 24 en 24, con un boton de «ver mas».

   La pagina trae dentro las primeras 24 ya escritas. Eso es lo que ve quien
   llega, lo que leen los buscadores y lo que vera Paddle. Cuando el indice
   termina de bajar, este programa toma el relevo sin que se note.

   NO SABE CUANTAS FORMAS DE BUSCAR HAY: lee los botones que encuentra. Si
   mañana se añade una en ejes.json, esto no cambia. */
(function(){
  var q = document.getElementById('q');
  var rej = document.getElementById('rej');
  var nada = document.getElementById('nada');
  var masBtn = document.getElementById('vermas');
  if(!q || !rej) return;
  var botones = [].slice.call(document.querySelectorAll('.chip[data-eje]'));

  var DE_GOLPE = 24;
  var TODOS = null;      /* la tienda entera, cuando llegue */
  var VISTOS = DE_GOLPE; /* cuantos se estan enseñando */
  var puesto = {};
  botones.forEach(function(b){ puesto[b.dataset.eje] = 'todo'; });

  /* LO QUE ESTA PUESTO DE VERDAD. «puesto» tiene las cuatro formas de
     buscar, casi siempre en «todo»; esto tiene solo las que la persona ha
     escogido. Mirar una lista vacia no cuesta nada, y recorrer cuatro por
     cada uno de cinco mil productos, si. */
  var ACTIVOS = [];
  function rehacerActivos(){
    ACTIVOS = [];
    for(var eje in puesto){
      if(puesto[eje] !== 'todo') ACTIVOS.push([eje, puesto[eje]]);
    }
  }

  /* Lo escrito, preparado una vez antes de mirar los productos — no cinco
     mil veces. */
  var TEXTO = '';
  function prepararTexto(){ TEXTO = q.value.trim().toLowerCase(); }

  function cumple(p, eje, valor){
    if(valor === 'todo') return true;
    var v = p.a[eje];
    return !!v && v.indexOf(valor) >= 0;
  }

  function pasa(p, saltandose){
    /* Se busca en el titulo, el tema y el principio de la descripcion. La
       descripcion entera no se guarda: con cinco mil productos eran dos
       megas y medio solo de texto que casi nadie busca. «p.s» es eso ya en
       minusculas y en un solo trozo, hecho al recibir la tienda. */
    if(TEXTO && p.s.indexOf(TEXTO) < 0) return false;
    for(var i = 0; i < ACTIVOS.length; i++){
      if(ACTIVOS[i][0] === saltandose) continue;
      var v = p.a[ACTIVOS[i][0]];
      if(!v || v.indexOf(ACTIVOS[i][1]) < 0) return false;
    }
    return true;
  }

  function tarjeta(p){
    /* CON LOS MISMOS ATRIBUTOS que las que escribe el armador. Una
       tarjeta ha de ser igual la pinte quien la pinte: si no, lo que
       se ve en pantalla deja de poder comprobarse. */
    var at = '';
    for(var eje in p.e){ at += ' data-' + eje + '="' + p.e[eje] + '"'; }
    return '<div class=celda' + at + '>' +
      '<a class=libro href="../' + p.id + '/index.html">' +
      '<div class=obj style="background-image:url(../../img/' + p.g + '-mockup.jpg)"></div>' +
      '<h4>' + p.t + '</h4><p>' + p.c + '</p><b>' + p.p + '</b></a></div>';
  }

  function pintar(){
    if(!TODOS) return;           /* todavia no ha llegado: se deja lo escrito */
    prepararTexto();
    rehacerActivos();
    var hay = TODOS.filter(function(p){ return pasa(p, null); });
    rej.innerHTML = hay.slice(0, VISTOS).map(tarjeta).join('');
    if(nada) nada.hidden = hay.length > 0;
    if(masBtn){
      var faltan = hay.length - VISTOS;
      masBtn.hidden = faltan <= 0;
      masBtn.textContent = MAS_TEXTO.replace('{n}', faltan > DE_GOLPE ? DE_GOLPE : faltan);
    }
    contar();
  }

  /* Cuantos quedarian si le picaras. No cuenta el de su propia fila, porque
     escoger uno de esa fila sustituye al que haya. El que daria cero se
     apaga: nadie le pica a un filtro para encontrarse una pantalla vacia. */
  function contar(){
    if(!TODOS) return;
    /* UNA PASADA POR FILA DE BOTONES, no una por boton. Entre los botones de
       una misma fila lo unico que cambia es el valor, asi que en la misma
       pasada se cuentan todos. Con veintidos botones y cinco mil productos,
       eso es cuatro recorridos en vez de veintidos. */
    var cuentas = {};
    for(var eje in puesto){
      var c = cuentas[eje] = {todo: 0};
      for(var i = 0; i < TODOS.length; i++){
        var p = TODOS[i];
        if(!pasa(p, eje)) continue;
        c.todo++;
        var partes = p.a[eje];
        if(!partes) continue;
        for(var k = 0; k < partes.length; k++){
          c[partes[k]] = (c[partes[k]] || 0) + 1;
        }
      }
    }
    botones.forEach(function(b){
      var n = (cuentas[b.dataset.eje] || {})[b.dataset.valor] || 0;
      var e = b.querySelector('.cuantos');
      if(!e){ e = document.createElement('span'); e.className = 'cuantos'; b.appendChild(e); }
      e.textContent = n;
      b.classList.toggle('vacio', n === 0);
    });
  }

  function escoger(eje, valor, pintarYa){
    var b = botones.filter(function(o){
      return o.dataset.eje === eje && o.dataset.valor === valor; })[0];
    if(!b) return false;
    botones.forEach(function(o){
      if(o.dataset.eje === eje) o.classList.remove('on'); });
    b.classList.add('on');
    puesto[eje] = valor;
    VISTOS = DE_GOLPE;
    if(pintarYa !== false) pintar();
    return true;
  }

  q.addEventListener('input', function(){ VISTOS = DE_GOLPE; pintar(); });
  botones.forEach(function(b){
    b.addEventListener('click', function(){
      escoger(b.dataset.eje, b.dataset.valor);
      guardarEnLaDireccion();
    });
  });
  if(masBtn){
    masBtn.addEventListener('click', function(){ VISTOS += DE_GOLPE; pintar(); });
  }

  function guardarEnLaDireccion(){
    var partes = [];
    for(var eje in puesto){
      if(puesto[eje] !== 'todo') partes.push(eje + '=' + puesto[eje]);
    }
    history.replaceState(null, '', partes.length ? '#' + partes.join('&') : location.pathname);
  }

  function porLaDireccion(){
    for(var eje in puesto){ puesto[eje] = 'todo'; }
    botones.forEach(function(o){
      o.classList.toggle('on', o.dataset.valor === 'todo'); });
    var h = (location.hash || '').replace('#', '');
    h.split('&').forEach(function(par){
      if(!par) return;
      var k = par.split('='), eje = k[0], valor = k[1];
      if(valor === undefined){ escoger('tema', eje, false); }
      else { escoger(eje, valor, false); }
    });
    VISTOS = DE_GOLPE;
    pintar();
  }
  window.addEventListener('hashchange', porLaDireccion);

  /* La tienda entera viene en «indice.js», que la pagina carga antes que
     esto. Si no llegara —archivo que falta, red que se corta— NO se rompe
     nada: se quedan las primeras tarjetas, ya escritas en la pagina, y se
     puede entrar a cualquiera de ellas. */
  if(typeof INDICE !== 'undefined' && INDICE && INDICE.productos){
    TODOS = INDICE.productos;
    /* TODO LO QUE NO CAMBIA NUNCA, preparado aqui una sola vez en lugar de
       rehacerlo en cada letra que se escribe: el texto que se busca, en
       minusculas y en un solo trozo, y los temas de cada producto ya
       partidos por las comas. */
    for(var i = 0; i < TODOS.length; i++){
      var p = TODOS[i];
      p.s = (p.t + ' ' + p.c + ' ' + p.b).toLowerCase();
      p.a = {};
      for(var eje in p.e){ p.a[eje] = String(p.e[eje]).split(','); }
    }
  }
  porLaDireccion();
})();
