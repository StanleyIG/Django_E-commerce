
console.log(csrftoken)


$(document).ready(function () {
    $("#form1").submit(function (e) {
        e.preventDefault();
        var url = $(this).attr("action");
        // console.log(url);
        // console.log($("#user-form1").val());
        // стираю созданные ранее тэги с сообщениями об ошибки которые были ранее
        $('.error-message').remove();
        // Удаление класса ошибки с полей
        $('.input').removeClass('error');


        var formData = {
            csrfmiddlewaretoken: csrftoken, // Сервер Django тправит код 403 на запрос если гн отправить csrf токен
            username: $('input[placeholder="username"]').val(),
            password: $('input[placeholder="password"]').val(),
            email: $('input[placeholder="email"]').val(),
        };

        console.log(formData);
        // $.ajax({
        //     type: "POST",
        //     url: url,
        //     data: formData,
        //     dataType: "json",
        //     success: function (response) {
        //         console.log(response);
        //     },
        //     error: function (error) {

        //     }
        // });
        $.ajax({
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            success: function (response) {
                if (response.message == 'ok') {
                    console.log(response.message);
                    // при успешной регистрации сработает анимация переключения форму на форму аутентификации
                    container.classList.remove("right-panel-active");

                    // window.location.href = "/login/"; можно редиректнуть на другую страницу с помощью JS

                } else {
                    // console.log(response);
                    for (var field in response.errors) {
                        // Получение элемента поля
                        var fieldElement = $('input[placeholder="' + field + '"]');
                        // Добавление класса ошибки
                        fieldElement.addClass('error');
                        // Создание элемента с сообщением об ошибке
                        var errorMessage = $('<span class="error-message">' + response.errors[field] + '</span>');
                        // Добавление элемента сообщения об ошибке после поля
                        fieldElement.after(errorMessage);
                    }
                }
            },
            error: function (error) {
                // Обработка ошибки запроса
            }
        });

    });
});


// Аутентификация пользователя
// Плавный рендеринг на другую страницу. Демонстрация работы Django в паре c JQuery
$(document).ready(function () {
    $(".container__form.container--signin form").submit(function (e) {
        e.preventDefault();
        var url = $(this).attr("action");
        console.log(url);
        // стираю созданные ранее тэги с сообщениями об ошибки которые были ранее
        $('.error-message').remove();
        // Удаление класса ошибки с полей
        $('.input').removeClass('error');

        var formData = {
            csrfmiddlewaretoken: csrftoken, // Сервер Django тправит код 403 на запрос если не отправить csrf токен
            password: $('#password-login').val(),
            email: $('#username-login').val(),
        };
        console.log(formData);

        $.ajax({
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            success: function (response) {
                //window.location.href = "/mainapp/"
                if (response.message) {
                    //window.location.href = "/mainapp/"
                    window.history.pushState({ route: 'http://127.0.0.1:8000/mainapp/' }, "EVILEG", 'http://127.0.0.1:8000/mainapp/'); // устанавливаем URL в строку браузера
                    //var newHtml = response.message;
                    $("style").remove();
                    $("head").empty();
                    $("body").empty();
                    //var newHtml = response.message.replace(/<script.*>.*<\/script>/igm, '');
                    // $("html").html(newHtml);
                    // console.log(newHtml);
                    // Создаем новый документ HTML
                    var newDoc = document.implementation.createHTMLDocument();
                    // Вставляем новую HTML-разметку в документ HTML
                    newDoc.documentElement.innerHTML = response.message;
                    // Получаем содержимое элементов <head> и <body> из документа HTML
                    var newHead = newDoc.head.innerHTML;
                    var newBody = newDoc.body.innerHTML;
                    // Обновляем содержимое элементов <head> и <body> на странице с помощью jQuery
                    $("head").html(newHead);
                    $("body").html(newBody);
                    //$("body").html(newHtml);
                    //     // console.log(response.message);
                    //     // // Получить ссылку на кнопку "Войти"
                    //     // const signInButton = document.querySelector('.btn');

                    //     // // Создать новый элемент <div> с классом error-message
                    //     // const errorMessage = document.createElement('div');
                    //     // errorMessage.classList.add('error-message');

                    //     // // Вставить новый элемент перед кнопкой "Войти"
                    //     // signInButton.parentNode.insertBefore(errorMessage, signInButton);

                    //     // // Добавить сообщение об ошибке в новый элемент
                    //     // errorMessage.textContent = response.error_message;
                }
                else {
                    console.log(response.error);
                }
            },
        });
    });
});


// // Аутентификация пользователя
// $(document).ready(function () {
//     $("#form2").submit(function (e) {
//         e.preventDefault();
//         var url = $(this).attr("action");
//         console.log(url);
//         // стираю созданные ранее тэги с сообщениями об ошибки которые были ранее
//         $('.error-message').remove();
//         // Удаление класса ошибки с полей
//         $('.input').removeClass('error');

//         var formData = {
//             csrfmiddlewaretoken: csrftoken, // Сервер Django тправит код 403 на запрос если не отправить csrf токен
//             password: $('input[placeholder="password"]').val(),
//             email: $('input[placeholder="email"]').val(),
//         };

//         $.ajax({
//             url: url,
//             type: "POST",
//             data: formData,
//             dataType: "json",
//             success: function (response) {
//                 if (response.message == 'error') {
//                     // console.log(response.message);
//                     // // Получить ссылку на кнопку "Войти"
//                     // const signInButton = document.querySelector('.btn');

//                     // // Создать новый элемент <div> с классом error-message
//                     // const errorMessage = document.createElement('div');
//                     // errorMessage.classList.add('error-message');

//                     // // Вставить новый элемент перед кнопкой "Войти"
//                     // signInButton.parentNode.insertBefore(errorMessage, signInButton);

//                     // // Добавить сообщение об ошибке в новый элемент
//                     // errorMessage.textContent = response.error_message;
//                 }
//                 else {
//                     console.log(response.message);
//                 }
//             },
//         });
//     });
// });