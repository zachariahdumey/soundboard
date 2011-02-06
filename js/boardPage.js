$(document).ready(function() {
  var name = "";
  var board_id = 1;
  $("#upload_data").click(function(){
    name     = $("#name").val();
    board_id = $("#board_id").val();

    $('#upload_data').binaryUpload({
      url: $('#upload_data').parent('form').attr('action'),
      fields: {"name" : name, "board_id" : board_id },
      onStart: function(evt) {
        $('#progress').html('0%');
      },
      onFinish: function(evt) {
        $('#progress').html('100%');
        rerender();
      },
      onError: function(evt) {
        $('#progress').html('Error');
      },
      onBrowserIncompatible: function() {
          $('#progress').html('Bad browser');
      }
    });
  });
  
  function rerender(){ 
    $.get('/board/'+board_id, function(data) {
      $('#soundboard').html(data);
    });
   }
});
  
