var tblProducts;
var vents = {
    items: {
        provee: '',
        date_joined: '',
        total: 0.00,
        products: [],
        comment: ''
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function(key,value){
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function() {
        var total = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cant * dict.precio;
            total += dict.subtotal;
        });
        this.items.total = total;
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
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
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a href="#" rel="remove" class="btn-danger btn-xs"><i class="fas fa-times"></i></a>';
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
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cant+'">';
                    }
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
            rowCallback(row, data){
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        });
        console.log(this.get_ids());
    },
};



$(function(){
    
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

    $('#frmPurch').on('submit', function(e) {
        
        var proveedor = $('select[name="proveedor"]').on('select2:select', function (e) {
            proveedor = e.params.data;
            proveedor = proveedor.text;
        });

        if(proveedor.length <= 2){
            proveedor = $(proveedor[0]).children("option:selected").text();
        } else if(proveedor == null){
            proveedor = data.nombre;
        };
        
        e.preventDefault();
        if(vents.items.products.length === 0){
            message_error('Debe agregar al menos un producto');
            return false;
        }
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.comment = $('input[name="comment"]').val();
        vents.items.provee = $('select[name="proveedor"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        console.log(parameters);
        var i;
        var productos = '<ul class="list-group">';
        for (i = 0; i < vents.items.products.length; i++) {
          productos += '<li class="list-group-item d-flex justify-content-between align-items-center">' + vents.items.products[i].nombre + 
          '<span class="badge badge-primary badge-pill">' + vents.items.products[i].cant + '</span></li>';
        };
        productos += '</ul>'
        var content = '<div>' + proveedor + '</div>' +
                        '<div class="text-justify">' + productos + '</div>'||vents.items.provee; //.products.cant) + ' ' + JSON.stringify(vents.items.products.cant) + '</div>';
        
        submitWithAjax(window.location.pathname, '¿Registrar compra?', content, parameters, function(response) {
            // alert_action('Notificación', '¿Imprimir ticket?', function() {
            //     window.open('/gest/sales/invoice/'+ response.id +'/', '_blank');
            //     location.href = '/gest/caja/';
            // }, function() {
            //     location.href = '/gest/caja/';
            // });
            location.href = '/gest/salidas/';
        });
    });

    // vents.list();
    
});