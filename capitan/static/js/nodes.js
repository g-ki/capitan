(function() {

function destroy_node_onclick(element) {
  element.addEventListener('click', event => {
    event.preventDefault();

    delete_request(element.href).then(ok => {
      if (ok) {
        element.classList.add('in-action');
        setTimeout(() => {
          location.reload();
        }, 4000);
      }
    });
  });
}


const delete_buttons = document.querySelectorAll('a.nodes-delete');
delete_buttons.forEach(element => destroy_node_onclick(element));

})();
