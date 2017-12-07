// Se muestra el modal inicial para crear nombre de template
$(document).ready(function() {
  $('#new_template').modal('show');
});

// Una vez se agrega el primer patron al template, se elimina
// el mensaje de bienvenida
$(".pattern, .pattern-carousel, .pattern-accordion").on('click', function() {
  $("#welcome").hide();
});

// Se bloquea el modal del nombre del template para evitar que
// desaparezca al hacer click fuera de el o presionando la te-
// cla ESC. 
$('#new_template').modal({
  backdrop: 'static',
  keyboard: false
});

// Una vez tenemos el nombre del template se hace request a la
// aplicacion para guardar el nuevo template en bd
$('#accept_name_template').click(function(){
  $('#title').text($('#template_name').val())
  $.ajax({
      url : "../new-template/",
      data :  {'name': $('#template_name').val()},

  })
  .done(function(data){
    if(data){
      $('#template_id').val(data.id);
      $('#new_template').modal('hide');
    }
  });
});
