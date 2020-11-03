var tablePost;
// $(document).ready(function(){
    function getData() {
        tablePost = $('#data').DataTable( {
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
                },
                dataSrc: ""
            },
            columns: [
                {"data": "title"},
                {"data": "thumbnail"},
                {"data": "timestamp"},
                {"data": "author"},
                {"data": "opciones"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a data-fancybox data-type="iframe" href="/blog/post/' + row.id + '/" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a>';
                        buttons += '<a href="/gest/blog/edit/' + row.id + '" class="btn-warning btn-xs"><i class="far fa-edit"></i></a> ';
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
                // alert('Tabla cargada');
              }
            });
    };
// });

$(function () {

    getData();

    // $('#myModalPost').modal('show');
    

    $('#data tbody')
        .on('click', 'a[rel="delete"]', function (){
            // modal_title.find('span').html('Editar Cliente');
            var tr = tablePost.cell($(this).closest('td, li')).index();
            var data = tablePost.row(tr.row).data(); // obtener todos los datos del registro
            console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submitWithAjax(window.location.pathname, 'Eliminar', '¿Estás seguro de querer eliminar este registro?', parameters, function() {
                $('#myModalPost').modal('hide');
                tablePost.ajax.reload();//getData();
            });
        });
});