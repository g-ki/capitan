// send DELETE request to @href
function delete_request(href) {
  return fetch(href, {
    method: 'DELETE',
    credentials: 'same-origin',
  }).then(res => {
    return true
  }).catch(err => {
    return false
  })
}

function destroy_element_onclick(element) {
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
