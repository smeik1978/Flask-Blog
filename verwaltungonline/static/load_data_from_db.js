$(document).ready(function () {
  // Finden des <option>-Elements, das als "selected" markiert ist
  const selectedOption = document.querySelector('select option[selected]');
  const name = selectedOption.parentNode.name;
  //console.log(name)

  // Zugriff auf den Wert des <option>-Elements
  const selectedValue = selectedOption.value;
  //console.log(selectedValue);
  const message = {
    id: selectedValue,
    name: name
  };
  //console.log('message: ', message);
  fetch(window.location.href, {  // die aktuelle URL herausfinden und verwenden
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message) // Das Select-Feld als JSON-Objekt codieren und an den Server senden
  })
  .then(response => response.json())
    .then(data => {
      //console.log('data: ', data);
      for (key in data) {
        //console.log('key :', key)
        field = document.getElementById(key);
        //console.log('field: ', field);
        if (field) {
          //console.log('field.value: ', field.value);
          //console.log('data[key]:'. data[key]);
          field.value = data[key];
        }
      }
    })
})


function updateDataFromDB(event) {
  console.log('event: ', event);
  const name = event.target.id; // Der Name des getriggerten Select-Felds
  const selectedOption = event.target.options[event.target.selectedIndex]; // Die ausgewählte Option des getriggerten Select-Felds
  const message = {
    id: selectedOption.value,
    name: name
  };
  console.log('message', message);
  fetch(window.location.href, {  // die aktuelle URL herausfinden und verwenden
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message) // Das Select-Feld als JSON-Objekt codieren und an den Server senden
  })
  .then(response => response.json())
  .then(data => {
    console.log('data: ', data);
    //console.log('window is: ', window.location.href);
    if (window.location.href == window.location.origin + '/ablesung') {
      const tablebodyElement = document.getElementById('tbody');
      if (tablebodyElement) { 
        // Vorhandene Zeilen entfernen
        const tbodyElement = tablebodyElement //.parentNode.parentNode;
        while (tbodyElement.firstChild) {
          tbodyElement.removeChild(tbodyElement.firstChild);
        }
        // Neue Zeilen erstellen und hinzufügen
        data.zaehler.forEach(zaehler => {  //for (const key in data) {
          const trElement = document.createElement('tr');
          const tdRaum = document.createElement('td');
          const tdZaehler = document.createElement('td');
          const tdTyp = document.createElement('td');
          const tdVorjahreswert = document.createElement('td');
          const tdAblesewert = document.createElement('td');
          const tdCheck = document.createElement('td');
          const inputAblesewert = document.createElement('input');

          tdRaum.textContent = zaehler.raum;
          tdZaehler.textContent = zaehler.nummer;
          tdTyp.textContent = zaehler.typ; // ToDo: Klarname statt Objekt
          tdVorjahreswert.textContent = 'Vorjahreswert'; // ToDo Abfrage in Route definieren und Ergebnis in JSON integrieren
          inputAblesewert.type = 'text';
          inputAblesewert.classList.add('form-control', 'form-control-xs');
          inputAblesewert.name = `ablesewert_${data[key]}`;
          tdAblesewert.appendChild(inputAblesewert);
          tdCheck.textContent = 'Check'; // ToDo Validierung der Zeile; z.B not None and Ableswert > Vorjahreswer

          trElement.appendChild(tdRaum);
          trElement.appendChild(tdZaehler);
          trElement.appendChild(tdTyp);
          trElement.appendChild(tdVorjahreswert);
          trElement.appendChild(tdAblesewert);
          trElement.appendChild(tdCheck);

          tbodyElement.appendChild(trElement);
        })
      }
    }
    for (key in data) {
      field = document.getElementById(key);
      if (field) {
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
