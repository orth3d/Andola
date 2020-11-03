$(document).ready(function(){
        
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

function message_error(obj) {
    var html = '';
    if (typeof(obj) === 'object'){
        html = '<ul>';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>'; //+ key + ': ' 
        });
        html += '</ul>';
    }
    else{
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
};

function submitWithAjax(url, title, content, parameters, callback) {
    
    $.confirm({
        theme: 'modern',
        title: title,
        icon: 'fas fa-info-circle',
        content: content,
        cancelButtonClass: 'btn-primary',
        buttons: {
            si: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        console.log(data);
                        if(!data.hasOwnProperty('error')) {
                            callback();
                            //location.href = '{{ list_url }}';
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function(jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function(data) {

                    });
                }
            },
            no: {
                text:"No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        },
    });
};