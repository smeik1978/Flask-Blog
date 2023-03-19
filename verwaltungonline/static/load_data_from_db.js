$(document).ready(function () {
  // Finden des <option>-Elements, das als "selected" markiert ist
  const selectedOption = document.querySelector('select option[selected]');
  const name = selectedOption.parentNode.name;
  console.log(name)

  // Zugriff auf den Wert des <option>-Elements
  const selectedValue = selectedOption.value;
  console.log(selectedValue);
  const message = {
    id: selectedValue,
    name: name
  };
  console.log(message);
  fetch(window.location.href, {  // die aktuelle URL herausfinden und verwenden
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message) // Das Select-Feld als JSON-Objekt codieren und an den Server senden
  })
  .then(response => response.json())
    .then(data => {
      console.log(data);
      for (key in data) {
        field = document.getElementById(key);
        if (field) {
          //console.log(field);
          //console.log(data[key]);
          field.value = data[key];
        }
      }
    })
})


function updateDataFromDB(event) {
  console.log(event);
    const name = event.target.id; // Der Name des getriggerten Select-Felds
    const selectedOption = event.target.options[event.target.selectedIndex]; // Die ausgewählte Option des getriggerten Select-Felds
    const message = {
      id: selectedOption.value,
      name: name
    };
    console.log(message);
    fetch(window.location.href, {  // die aktuelle URL herausfinden und verwenden
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message) // Das Select-Feld als JSON-Objekt codieren und an den Server senden
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      for (key in data) {
        field = document.getElementById(key);
        if (field) {
          //console.log(field);
          //console.log(data[key]);
          field.value = data[key];
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
 


// // Event-Handler für den Klick auf den "Hinzufügen" Button
// $('#add-btn').click(function() {
//     var activeTab = $('.tab-pane.active').attr('id');
      
//     // Lädt das Formular in den entsprechenden Tab
//     $('#' + activeTab).load("/add_einheiten");

//     // Event-Handler für das Submit-Event des Formulars
//     $(document).on('submit', '#AddEinheiten', function(event) {
//         event.preventDefault();
//         var form_data = $(this).serialize();
//         $.ajax({
//           url: '/add_einheiten',
//           type: 'POST',
//           data: form_data,
//           success: function(response) {
//             $('#stammdaten').html(response.html);
//           },
//           error: function(xhr) {
//             $('#stammdaten').html(xhr.responseJSON.html);
//           }
//         });
//       });     
// });
