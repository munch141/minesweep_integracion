//Inicia ventana de configuración

// Este elemento es el boton del sidebar, al hacer click debe hacer que
// aparesca el modal de configuracion del patron

$(".pattern-pagination").on('click', function() {
    var modal = $('#modal-pagination');
    modal.modal('show');
    
    $.ajax({
        //url: '../pagination-config/',
        url: $(this).attr("data-action"),
        data: {
          'template': $('#template_id').val(),
          'position': $('#position').val(),
        }
    }).done(function(response) {
        modal.html(response);
    });
});
/*
// Este elemento es el boton de aceptar el modal
$(document).on('click', "#accept-pagination", function () {
  var form_options = { 
    target: '#modal-configuracion .modal-dialog', 
    data: {
      "template": $('#template_id').val(),
      "position": $('#new-ask').data('position'),
    },
    success: function() {
		
        modal.modal('hide');
    },
  };
});*/


// Este elemento es el boton de eliminar del card, al hacer click debe
// encargarse de eliminar el card y llamar a la funcion pertinente en el view
$(document).on('click', "button#eliminarPagination", function() {
  var position = $(this).attr('data-position');
  var pagination_id = $(this).parent().parent().find("input[name='idPagination']").val();
  var id = $(this).parent().parent().attr('id')

  $.ajax({
      url : $(this).attr('data-action'),
      data :  {
        'template': $('#template_id').val(),
        'position': position
      },
  })
  .done(function(data) {
    card = document.getElementById(id);
    card.remove()
  });
});

// Este elemento es el boton de configurar del card, al hacer click debe
// encargarse de llamar a la funcion perinente del view y mostrar el modal
$(document).on('click', "button#modificarPagination", function() {
  var position = $(this).attr('data-position');
  var pagination_id = $(this).parent().parent().find("input[name='idPagination']").val();
  var modal = $('#modal-pagination');
  
  $.ajax({
    url: $(this).attr('data-action') + pagination_id,
    data: {
      'template': $('#template_id').val(),
      'position': position
    }
  }).done(function(res) {
    modal.modal('show');
    modal.html(res);
  });

  $('#card-id').val(position);
  $('#position').val(position);
});
