// Archivo que se encarga de todas las funciones en JS del Navbar.
// Funciones para cargar los datos una vez se cargue el modal.
// Funciones para cuando se acepta la configuración puesta en el modal.
// Funciones utils para navbar.
var elements = [];
var counter = 1;
var limit = 8

// Datos que deben cargarse en el modal de configuración del navbar cuando Este
// es CREADO (no modificado), es decir, se está seleccionando de la barra lateral.
function afterLoadNavbarConfigModal() {
  elements = [];
  counter = 1;
}

// Datos que deben cargarse en el modal de configuración del navbar cuando éste
// es MODIFICADO (no creado), es decir, cuando se hace click en el botón de
// config.
function afterLoadEditNavbarConfigModal() {
  var position  = $('#modal-configuracion').data('position'),
      navbarData  = $('.navbar-wrapper[data-navbar-position="'+ position +'"]').data('navbar-json');
  // Django templates escribe los key de los diccionarios como ' en vez de "
  // Para poder aplicar JSON.parse deben tener ".
  var navbarDataFixed = navbarData.replace(/'/g, "\"");
  elements = JSON.parse(navbarDataFixed);
  counter = 1;
}

// Función que envía un Navbar a Django para guardarlo en el modelo.
// Es una función que debe retornar un diccionario que contiene el url a donde
// hacer el request y los datos que se quieran enviar.
function sendNavbarData() {
  // var elements = $("#navbar-elements").val();
  return {
    url : "../navbar-config/",
    data : {
            'elementos': JSON.stringify(elements),
           },
  }
}

function showAddSection() {
  // Obtiene el valor de la opción seleccionada
  var selectedOption = document.getElementById("elementList").value;

  // Muestra la sección correspondiente para crear el elemento a añadir y oculta
  // las demás secciones que no corresponden con la opción actual
  switch(selectedOption) {
    case "Link":
      document.getElementById("addLinkSection").style.display = "block";
      document.getElementById("addBrandSection").style.display = "none";
      document.getElementById("addDropdownSection").style.display = "none";
      break;

    case "Navbar Brand":
      document.getElementById("addBrandSection").style.display = "block";
      document.getElementById("addLinkSection").style.display = "none";
      document.getElementById("addDropdownSection").style.display = "none";
      break;

    default:
      document.getElementById("addDropdownSection").style.display = "block";
      document.getElementById("addBrandSection").style.display = "none";
      document.getElementById("addLinkSection").style.display = "none";
      break;


  };
}

function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          var newItem = " <br><div class=\"col-lg-12\">\
      <label for=\"dropdownItem" +(counter + 1)+"\">Item:</label>\
            <input type=\"text\" name=\"dropdownItem"+(counter + 1)+"\" id=\"dropdownItem"+(counter + 1)+"\"/>\
          </div>\
          <div class=\"col-lg-12\">\
            <label for=\"dropdownItem"+(counter + 1)+"Link\">Link:</label>\
            <input type=\"text\" name=\"dropdownItem"+(counter + 1)+"Link\" id=\"dropdownItem"+(counter + 1)+"Link\"/>\
          </div>";
          newdiv.innerHTML = newItem;
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}

function showAddSection() {
  // Obtiene el valor de la opción seleccionada
  var selectedOption = document.getElementById("elementList").value;

  // Muestra la sección correspondiente para crear el elemento a añadir y oculta
  // las demás secciones que no corresponden con la opción actual
  switch(selectedOption) {
    case "Link":
      document.getElementById("addLinkSection").style.display = "block";
      document.getElementById("addBrandSection").style.display = "none";
      document.getElementById("addDropdownSection").style.display = "none";
      break;

    case "Navbar Brand":
      document.getElementById("addBrandSection").style.display = "block";
      document.getElementById("addLinkSection").style.display = "none";
      document.getElementById("addDropdownSection").style.display = "none";
      break;

    default:
      document.getElementById("addDropdownSection").style.display = "block";
      document.getElementById("addBrandSection").style.display = "none";
      document.getElementById("addLinkSection").style.display = "none";
      break;


  };
}

function addElement(element) {
  switch(element) {
    case "dropdown":

      var elementsList = []
      var dropdownName      = document.getElementById("dropdownName").value;

      for (i = 1; i <= counter; i++) {
        var dropdownItem     = document.getElementById("dropdownItem"+i).value;
        var dropdownItemLink = document.getElementById("dropdownItem"+i+"Link").value;

        var object = {name: dropdownItem,link: dropdownItemLink}
        elementsList.push(object)
      }

      var object = {type: "dropdown", name: dropdownName, elements:elementsList}
      elements.push(object);

      // Se genera codigo html para el dropdown.
      var newdiv = document.createElement('li');
            var newItem = " <li class=\"nav-item dropdown\">\
                  <a class=\"nav-link dropdown-toggle\" id=\"#\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">"+dropdownName+"</a>";
            newdiv.innerHTML = newItem;
            document.getElementById("dynamicLinks").appendChild(newdiv);
      break

    case "link":
      var linkName = document.getElementById("linkName").value;
      var linkLink = document.getElementById("linkLink").value;
      var linkOption = document.getElementById("linkOption").value;
      var object = {type: "link", name: linkName, link: linkLink, option: linkOption}
      elements.push(object);

      // Se genera codigo html para los links.
      var newdiv = document.createElement('li');

        if (linkOption == "disabled"){
          var newItem = "<li class=\"nav-item\"> <a class=\"nav-link disabled\" href=\"#\">"+linkName+"<span class=\"sr-only\">(current)</span></a> </li>";
        }
        else {
          var newItem = "<li class=\"nav-item\"><a class=\"nav-link\" href=\"#\">"+linkName+"<span class=\"sr-only\">(current)</span></a>";
        }
            newdiv.innerHTML = newItem;
            document.getElementById("dynamicLinks").appendChild(newdiv);
      break


    default:
      var brandName = document.getElementById("navbarBrandName").value;
      var brandImage = document.getElementById("navbarBrandLogo").value;
      var object = {type: "brand", name: brandName, link: brandImage}
      elements.push(object);
      // $("#navbar-elements").val(elements + JSON.stringify(object));

      // Se genera codigo html para el Brand.
      var newdiv = document.createElement('a');
            var newItem = "<a class=\"navbar-brand\" href=\"#\">"+brandName+"</a>";
            newdiv.innerHTML = newItem;
            document.getElementById("dynamicBrans").appendChild(newdiv);
      break
  };

  document.getElementById("addLinkSection").style.display = "none";
  document.getElementById("addBrandSection").style.display = "none";
  document.getElementById("addDropdownSection").style.display = "none";
};

$(document).on('click', '#generarCodigo', function() {
  document.getElementById('location').value = JSON.stringify(elements);
});
