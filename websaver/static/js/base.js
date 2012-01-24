$(document).ready(function () {
  $('#webbox').focus(function() {
    if ($(this).attr('value') == "Enter the page link you want to save.") {
      $(this).attr('value', '');
    }
  })
});