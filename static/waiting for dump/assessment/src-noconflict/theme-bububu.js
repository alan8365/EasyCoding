ace.define("ace/theme/bububu", [], function (require, exports, module) {

    exports.isDark = true;
    exports.cssClass = "ace-bububu";
    exports.cssText = ".ace-bububu .ace_gutter {\
background: #262424;\
color: #E6E1DC\
}\
.ace-bububu .ace_print-margin {\
width: 1px;\
background: #262424\
}\
.ace-bububu {\
background-color: rgb(48, 57, 99);\
color: #E6E1DC\
}\
.ace-bububu .ace_cursor {\
color: #FFFFFF\
}\
.ace-bububu .ace_marker-layer .ace_selection {\
background: #494949\
}\
.ace-bububu.ace_multiselect .ace_selection.ace_start {\
box-shadow: 0 0 3px 0px #1C1C1C;\
}\
.ace-bububu .ace_marker-layer .ace_step {\
background: rgb(102, 82, 0)\
}\
.ace-bububu .ace_marker-layer .ace_bracket {\
margin: -1px 0 0 -1px;\
border: 1px solid #404040\
}\
.ace-bububu .ace_marker-layer .ace_active-line {\
background: rgb(62, 70, 108)\
}\
.ace-bububu .ace_gutter-active-line {\
background-color: #333435\
}\
.ace-bububu .ace_marker-layer .ace_selected-word {\
border: 1px solid #494949\
}\
.ace-bububu .ace_invisible {\
color: #404040\
}\
.ace-bububu .ace_entity.ace_name.ace_tag,\
.ace-bububu .ace_keyword,\
.ace-bububu .ace_meta,\
.ace-bububu .ace_meta.ace_tag,\
.ace-bububu .ace_storage {\
color: #FC803A\
}\
.ace-bububu .ace_constant,\
.ace-bububu .ace_constant.ace_character,\
.ace-bububu .ace_constant.ace_character.ace_escape,\
.ace-bububu .ace_constant.ace_other,\
.ace-bububu .ace_support.ace_type {\
color: #68C1D8\
}\
.ace-bububu .ace_constant.ace_character.ace_escape {\
color: #B3E5B4\
}\
.ace-bububu .ace_constant.ace_language {\
color: #E1C582\
}\
.ace-bububu .ace_constant.ace_library,\
.ace-bububu .ace_string,\
.ace-bububu .ace_support.ace_constant {\
color: #8EC65F\
}\
.ace-bububu .ace_constant.ace_numeric {\
color: #7AB8FF\
}\
.ace-bububu .ace_invalid,\
.ace-bububu .ace_invalid.ace_deprecated {\
color: #FFFFFF;\
background-color: #FE3838\
}\
.ace-bububu .ace_fold {\
background-color: #FC803A;\
border-color: #E6E1DC\
}\
.ace-bububu .ace_comment,\
.ace-bububu .ace_meta {\
font-style: italic;\
color: #AC4BB8\
}\
.ace-bububu .ace_entity.ace_other.ace_attribute-name {\
color: #EAF1A3\
}\
.ace-bububu .ace_indent-guide {\
background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWOQkpLyZfD09PwPAAfYAnaStpHRAAAAAElFTkSuQmCC) right repeat-y\
}";

    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass);
});
(function () {
    ace.require(["ace/theme/bububu"], function (m) {
        if (typeof module == "object" && typeof exports == "object" && module) {
            module.exports = m;
        }
    });
})();
