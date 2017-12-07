// Function executed after loading config modal for carousel pattern
function afterLoadCarouselConfigModal() {
  $('.formset_row').formset({
    addText: 'Añadir elemento',
    deleteText: 'Eliminar elemento',
    prefix: 'content_set'
  });

  $('#modal-configuracion .modal-dialog').addClass("modal-lg");

  return;
}

$(document).on('click', "#accept-carousel", function () {
  var form_options = { 
    target: '#modal-configuracion .modal-dialog', 
    data: {
      "template": $('#template_id').val(),
    },
    dataType: 'json',
    success: function(responseText, statusText) {
      console.log(responseText, statusText);

      $('#modal-configuracion').modal('hide');

      if (responseText.position != null) {
        if ($(".pattern-container[data-position='"+ responseText.position +"']").length) {
          $(".pattern-container[data-position='"+ responseText.position +"']").replaceWith(responseText.html);
        }
        else {
          $(".builder").append(responseText.html);
        }
      }

      $('#guardar').show();
      var tem_id = $('#template_id').val().toString()
      var link = "/revisar_template/"+ tem_id
      $('#preview').attr('href',link)
      $('#preview-form').attr('action',link)
      $('#frm1_submit').show();
      $('#preview').show();

      $('#modal-configuracion').removeData()
    },
  };

  if ($('#modal-configuracion').data('position') !== undefined) {
    form_options.data.position = $('#modal-configuracion').data('position');
  }

  $('#carousel-create').ajaxForm(form_options);
});
