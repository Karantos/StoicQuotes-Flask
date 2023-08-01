// Script that gets more quotes from server (used jquery)
$(document).on('click', '#get-quotes', function () {
    $('#quotes-table').load('/get_quotes')
});

$(document).on('click', '#get-quote', function () {
    $('#quote').load('/ #quote')
});
