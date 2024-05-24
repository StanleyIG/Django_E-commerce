'use strict';

window.onload = function () {
    console.log('DOM ready');
    let basket = document.querySelector('.basket_list');
    // let basket = document.querySelector('.basket_list .basket_record input');
    // let basket = document.querySelector('.basket_record input');
    console.log(basket);
    basket.onclick = function (e) {
        console.log('target', e.target);
    }
}