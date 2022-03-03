$(function(){
    $('.datos-compras:first').show();
});

jQuery(function ($) {
    

    $('select[name="proveedor"]').select2(
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

    $('.btnAddArticulo').on('click', function(){
        $('#myModalArticulo').modal('show');
    });

    $('#myModalArticulo').on('hidden.bs.modal', function(e) {
        $('#frmArticulo').trigger('reset');
    });

    $('#frmArticulo').on('submit', function(e){
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_articulo');
        submitWithAjax(window.location.pathname, 'Guardar', '¿Registrar articulo?', parameters, function(response) {
            response.cant = 1;
            response.subtotal = 0.00;
            vents.add(response);
            var newOption = new Option(response.nombre, response.id, false, true);
            $('#myModalArticulo').modal('hide');
            $('select[name="articulo"]').append(newOption).val('');
        });
    });

    $('select[name="articulo"]').select2(
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
                        action: 'search_articulo',
                        ids: JSON.stringify(vents.get_ids()) //vents.get_ids() 
                    }
                    return queryParameters;
                },
                processResults: function(data) {
                    return {
                        results:data
                    };
                },
            },
            placeholder: 'Nombre del articulo',
            minimumInputLength: 1,
        }
    ).on('select2:select', function (e) {
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        console.log(data);
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });
    
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
        console.log(parameters);
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
    })


    $('#tblProducts tbody').on('change', 'input[name="cant"]', function() {
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].cant = cant;
        vents.calculate_invoice();
        $('td:eq(4)', tblProducts.row(tr.row).node()).html('$'+vents.items.products[tr.row].subtotal.toFixed(2));
    });
}); 


