// variable global que guarda el form builder
var $formBuilder = null;

var fbOptions = {
  disabledActionButtons: ['data', 'clear', 'save']
};

function sendFormData() {
  formData = $formBuilder.formData;
  return {
    url : "../form-config/",
    data : {
      'form_json': formData,
    }
  }
}

function afterLoadFormConfigModal() {
  // Initialize form builder plugin
  $formBuilder = $('#fb-editor').formBuilder(fbOptions);
}

function afterLoadEditFormConfigModal () {
  // Sacamos la posicion del modal, y extraemos el form json del card correspondiente a esa posicion.
  var position  = $('#modal-configuracion').data('position'),
      formData  = $('.fb-rendered-form[data-position="'+ position +'"]').data('form-json'),
      $fbEditor = $('#fb-editor'),
      options   = Object.assign({}, fbOptions, {
        formData: JSON.stringify(formData),
        dataType: 'json'
      });
  // Initialize form builder plugin
  $formBuilder = $fbEditor.formBuilder(options);
}

function afterSendFormData(data) {
  // Render el form recien creado
  $(".pattern-container[data-position='"+ data.position +"'] .fb-rendered-form").html(formDataToHTML(data.form_json));
}

$(document).ready(function() {
  // Si hay forms, renderizar el json de los form como html
  $('.pattern-container .fb-rendered-form').each(function(i, elem) {
    $(elem).html(formDataToHTML($(elem).data('form-json')));
  })
})