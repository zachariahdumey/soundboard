// This function plays sound
var sounds = {};
function soundPlay(soundNumber) {
  // This uses an associative array to store one audio element per sound
  // In some browsers (possibly all?), only a limited number of Audio objects
  // will be constructed, so this method reuses the same element to play
  // the same sound. Note that .load() must be called before the sound
  // will be played a second time.
  var sound = sounds["" + soundNumber];
  if (sound == null) {
    sounds["" + soundNumber] = new Audio("/sound/"+soundNumber);
    sound = sounds["" + soundNumber];
  } else {
    sound.load();
  }
  sound.play();
}

// This is supposed to set the dialog initialization for all the buttons.
function setDialog() {
  $("div[name=name_dialog]").dialog({
    autoOpen: false,
    modal: true,
    buttons: {
      "Rename": function() {
        board_id = $("#board_id").val();
        sound_id = $(this).attr('id').substring(12);
        new_name = $("#name_"+sound_id).val();
        $.post('/editSound', {
            new_name: new_name,
            soundboard_id: board_id,
            sound_id: sound_id
          },
          function (data) {
            $("#play_"+sound_id).button("option", "label", data)
          }
        );
        $(this).dialog("close");
      },
      "Cancel": function() {
        $(this).dialog("close");
      },
    }
  });

  $("#board_name_dialog").dialog({
    autoOpen: false,
    modal: true,
    buttons: {
      "Rename": function() {
        board_id = $("#board_id").val();
        new_name = $("#new_board_name").val();
        $.post('/editName', {
            new_name: new_name,
            soundboard_id: board_id
          },
          function(data) {
            $("#board_name_button").button("option", "label", data)
          }
        )
        $(this).dialog("close");
      },
      "Cancel": function() {
        $(this).dialog("close");
      },
    }
  });

  $("#add_sound_dialog").dialog({
    autoOpen: false,
    modal: true,
  });
}
  
function rerender(){
  board_id = $("#board_id").val();
  $.get('/board/'+board_id, {rerender: 1}, function(data) {
    $('#soundboard').html(data);
    setupSortables();
    setupButtons();
    $(setDialog());
    setupUpload();
  });
}

$(document).ready(function() {
  var name = "";
  var board_id = 1;
  setupSortables();
  setupButtons();
  setupUpload();
});
 
function setupUpload(){
  $("#upload_file").click(function(){
    name     = $("#name").val();
    board_id = $("#board_id").val();

    $('#upload_file').binaryUpload({
      url: '/upload',
      fields: {"name" : name, "board_id" : board_id },
      onStart: function(evt) {
        // Set the upload file path to the empty string so that
        // subsequent uploads do not upload multiple files.
        $('#upload_file').val('');
        $('#progress').html('0%');
      },
      onFinish: function(evt) {
        $('#progress').html('100%');
        rerender();
        $("#add_sound_dialog").dialog('close');
      },
      onError: function(evt) {
        $('#progress').html('Error');
      },
      onBrowserIncompatible: function() {
          $('#progress').html('Bad browser');
      }
    });
  });
}

function setupSortables(){
 $(function() {
    $( "#sortable" ).sortable({
      update: function(event, ui) {
        board_id = $("#board_id").val();
        var serialized_ids = $('#sortable').sortable('serialize');
        $.post('/editOrder',
            {serialized_ids: serialized_ids, soundboard_id: board_id},
            function(data) { });
      }
    });
    $( "#sortable" ).disableSelection();
  });
  $(setDialog());
} 

function setupButtons(){
  $(function() {
    $("button[name=sound_button]")
      .button()
      .click(function() {
        sound_id = $(this).attr('id').substring(5);
      }
    );
    $("button[name=button_edit_sound]")
      .button( {
        label: "dummy text",
        text: false,
        icons: {
          primary: "ui-icon-wrench"
        }
      }
    )
    .click(function() {
      board_id = $("#board_id").val();
      sound_id = $(this).attr('id').substring(5);
      new_name = $("#name_"+sound_id).val();
      $("#name_dialog_"+sound_id).dialog("open");
      $("#name_"+sound_id)
        .attr("value", $("#play_"+sound_id)
        .button("option", "label"))
    })
    .parent()
      .buttonset();
  });

  $(function() {
    $("#board_name_button")
      .button()
      .click(function() {
        alert("Name Clicked");
      });
    $("#edit_name_button")
      .button( {
        label: "dummy text",
        text: false,
        icons: {
          primary: "ui-icon-wrench"
        }
      })
      .click(function() {
        board_id = $("#board_id").val();
        new_name = $("#new_board_name").val();
        $("#board_name_dialog").dialog("open");
        $("#new_board_name")
          .attr("value", $("#board_name_button")
            .button("option", "label"))
      })
      .parent()
        .buttonset();

    $("#empty_sound")
      .button()
      .click(function() {
        alert("Empty Sound Clicked");
      });
    $("#empty_sound").button("disable");
    $("#add_sound_button")
      .button( {
        label: "dummy text",
        text: false,
        icons: {
          primary: "ui-icon-plus"
        }
      })
      .click(function() {
        board_id = $("#board_id").val();
        $("#add_sound_dialog").dialog("open");
      })
      .parent()
        .buttonset();
  });    
}
