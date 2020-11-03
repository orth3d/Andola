var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');

function generate_report() {
    
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
    };

    if(date_range !== null ){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn bg-olive btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-xs',
                download: 'open',
                orientation: 'portrait',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['10%','35%','15%','20%','20%','0%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columnDefs: [
            {
                targets: [-2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            // {
            //     targets: [-1],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var buttons = '<a href="#" rel="details" class="btn-secondary btn-xs"><i class="far fa-eye"></i></a> ';
            //         buttons += '<a href="/gest/sales/update/' + row.id + '/" class="btn-warning btn-xs"><i class="fas fa-edit"></i></a> ';
            //         buttons += '<a href="/gest/sales/invoice/' + row.id + '/" target="_blank" class="btn-info btn-xs"><i class="fas fa-file-pdf"></i></a> ';
            //         buttons += '<a href="#" rel="delete" class="btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
            //         return buttons;
            //     }
            // },
            // {
            //     targets: [1],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var n = data.nombre + ' ' + data.apellido;
            //         return n;
            //     }
            // },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    $('input[name="date_range"]').daterangepicker().on('apply.daterangepicker', function(ev, picker) {
        date_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    });
    generate_report();
});