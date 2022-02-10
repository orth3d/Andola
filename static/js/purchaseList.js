var tblSale;

$(function () {

    tblSale = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        pageLength: 25,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "proveedor"},
            {"data": "date_joined"},
            {"data": "total"},
            {"data": ""},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="details" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a> ';
                    buttons += '<a href="/gest/pagos/update/' + row.id + '/" class="btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [1],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    return data.nombre;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            var comment = data.comment;
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_art',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "artic.nombre"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#comment').html('<br>'+'<h5>Comentarios: </h5>'+'<p>' + comment + '</p>');
            $('#addedby').html('<br>'+'<p>Agregado por <b>' + data.added + '</b></p>');
            $('#myModalDet').modal('show');
        })
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data(); // obtener todos los datos del registro
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este producto?', parameters, function() {
                $('#myModalSale').modal('hide');
                tblSale.ajax.reload();//getData();
            });
        });
});