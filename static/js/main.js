$(function(){

    var windowHeight = $(window).height();
    var barraAltura = $('.barra').innerHeight();
    var imgUp = imUp;
    var imgDw = imDw;

    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        if(scroll > windowHeight) {
            $('.barra').addClass('barra-baja');
            $('#logo').attr('src',imgDw);
            $('#logo').attr('height','50');
            $('.navegacion-principal a').css({'font-size':'1.7rem'});
            $('.dropdown-content a').css({'font-size':'1.6rem'});
        }else {
            $('.barra').removeClass('barra-baja');
            $('#logo').attr('src',imgUp);
            $('#logo').attr('height','80');
            $('.navegacion-principal a').css({'font-size':'2.2rem'});
            $('.dropdown-content a').css({'font-size':'1.6rem'});
        }
    })

    // Menu Responsive 

    $('.mobile-menu').on('click',function() {
        $('.navegacion-principal').slideToggle();
    })


});

// (function () {
//     'use strict';

//     document.addEventListener('DOMContentLoaded', function () {
//         console.log("Listo!");
//         //Campos Datos Usuario
//         var nombre = document.getElementById('nombre');
//         var apellido = document.getElementById('apellido');
//         var email = document.getElementById('email');

//         //Campos Carrito
//         var aceite_1 = document.getElementById('aceite_1');

//         //Botones y divs
//         //var calcular = document.getElementById('calcular');
//         var errorDiv = document.getElementById('error');
//         var botonRegistro = document.getElementById('btnRegistro');
//         var botonPagar = document.getElementById('btnPagar');
//         var lista_productos = document.getElementById('lista-productos');
//         var suma = document.getElementById('suma-total');

//         aceite_1.addEventListener('blur', calcularMontos);

//         // nombre.addEventListener('blur', validarCampos);
//         // apellido.addEventListener('blur', validarCampos);
//         // email.addEventListener('blur', validarCampos);
//         // email.addEventListener('blur', validarMail);
        
//         // function validarCampos() {
//         //     if(this.value == '') {
//         //         errorDiv.style.display = 'block';
//         //         errorDiv.innerHTML = "Este campo es obligatorio";
//         //         this.style.border = '1px solid red';
//         //     } else {
//         //         errorDiv.style.display = 'none';
//         //         this.style.border = '1px solid #cccccc'; 
//         //     }
//         // };

//         // function validarMail() {
//         //     if(this.value.indexOf("@") > -1) {
//         //         errorDiv.style.display = 'none';
//         //         this.style.border = '1px solid #cccccc'; 
//         //     } else {
//         //         errorDiv.style.display = 'block';
//         //         errorDiv.innerHTML = "Ingresa un email válido";
//         //         this.style.border = '1px solid red';
//         //     }
//         // }

//         //calcular.addEventListener('click', calcularMontos);

//         function calcularMontos(event) {
//             event.preventDefault();
//             var numeroArticulo_1 = parseInt(aceite_1.value, 10) || 0;

//             var totalPagar = (numeroArticulo_1 * 50);

//             console.log("Total a pagar: " + totalPagar);

//             var listadoProductos = [];

//             if (numeroArticulo_1 >= 1) {
//                 listadoProductos.push(numeroArticulo_1 + ' Aceite');

//             }

//             console.log(listadoProductos);
//             lista_productos.style.display = 'block';
//             lista_productos.innerHTML ='';
//             for(var i = 0; i < listadoProductos.length; i++) {
//                 lista_productos.innerHTML += listadoProductos[i] + '<br/>';
//             }
//             suma.innerHTML = '$ ' + totalPagar.toFixed(2);


//         }


//     });  //DOM CONTENT LOADED
// })();
