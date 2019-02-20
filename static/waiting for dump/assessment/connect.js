/**
 * Created by USER on 2018/4/3.
 */

$("#GO").click(function(){
    $.post("demo_test.asp", function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
    });
});