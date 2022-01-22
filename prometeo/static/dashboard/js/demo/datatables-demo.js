// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('.table-bordered').each(function(index, element) {
    $(element).DataTable();
  });
});
