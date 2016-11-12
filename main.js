function resizeRows() {
    var paddingTop = 100;
    var x = $(window).height();
    $(".row").height(x - paddingTop);
}

$(document).ready(resizeRows);
$(window).resize(resizeRows);