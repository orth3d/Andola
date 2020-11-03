var tableClient;
function getData() {
    
    tableClient = $('#data').DataTable( {
        responsive: true,
        autoWidth: true,
        // scrollX: true,
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
            {"data": "id"},
            {"data": "nombre"},
            {"data": "apellido"},
            {"data": "fecha_nacimiento"},
            {"data": "telefono"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="see" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a> ';
                    buttons += '<a href="#" rel="edit" class="btn-warning btn-xs"><i class="far fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" type="button" class="btn-danger btn-xs"><i class="far fa-trash-alt"></i></button>';
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
    
    $('.btnAdd').on('click', function (){
        $('input[name="action"]').val('add');
        $('#form')[0].reset();
        $('#myModalClient').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableClient.cell($(this).closest('td, li')).index();
            var data = tableClient.row(tr.row).data(); // obtener todos los datos del registro
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="apellido"]').val(data.apellido);
            $('select[name="genero"]').val(data.genero);
            $('input[name="fecha_nacimiento"]').val(data.fecha_nacimiento);
            $('input[name="telefono"]').val(data.telefono);
            $('input[name="mail"]').val(data.mail);
            $('input[name="rfc"]').val(data.rfc);
            $('#myModalClient').modal('show');
    })
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableClient.cell($(this).closest('td, li')).index();
            var data = tableClient.row(tr.row).data(); // obtener todos los datos del registro
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este registro?', parameters, function() {
                $('#myModalClient').modal('hide');
                tableClient.ajax.reload();//getData();
            });
    })
        .on('click', 'a[rel="see"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableClient.cell($(this).closest('td, li')).index();
            var data = tableClient.row(tr.row).data(); // obtener todos los datos del registro
            Swal.fire({
                title: 'Cliente',
                html: '<table class="table table-sm text-left">' +
                '<tbody>' +
                  '<tr>' +
                    '<th scope="row">ID</th>' + 
                    '<td>' + data.id + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Nombre</th>' + 
                    '<td>' + data.nombre + ' ' + data.apellido + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Género</th>' + 
                    '<td>' + data.genero + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Fecha de Nacimiento</th>' + 
                    '<td>' + data.fecha_nacimiento + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Teléfono</th>' + 
                    '<td>' + data.telefono + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">E-mail</th>' + 
                    '<td>' + data.mail + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">RFC</th>' + 
                    '<td>' + data.rfc + '</td>' +
                  '</tr>' +
                '</tbody>' +
              '</table>'
            });
    });

    $('form').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submitWithAjax(window.location.pathname, 'Guardar', '¿Estás seguro de querer guardar este registro?', parameters, function() {
            $('#myModalClient').modal('hide');
            tableClient.ajax.reload();//getData();
        });
    });
});