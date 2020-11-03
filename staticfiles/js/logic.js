var tblProducts;
var vents = {
    items: {
        cli: '',
        date_joined: '',
        total: 0.00,
        products: []
    },
    calculate_invoice: function() {
        var total = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cant * dict.precio;
            total += dict.subtotal;
        });
        this.items.total = total;
        $('input[name="total"]').val(this.items.total.toFixed());
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "precio"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a href="#" rel="remove" type="button" class="btn-danger btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    // render: function (data, type, row) {
                    //     return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="'+row.cant+'">';
                    // }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            // rowCallback(row, data){
// 
            // },
            initComplete: function (settings, json) {

            }
        });
    },
};



$(function(){
    
    $('.btnAdd').on('click', function() {
        var id = $(this).attr('id')
        // var cant = 
        // alert(cant);
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': $('.enuso').attr('id'),
                'id': id,
            },
            dataType: 'json',
        }).done(function (data) {//response(data);
            // console.clear();
            data.cant = $('#cant'+data.nombre).val(), //cant;
            data.subtotal = 0.00;
            vents.items.products.push(data);
            console.log(vents.items);
            vents.list();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    });

    $('.btnRemoveAll').on('click', function () {
        vents.items.products=[];
        vents.list();
    });

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function(){
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products.splice(tr.row, 1);
            vents.list();
        });

    $('form').on('submit', function(e) {
        e.preventDefault();
        if(vents.items.products.length === 0){
            message_error('Debe agregar al menos un producto');
            return false;
        }
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submitWithAjax(window.location.pathname, 'Guardar', '¿Estás seguro de querer guardar esta venta?', parameters, function() {
            location.href = '/gest/sales/';
        });
    });

    // vents.list();
    
});