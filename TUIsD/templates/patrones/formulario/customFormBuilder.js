function unescapeHTML(html) {
  dom = new DOMParser().parseFromString(html, "text/html");
  return dom.documentElement.textContent;
}

function isCaptcha(formField) {
  return ('type' in formField) && (formField.type == 'captcha');
}

function formDataToHTML(formData) {
  console.log("Form JSON to HTML", formData);
  var escapeHTML = function(html) {
    escapeEl.textContent = html;
    return escapeEl.innerHTML;
  };
  var addLineBreaks = function(html) {
    return html.replace(new RegExp('&gt; &lt;', 'g'), '&gt;\n&lt;').replace(new RegExp('&gt;&lt;', 'g'), '&gt;\n&lt;');
  };
  var $markup = $('<div/>');
  console.log(formData);
  $markup.formRender({formData});
  return addLineBreaks($markup[0].innerHTML);
}
