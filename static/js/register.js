        var username_check=false;
        var upwd_check=false;
        var cupwd_check=false;
        var uemail_check=false;
        $(function () {
            $('#yanzheng').click(function () {
                $.ajax({
                    url:'/user/sendmail/',
                    type:'GET',
                    data:{
                        uemail:$('#uemail').val()
                    }
                    ,success:function () {
                        alert('已成功发送邮箱')
                    }
                })

            })

            $('#uname').blur(function () {
                var len=$('#uname').val().length;
                if (len>=5 && len<=20){
                $.ajax({
                    url:'/user/name_exist/',
                    type:'GET',
                    data:{
                        username:$('#uname').val(),
                    }
                    ,success:function (result) {
                        if(result.result==1){
                            $("#name_check").removeClass('hidden').html('用户名已经存在');
                            username_check=false;
                        }
                        else{
                            $("#name_check").addClass('hidden');
                            username_check=true;
                        }
                    }
                })

                }
                else{
                        $("#name_check").removeClass('hidden').html('用户名必须在5到20字符之间');
                        username_check=false;
                }
            })

            $('#upwd').blur(function () {
                var len=$('#upwd').val().length
                if(len>=8 && len<=20){
                    upwd_check=true;
                    $("#pwd_check").addClass('hidden');
                }
                else{
                    upwd_check=false;
                    $("#pwd_check").removeClass('hidden').html('密码必须要在8到20位之间');
                }
            })

            $('#cupwd').blur(function () {
                if ($('#upwd').val()==$(this).val()){
                    cupwd_check=true;
                    $("#cpwd_check").addClass('hidden');
                }
                else{
                    cupwd_check=false;
                    $("#cpwd_check").removeClass('hidden').html('两次输入的密码必须一致')
                }
            })

            $('#uemail').blur(function () {
                var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if(re.test($(this).val())){
                    uemail_check=true;
                    $("#email_check").addClass('hidden');
                    $("#yanzheng").removeAttr('disabled')
                }
                else{
                    uemail_check=false;
                    $("#email_check").removeClass('hidden').html('邮箱格式不正确')
                    $("#yanzheng").attr('disabled','disabled')
                }
            })




        })
