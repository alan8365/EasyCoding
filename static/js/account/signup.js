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
 });


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
 });

 /*==================================================================
 [ Validate ]*/
 let input = $('.validate-input .user-input');

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
     if ($input.val() === "") {
         $input.parent().attr("data-validate", "此欄不能為空");

         return false;
     }

     if ($input.attr('name') == 'email') {

         //檢查信箱地址是否合法
         if ($input.val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {

             $input.parent().attr("data-validate", "郵件格式需為: ex@abc.xyz");

             return false;
         }

     } else if ($input.attr('name') == "username") {

         if ($input.val().length < 4) {
             $input.parent().attr("data-validate", "帳號需4個字以上");

             return false;
         }

     } else if ($input.attr('name') == "password") {

         if ($input.val().length < 4) {
             $input.parent().attr("data-validate", "密碼需4個字以上");

             return false;
         }

         if ($input.val().match(/^[a-zA-Z0-9]+$/) == null) {
             $input.parent().attr("data-validate", "密碼只能使用英數字");

             return false;
         }

     } else if ($input.attr('name') == "check-password") {
         //檢查密碼兩次輸一致
         if ($input.val() != $("input[name=password]").val()) {
             $input.parent().attr("data-validate", "第二次密碼錯誤");

             return false;
         }
     }
 }

 function showValidate(input) {
     let thisAlert = $(input).parent();

     $(thisAlert).addClass('alert-validate');
 }

 function hideValidate(input) {
     let thisAlert = $(input).parent();

     $(thisAlert).removeClass('alert-validate');
 }
