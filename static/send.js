'use strict';

$("#send").on("click",()=> {
    $.get('/bulk', (res)=> {
        alert (res)
    });
}) 

// $(".flashes").on("submit",()=> {

// })
setTimeout(function() {
    $('.flashes').slideUp(300);
}, 6000); // <-- time in milliseconds

// $('.label').on('hover',() => {
//     $(this).attr('placeholder', {'visibility': 'hidden'});
// });
// not working hide placeholder
$('.label').mouseenter('show',(){
    $(this).attr('placeholder') 
});
  $('.label').mouseout('hide',(){
    $(this).attr('placeholder');
  });
  
