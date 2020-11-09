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
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                data: function(params) {
                    var queryParameters = {
                        term: params.term,
                        action: 'search_clients'
                    }
                    return queryParameters;
                },
                processResults: function(data) {
                    return {
                        results:data
                    };
                },
            },
            placeholder: 'Nombre de cliente',
            minimumInputLength: 1,
        }
    );
    
    $('.btnAddClient').on('click', function(){
        $('#myModalClient').modal('show');
    })

    $('#myModalClient').on('hidden.bs.modal', function(e) {
        $('#frmClient').trigger('reset');
    })

    $('#frmClient').on('submit', function(e){
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submitWithAjax(window.location.pathname, 'Guardar', '¿Registrar cliente?', parameters, function(response) {
            var newOption = new Option(response.full_name, response.id, false, true)
            $('select[name="cli"]').append(newOption).trigger('select');
            $('#myModalClient').modal('hide');
        });
    })

    var date = moment().format('YYYY-MM-DD');
    if($('input[name="action"]').attr('value') == 'edit'){
               date = $('input[name="date_joined"]').val();
    };
    


    $('#id_date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date : date,
        locale: 'es',
        maxDate: moment().format('YYYY-MM-DD'),
    });
}); 



