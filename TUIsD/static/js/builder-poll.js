// Permite agregar nuevas opciones a la encuesta
$(document).on('click', "button#add-option", function (e) {
  e.preventDefault();
  $('<div class="form-group">' +
    '<label for="opcion">Opcion:</label>' +
    '<input type="text" name="opcion" parsley-trigger="change" required ' +
    'placeholder="Escriba la opcion" class="form-control" id="opcion">' +
    '</div>').insertBefore($(this).parent())
})

function sendPollData() {
  // Declaracion de variables locales
  // opciones -> Lista con las opciones de la encuesta que se quiere crear
  var opciones = [];
  $("#modal-configuracion input[name='opcion']").each(function () {
    opciones.push($(this).val());
  });

  var pregunta = $("#modal-configuracion input[name='pregunta']").val()

  return {
    url: "../poll-config/",
    data: {
      'pregunta': pregunta,
      'opciones': opciones
    }
  }
}

function afterLoadPollConfigModal() {
  // Agregar dos opciones por defecto al cargar el modal
  $('#add-option').click();
  $('#add-option').click();
}