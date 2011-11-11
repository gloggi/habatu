/*
 * Javascrizzle in tha house!
 * Author: Stefan Reinhard
 */
 
 dragActive = false;

function updateCurrent() {
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    minute = minute - (minute % 15);
    
    $('tr.current').removeClass('current');
    $('tr').each(function () {
        var $tr = $(this);
        if (hour == $tr.data('hour') && minute == $tr.data('minute')) {
            $tr.addClass('current');    
        }
    });
}

function updateClock() {
    var now = new Date();
    var h = now.getHours();
    var m = now.getMinutes();
    var s = now.getSeconds();
    m = m < 10 ? '0'+m : m;
    s = s < 10 ? '0'+s : s;
    $('#clock').html(h+":"+m+":"+s);
}
 
 function checkConflicts() {
     $('tr').each(function (i, tr) {
        $(tr).removeClass('conflicts');
        var team_count = { };
        $(tr).find('span.team').each(function (i, team) {
            var id = $(team).data('team-id');
            var hidden = $(team).data('hidden');
            if (hidden) return false;
            if (team_count[id] !== undefined) {
                team_count[id]++;
            } else {
                team_count[id] = 1;
            }
        });
        
        // Look for conflicts
        for (team in team_count) {
            if (team_count[team] > 1) {
                $(tr).addClass('conflicts');
            };
        }
    });
 }
 
 function markTeams() {
    var selected = $(this).val();
    $("span.team").css({'font-weight': 'normal'});
    $("span.team." + selected).css({'font-weight': 'bold'}); 
    $(".game_entry").removeClass('mark');
    $(".game_entry").each(function () {
      if ($(this).has("span.team." + selected).length) {
        $(this).addClass('mark');
      }
    });
 }
 
$(function () {
  $("a.fancy").fancybox({
        'type' : 'iframe',
        'width': 570,
        'transitionIn': 'none', 
        'transitionOut': 'none',
        'speedIn': 100, 
        'speedOut': 100,
        'padding': 0,
        'onStart': function () {
            return !dragActive;
        }
  });
  
  checkConflicts();
  updateCurrent();
  updateClock();
  setInterval(updateClock, 500);
  
  $('.game_entry').draggable({
    revert:'invalid',
    start: function(event, ui) {
        dragActive = true;
        //ui.helper.unbind('click').click(function() { return false; });
    },
    stop: function(event, ui) {
        setTimeout(function() {dragActive = false}, 20);
    }
  });
  
  $('td').droppable({
    hoverClass: "drop",
	drop: function( event, ui ) {
	    // Add to td
        ui.draggable.appendTo(this).css({'left':0, 'top':0});
        
        // Update data
        var id = ui.draggable.data('id');
        var data = {
          time : $(this).data('timeframe'),
          location : $(this).data('location')
        };
        $.post('/update_dnd/' + id + '/', data, function () {});
        
        // Look for conflicts
        checkConflicts();
    }
  });
  
  /* team marker */
  $("#teammarker").change(markTeams);
});
