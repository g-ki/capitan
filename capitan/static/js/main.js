// send DELETE request to @href
function delete_request(href) {
  // return Promise.resolve(true)

  return fetch(href, {
    method: 'DELETE',
    credentials: 'same-origin',
  }).then(res => {
    console.info()
    console.info(res)
    return true
  }).catch(err => {
    console.error(err)
    return false
  })
}
