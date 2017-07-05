function resizeRows() {
    var paddingTop = 100;
    var x = $(window).height();
    $(".row").height(x - paddingTop);
}

$(document).ready(resizeRows);
$(window).resize(resizeRows);


// Change active navbar element on scroll
// https://jsfiddle.net/cse_tushar/Dxtyu/141/
$(document).ready(function () {
    $(document).on("scroll", onScroll);

    //smoothscroll
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        $(document).off("scroll");

        $('a').each(function () {
            $(this).removeClass('active');
        })
        $(this).addClass('active');

        var target = this.hash,
            menu = target;
        $target = $(target);
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top + 2
        }, 500, 'swing', function () {
            window.location.hash = target;
            $(document).on("scroll", onScroll);
        });
    });
});

function onScroll(event) {
    var scrollPos = $(document).scrollTop();
    $('.nav li').each(function () {
        var currItem = $(this);
        var currLink = $(this).find("a");
        var refElement = $(currLink.attr("href"));
        if (refElement.position().top <= scrollPos && refElement.position().top + refElement.height() > scrollPos) {
            $('.nav ul li a').removeClass("active");
            currItem.addClass("active");
        }
        else {
            currItem.removeClass("active");
        }
    });
}