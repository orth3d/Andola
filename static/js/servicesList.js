var tableService;
function getData() {
    
    tableService = $('#data').DataTable( {
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
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "precio"},
            {"data": "descripcion"},
            {"data": "stock"},
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
                    buttons += '<a href="#" rel="delete" class="btn-danger btn-xs"><i class="far fa-trash-alt"></i></button>';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(data > 0){
                        return '<span class="badge badge-success">'+data+'</span>'
                    }
                    return '<span class="badge badge-danger">'+data+'</span>'
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
        $('#myModalArticle').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="precio"]').val(data.precio);
            $('input[name="descripcion"]').val(data.descripcion);
            $('input[name="stock"]').val(data.stock);
            $('#myModalArticle').modal('show');            
    })
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este articulo?', parameters, function() {
                $('#myModalArticle').modal('hide');
                tableService.ajax.reload();//getData();
            });
    })
        .on('click', 'a[rel="see"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tableService.cell($(this).closest('td, li')).index();
            var data = tableService.row(tr.row).data(); // obtener todos los datos del registro
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
                    '<th scope="row">Categoria</th>' + 
                    '<td>' + data.categoria + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Precio</th>' + 
                    '<td>$ ' + data.precio + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Descripción</th>' + 
                    '<td>' + data.descripcion + '</td>' +
                  '</tr>' +
                  '<tr>' +
                    '<th scope="row">Stock</th>' + 
                    '<td>' + data.stock + '</td>' +
                  '</tr>' +
                '</tbody>' +
              '</table>'
            });
    });

    $('#form').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submitWithAjax(window.location.pathname, 'Guardar', '¿Estás seguro de querer guardar este articulo?', parameters, function() {
            $('#myModalArticle').modal('hide');
            tableService.ajax.reload();//getData();
        });
    });
});