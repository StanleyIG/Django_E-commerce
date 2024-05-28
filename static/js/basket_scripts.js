'use strict';

// изменить колличество или удалить
window.onload = function () {
    console.log('DOM ready');
    // let basket = document.querySelector('.basket_list');
    // basket.onchange = function (e) {
    //     console.log('target', e.target);
    // }
    let basketList = $('.basket_list');
    basketList.on('change', 'input[type=number].product_qty', function (event) {
        // console.log(event.target);
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                basketList.html(data.basket_items);
            },
        });
    })
}


// удаление товаров
$(document).ready(function () {
    let basketList = $('.basket_list');    
    basketList.on('click', '.btn-round', function (event) {
        let itemPk = $(this).data('pk');
        $.ajax({
            url: '/basket/delete/basket/item/' + itemPk + '/',
            success: function (data) {
                console.log(data);
                basketList.html(data.basket_items);
                // Обновление информации о корзине
                // $('.basket_summary')...
            },
        });
    });
});

