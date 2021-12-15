const inputDate = document.getElementById('form');

    inputDate.addEventListener('submit', () => {

        fetch('static/example.json')
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            console.log(data);
          });

    })


