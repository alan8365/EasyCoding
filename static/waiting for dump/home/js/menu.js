var open_switch = false;

$("#menu-button").click(function () {

    //    var left = parseInt($("#menu").css("left"));

    if (!open_switch) {
        $("#menu").css({
            "left": "0px"
        });

        $(".menu-toggle").addClass("xtype");

        open_switch = true;
    } else {
        $("#menu").css({
            "left": "-300px"
        });

        $(".menu-toggle").removeClass("xtype");

        open_switch = false;
    }
});
