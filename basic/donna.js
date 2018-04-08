window.addEventListener('load', function() {
  document.getElementById('make_event').addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('http://localhost:5000/add_event/', {
      method: 'POST',
      body: new FormData(document.getElementById('make_event')),
    }).then(response => console.log(response));
  })
})
