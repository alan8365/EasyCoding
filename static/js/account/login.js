 /*==================================================================
                                              [ Focus Contact2 ]*/
 $('.user-input').each(function () {
     $(this).on('blur', function () {
         if (validate(this) == false) {
             $(this).addClass('has-val');
         } else {
             $(this).removeClass('has-val');
         }
     })
 })


 /*==================================================================
 [ Validate after type ]*/
 $('.validate-input .user-input').each(function () {
     $(this).on('blur', function () {
         if (validate(this) == false) {
             showValidate(this);
         } else {
             $(this).parent().addClass('true-validate');
         }
     })
 })

 /*==================================================================
 [ Validate ]*/
 var input = $('.validate-input .user-input');

 $('.validate-form').on('submit', function () {
     var check = true;

     for (var i = 0; i < input.length; i++) {
         if (validate(input[i]) == false) {
             showValidate(input[i]);
             check = false;
         }
     }

     return check;
 });


 $('.validate-form .user-input').each(function () {
     $(this).focus(function () {
         hideValidate(this);
         $(this).parent().removeClass('true-validate');
     });
 });

 function validate(input) {
     let $input = $(input);

     //檢查是否為空值
     if ($input.val() == "") {
         $input.parent().attr("data-validate", "此欄不能為空");

         return false;
     }

     if ($input.attr('name') == "username") {

         if ($input.val().length < 4) {
             $input.parent().attr("data-validate", "帳號需4個字以上");

             return false;
         }

     }

     if ($input.attr('name') == "password") {

         if ($input.val().length < 4) {
             $input.parent().attr("data-validate", "密碼需4個字以上");

             return false;
         }

         if ($input.val().match(/^[a-zA-Z0-9]+$/) == null) {
             $input.parent().attr("data-validate", "密碼只能使用英數字");

             return false;
         }

     }
 }

 function showValidate(input) {
     var thisAlert = $(input).parent();

     $(thisAlert).addClass('alert-validate');
 }

 function hideValidate(input) {
     var thisAlert = $(input).parent();

     $(thisAlert).removeClass('alert-validate');
 }
