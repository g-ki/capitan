(function() {
  const delete_buttons = document.querySelectorAll('a.nodes-delete');

  delete_buttons.forEach(element => destroy_element_onclick(element));
})();
