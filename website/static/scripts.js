// Script that uses ajax to update only part of the page (used jquery)
$(document).on('click', '#get-quotes', function () {
    $('#quotes-table').load('/get_quotes')
});

$(document).on('click', '#get-quote', function () {
    $('#quote').load('/ #quote')
});

$(document).ready(function () {
    $('#navbarNavDarkDropdown').on('keypress', function () {
        $(this).dropdown('toggle');
    });
});