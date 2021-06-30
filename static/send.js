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




$('#email').click(function () {


  $(this).removeAttr('placeholder');

    // if($(this).val() == ''){
    //     $(this).attr('placeholder' , "My PlaceHolder");
    // }

});

$('#phone').click(function () {


  $(this).removeAttr('placeholder');

    // if($(this).val() == ''){
    //     $(this).attr('placeholder' , "My PlaceHolder");
    // }

});

$('#send').click(function () {


  $(this).removeAttr('placeholder');

    // if($(this).val() == ''){
    //     $(this).attr('placeholder' , "My PlaceHolder");
    // }

});


// $('.label').on('hover',() => {
//     $(this).attr('placeholder', {'visibility': 'hidden'});
// });
// not working hide placeholder

// for each placeholder in lable class show/hide palceholder value on hover
// $('.label').mouseenter('show',(){
//     $(this).attr('placeholder') 
// });
//   $('.label').mouseout('hide',(){
//     $(this).attr('placeholder');
//   });

// $("").on({
//     mouseover: function() {
//         $("#dd").stop().show();
//     },
//     mouseout: function() {
//         $("#dd").stop().hide();
//     } })
  
// $('#form').on('focus', function(){
//     if(!$(this).data('placeholder')){
//         $(this).data('placeholder', $(this).attr('placeholder'));
//     }
//     $(this).attr('placeholder', "");
// }).on('focusout', function(){
//     if($(this).val()==""){
//         $(this).attr('placeholder', $(this).data('placeholder'));
//     }
// });


$('.header').mouseenter(function(){ 
  $(this).toggleClass('expand'); 
  $(this).parent().parent().find('tbody tr').slideToggle(600); 
});
$('table').mouseleave(function(){   
  $(this).find('.header').toggleClass('expand'); 
  $(this).find('tbody tr').slideToggle(600);
});

