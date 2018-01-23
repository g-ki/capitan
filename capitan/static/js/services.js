(function() {
  const delete_buttons = document.querySelectorAll('a.services-delete');

  delete_buttons.forEach(element => destroy_element_onclick(element));
})();
