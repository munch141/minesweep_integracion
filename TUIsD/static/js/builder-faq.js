$(document).on('click', "button#add_more_faqs", function(e){
  e.preventDefault();
  $('<div class="form-group">' +
      '<label for="pregunta">Pregunta:</label>' +
      '<input type="text" name="pregunta" parsley-trigger="change" required placeholder="Escriba la pregunta " class="form-control">'+
    '</div>' +
    '<div class="form-group">' +
      '<label for="respuesta">Respuesta:</label>' +
      '<textarea type="text" name="respuesta" parsley-trigger="change" required placeholder="Escriba la respuesta " class="form-control"></textarea> '+
    '</div>').insertBefore($(this).parent())
})

// Permite enviar request a la app para guardar en bd el nuevo patron que se creara
function sendFAQData() {
  // Declaracion de variables locales
  // opciones -> Lista con las opciones de la encuesta que se quiere crear
  var preguntas = [];
  var respuestas = [];

  $("#modal-configuracion input[name='pregunta']").each(function() {
      preguntas.push($(this).val());
  });

  $("#modal-configuracion textarea").each(function() {
    respuestas.push($(this).val());
  });

  var categoria = $("#modal-configuracion input[name='categoria']").val()

  return {
    url : "../faq-config/",
    data : {
            'categoria': categoria,
            'preguntas': preguntas,
            'respuestas': respuestas,
           },
  }
}

function afterLoadFAQConfigModal() {
  // Agregar dos opciones por defecto al cargar el modal
  $('#add_more_faqs').click();
}