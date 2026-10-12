/* LA PAGINA DE GRACIAS.

   Le pregunta a la entrega que lleva esta compra y lo ensena. No decide
   nada: si la entrega dice que no, aqui no se insiste.

   Las palabras llegan en «GRA», que las pone cada pagina en su idioma. Este
   programa es uno solo para los cinco. */
(function(){
  var estado = document.getElementById('graEstado');
  var cosas = document.getElementById('graCosas');
  var nota = document.getElementById('graNota');
  var numero = document.getElementById('graNumero');
  var correo = document.getElementById('graCorreo');
  if(!estado || !cosas) return;

  /* El numero de la compra lo pega Paddle a esta direccion. Sin el, no se
     pregunta nada: esta pagina no se abre a mano. */
  var compra = new URLSearchParams(location.search).get('_ptxn') || '';
  if(!compra){ estado.textContent = GRA.graSinCompra; return; }

  /* Hasta dos minutos esperando a que el banco confirme. Mas de eso no se
     queda dando vueltas: se le dice a quien escribir. */
  var VECES = 24, voy = 0;

  function problema(){
    estado.textContent = GRA.graProblema;
    numero.textContent = GRA.graNumero + ': ' + compra;
    numero.hidden = false;
    correo.hidden = false;
  }

  function pintar(d){
    var enOtroIdioma = false;
    cosas.innerHTML = '';
    d.cosas.forEach(function(c){
      if(c.otroIdioma) enOtroIdioma = true;
      var a = document.createElement('a');
      a.className = 'comprar';
      a.href = c.enlace;
      a.textContent = GRA.graBajar + ' · ' + c.nombre;
      cosas.appendChild(a);
    });
    cosas.hidden = false;
    estado.textContent = '';
    /* Lo de la media hora se dice SIEMPRE, no solo cuando se rompe: quien
       vuelve a los dos dias tiene que saber de antemano que no perdio nada. */
    nota.textContent = (enOtroIdioma ? GRA.graEnFrances + ' ' : '')
                       + GRA.graMediaHora;
    nota.hidden = false;
  }

  function preguntar(){
    var pet = new XMLHttpRequest();
    pet.open('GET', '/api/entrega?t=' + encodeURIComponent(compra), true);
    pet.onload = function(){
      var d = null;
      try{ d = JSON.parse(pet.responseText); }catch(e){}
      if(pet.status === 200 && d && d.cosas && d.cosas.length){ pintar(d); return; }
      /* 202 = pagado pero el banco no ha cerrado. Se vuelve a preguntar. */
      if(pet.status === 202 && voy++ < VECES){
        estado.textContent = GRA.graEspera;
        setTimeout(preguntar, 5000);
        return;
      }
      /* Una membresia de una app no trae archivo, y eso no es un fallo. */
      if(d && d.mal === 'nada-que-entregar' && d.suscripcion){
        estado.textContent = GRA.graMembresia;
        return;
      }
      problema();
    };
    pet.onerror = problema;
    pet.send();
  }
  preguntar();
})();
