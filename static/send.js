'use strict';

$("#send").on("click",()=> {
    $.get('/bulk', (res)=> {
        alert (res)
    });
}) 

$.backstretch("/img/wallpaper2.png");


setTimeout(function() {
    $('.flashes').slideUp(300);
}, 6000); // <-- time in milliseconds


$('#email').click(function () {
  $(this).removeAttr('placeholder');
});

$('#phone').click(function () {
  $(this).removeAttr('placeholder');
});

$('#occ_date').click(function () {
  $(this).removeAttr('placeholder');
});
  

$('#send_dt').click(function () {
  $(this).removeAttr('placeholder');
});
  

$('thead').click(function(){ 
  $(".tr_toggle").slideToggle('slow');
});


