$(function(){

    var windowHeight = $(window).height();
    var barraAltura = $('.barra-fixed').innerHeight();
    var imgUpin = imUpin;
    var imgDwin = imDwin;

    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        if(scroll > barraAltura) {
            $('.barra-fixed').addClass('barra-baja');
            $('#logo').attr('src',imgDwin);
            $('#logo').attr('height','50');
            $('.navegacion-principal a').css({'font-size':'1.7rem'});
        }else {
            $('.barra-fixed').removeClass('barra-baja');
            $('#logo').attr('src',imgUpin);
            $('#logo').attr('height','80');
            $('.navegacion-principal a').css({'font-size':'2.2rem'});
        }
    })

    // Menu Responsive 

    $('.mobile-menu').on('click',function() {
        $('.navegacion-principal').slideToggle();
    })


});