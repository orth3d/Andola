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
                        action: 'search_proveedor'
                    }
                    return queryParameters;
                },
                processResults: function(data) {
                    return {
                        results:data
                    };
                },
            },
            placeholder: 'Nombre del proveedor',
            minimumInputLength: 1,
        }
    );
    
    $('.btnAddProveedor').on('click', function(){
        $('#myModalProveedor').modal('show');
    })

    $('#myModalProveedor').on('hidden.bs.modal', function(e) {
        $('#frmProveedor').trigger('reset');
    })

    $('#frmProveedor').on('submit', function(e){
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_proveedor');
        submitWithAjax(window.location.pathname, 'Guardar', '¿Registrar proveedor?', parameters, function(response) {
            var newOption = new Option(response.nombre, response.id, false, true)
            $('select[name="proveedor"]').append(newOption).trigger('select');
            $('#myModalProveedor').modal('hide');
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


