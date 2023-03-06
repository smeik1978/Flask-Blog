// Funktion zum Laden von Daten und Erstellen der Tabelle
function loadTabData(tabID) {
    $.ajax({
    url: "/load_data/"+tabID,
    type: 'GET',
    dataType: 'json',
    success: function(response) {
        var table = $('<table class="table table-light table-striped"></table>');
        var thead = $('<thead></thead>');
        var tbody = $('<tbody></tbody>');
        table.append(thead).append(tbody);

        var headerRow = $('<tr>');
        $.each(response.data[0], function(key, value) {
        var headerCell = $('<th scope="col"></th>').text(key);
        headerRow.append(headerCell);
        });
        thead.append(headerRow);

        $.each(response.data, function(index, data) {
        var row = $('<tr>');
        $.each(data, function(key, value) {
            var cell = $('<td>').text(value);
            row.append(cell);
        });
        tbody.append(row);
        });

        $('#' + tabID + '-pane').empty().append(table);
    }
    });
}
  
// Event-Handler für den Klick auf einen Tab
$('#myTab button').click(function() {
    var tabID = $(this).attr('id');
    console.log(tabID)
    loadTabData(tabID);
});

//automatisches Laden der Daten für den aktiven Tab
var activeTabID = $('.tab-pane.active').attr('id').replace('-pane', '');
console.log(activeTabID);
loadTabData(activeTabID);

// Event-Handler für den Klick auf den "Hinzufügen" Button
$('#add-btn').click(function() {
    var activeTab = $('.tab-pane.active').attr('id');
    var tabId = activeTab.replace('-tab-pane', '').toLowerCase();
    $('#' + activeTab).load("/add_"+tabId);
});


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
