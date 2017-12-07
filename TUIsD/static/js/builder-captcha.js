$(".forms").click(function() {
  event.preventDefault();
});

// Crea un nuevo patron de interaccion una vez se selecciona en el sidebar.
// Específicamente, crea el patrón CAPTCHA.
// Esta función debe escribir el HTML que tendrá el Modal y al final deberá
// mostrarlo con un show.
function afterLoadCaptchaConfigModal() {
  url = 'http://localhost:8000'
  $.ajax({
    url: '/servecaptcha/generate_apikey/',
    type: 'get',
    dataType: 'json',
    success: function(data) {
      $("#public_key").val(data.public_key);
      $("#private_key").val(data.private_key);
    },
    failure: function(data) {
      alert("ERROR");
    }
  });
};

// Función que envía un Captcha a Django para guardarlo en el modelo.
function sendCaptchaData() {
  return {
    url : "../captcha-config/",
    data : {
            'public_key': $('#public_key').val(),
            'private_key': $('#private_key').val(),
           },
  }
}

$(document).on('click', '#actualizarCaptcha', function() {
  url = 'http://localhost:8000';
  public_key = "demoPublicKey";
  $.ajax({
    url: '/servecaptcha/generate_captcha/'+public_key+'/',
    type: 'get',
    dataType: 'json',
    success: function(data) {
      $("#image_captcha").attr("src", url + "/servecaptcha/image/" + data.captcha_id);
      $("#captcha-id").val(data.captcha_id);
      $("#audioCaptcha").attr("src", url + "/servecaptcha/audio/" + data.captcha_id);
    },
    failure: function(data) {
      alert("ERROR");
    }
  });
});
