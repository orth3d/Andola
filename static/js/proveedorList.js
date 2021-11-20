var tableProveedor;
function getData() {
    
    tableProveedor = $('#data').DataTable( {
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "categoria"},
            {"data": "tel1"},
            {"data": "mail"},
            {"data": "location"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="see" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a> ';
                    buttons += '<a href="/gest/proveedores/edit/' + row.id + '" class="btn-warning btn-xs"><i class="far fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn-danger btn-xs"><i class="far fa-trash-alt"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {
            //alert('Tabla cargada');
          }
    });
};

$(function () {

    getData();
    
    
    $('#data tbody')
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableProveedor.cell($(this).closest('td, li')).index();
            var data = tableProveedor.row(tr.row).data(); // obtener todos los datos del registro
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este registro?', parameters, function() {
                $('#myModalProveedor').modal('hide');
                tableProveedor.ajax.reload();//getData();
            });
    })
        .on('click', 'a[rel="see"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableProveedor.cell($(this).closest('td, li')).index();
            var data = tableProveedor.row(tr.row).data(); // obtener todos los datos del registro
            console.log(data);
            Swal.fire({
                title: data.nombre,
                html: '<table class="table table-sm text-left">' +
                '<tbody>' +
                  '<tr>' +
                    '<th scope="row">ID</th>' + 
                    '<td>' + data.id + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Categoría</th>' + 
                    '<td>' + data.categoria + '</td>' +
                  '</tr>' +
                  // '<tr>' +
                  //   '<th scope="row">Clasificación</th>' + 
                  //   '<td>' + data.subcategoria + '</td>' +
                  // '</tr>' +
                  '<tr>' +
                    '<th scope="row">Teléfono</th>' + 
                    '<td>' + data.tel1 + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Teléfono 2</th>' + 
                    '<td>' + data.tel2 + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">E-mail</th>' + 
                    '<td>' + data.mail + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Dirección</th>' + 
                    '<td>' + data.address + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Sitio Web</th>' + 
                    '<td>' + data.website + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Zona</th>' + 
                    '<td>' + data.location + '</td>' +
                  '</tr>' +
                '</tbody>' +
              '</table>'
            });
    });

    $('form').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submitWithAjax(window.location.pathname, 'Guardar', '¿Estás seguro de querer guardar este registro?', parameters, function() {
            $('#myModalProveedor').modal('hide');
            tableProveedor.ajax.reload();//getData();
        });
    });
});