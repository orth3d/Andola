var tableService;
function getData() {
    
    tableService = $('#data').DataTable( {
        responsive: true,
        autoWidth: true,
        // scrollX: true,
        destroy: true,
        // deferRender: true,
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
            {"data": "thumbnail"},
            {"data": "nombre"},
            {"data": "precio"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="see" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a> ';
                    buttons += '<a href="#" rel="edit" class="btn-warning btn-xs"><i class="far fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" type="button" class="btn-danger btn-xs"><i class="far fa-trash-alt"></i></button>';
                    return buttons;
                }
            },
            {
                targets: [1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var image = '<img src="' + row.thumbnail + '" alt="..." height="30px">';
                    return image;
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
        $('#myModalService').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('select[name="thumbnail"]').val(data.thumbnail);
            $('input[name="precio"]').val(data.precio);
            $('input[name="costo"]').val(data.costo);
            $('#myModalService').modal('show');            
    })
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este servicio?', parameters, function() {
                $('#myModalService').modal('hide');
                tableService.ajax.reload();//getData();
            });
    })
        .on('click', 'a[rel="see"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
            Swal.fire({
                title: 'Servicio',
                html: '<img src="' + data.thumbnail + '" alt="..." height="100px"></img>' +
                '<table class="table table-sm text-left">' +
                '<tbody>' +
                  '<tr>' +
                    '<th scope="row">ID</th>' + 
                    '<td>' + data.id + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Nombre</th>' + 
                    '<td>' + data.nombre + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Precio</th>' + 
                    '<td>$ ' + data.precio + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Costo</th>' + 
                    '<td>$ ' + data.costo + '</td>' +
                  '</tr>' +
                '</tbody>' +
              '</table>'
            });
    });

    $('#form').on('submit', function(e) {
        // alert('x');
        e.preventDefault();
        var parameters = new FormData(this);
        submitWithAjax(window.location.pathname, 'Guardar', '¿Estás seguro de querer guardar este producto?', parameters, function() {
            $('#myModalService').modal('hide');
            tableService.ajax.reload();//getData();
        });
    });
});