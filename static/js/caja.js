$(function(){

    $('.datos-prodyserv .datos-servicios:first').show();
    $('.menu-pys a:first').addClass('activo');
    $('.datos-prodyserv div:first').addClass('enuso');
    
    $('.menu-pys a').on('click', function() {
        
        $('.menu-pys a').removeClass('activo')
        $('.datos-prodyserv div:first').removeClass('enuso');
        $('.datos-prodyserv .datos-productos').removeClass('enuso');
        $(this).addClass('activo');
        $('.ocultar').hide();
        
        var enlace = $(this).attr('href');
        $(enlace).fadeIn(600);
        $(enlace).addClass('enuso');
        return(false);
    });  // Pestañas productos y servicios
    
});

jQuery(function ($) {
    

    $('.select2').select2(
        {
        theme: "bootstrap4",
        language: 'es'
        } 
    );


    $('#id_date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        maxDate: moment().format('YYYY-MM-DD'),
    });
}); 



