function updateDataFromDB(event) {
    const leistungSelect = event.target; // Das Select-Element, das das Leistungsfeld darstellt
    const selectedOption = leistungSelect.options[leistungSelect.selectedIndex]; // Die ausgewählte Option
    const name = leistungSelect.id
    console.log(name);
    const leistung = {
      id: selectedOption.value,
      name: name
    }; // Ein Objekt, das sowohl die ID als auch den Namen des ausgewählten Leistungsdatensatzes enthält
    console.log(leistung);
    fetch('/get_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(leistung) // Das Leistungsfeld als JSON-Objekt codieren und an den Server senden
    })
    .then(response => response.json())
    .then(data => {
      const abrechnungsjahrField = document.getElementById('abrechnungsjahr');
      abrechnungsjahrField.value = data.abrechnungsjahr;
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
