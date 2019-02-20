$("#static-tag > div").click(function () {
    console.log($(this));

    $("#static-tag > div").removeClass("choice-tag");

    $(this).addClass("choice-tag");

    $("#static-content > div").addClass("no-vis");

    var id = $(this)[0].id;

    $("#" + id + "-point").removeClass("no-vis");
});
