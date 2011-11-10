/*
 * Javascrizzle in tha house!
 * Author: Stefan Reinhard
 */
 
$(function () {
  $("a.fancy").fancybox({
        'type' : 'iframe',
        'width': 570,
        'speedIn': 100, 
        'speedOut': 100,
        'padding': 0
  });
    
  $("#teammarker").change(function () {
    
    var selected = $(this).val();
    
    $("span.team").each(function () {
      $(this).css({'font-weight': 'normal'});
    });
    
    $("span.team." + selected).each(function () {
      $(this).css({'font-weight': 'bold'});
    });
    
    $("td").each(function () {
      $(this).css({'background-color': '#fff'});
    });
    
    $("td").each(function () {
      if ($(this).has("span.team." + selected).length) {
        
        $(this).css({'background-color': '#ffc'});
      }
    });
  });
});
