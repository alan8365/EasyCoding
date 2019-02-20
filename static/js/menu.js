$("#meun-collapse").on('show.bs.collapse', function () {
    $(".menu-toggle").addClass("xtype");
})

$("#meun-collapse").on('hide.bs.collapse', function () {
    $(".menu-toggle").removeClass("xtype");
})

var lastScrollY = 0;

window.addEventListener('scroll', function () {
    var st = this.scrollY;
    // 判斷是向上捲動，而且捲軸超過 200px
    if (st < lastScrollY) {
        $("#menu").removeClass('hideup');
    } else {
        $("#menu").addClass('hideup');

        $("#meun-collapse").collapse('hide');
    }
    lastScrollY = st;
});
