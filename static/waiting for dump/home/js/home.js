//course


var init_course = function (lesson, chapter) {
    $("#course-title").text(course[lesson][chapter][0]);
    $("#course-content").text(course[lesson][chapter][1]);
}

init_course(lesson, chapter);

$("#up-arrow").click(function () {
    if (chapter > 1) {
        chapter--;

        init_course(lesson, chapter);
    }else if(lesson > 1){
        lesson--;
        chapter = Object.keys(course[lesson]).length;

        init_course(lesson, chapter);
    }
})

$("#down-arrow").click(function () {
    if (chapter  < Object.keys(course[lesson]).length) {
        chapter++;

        init_course(lesson, chapter);
    }else if(lesson < Object.keys(course).length - 1) {
        lesson++;
        chapter = 1;

        init_course(lesson, chapter);
    }
})
