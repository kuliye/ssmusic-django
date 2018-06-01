$(function () {
        $("#login").click(function () {
            $.ajaxSetup({
            data:{csrfmiddlewaretoken:'{{ csrf_token }}'}})
            $.ajax({
                url:'/user/login_handle/',
                type:'POST',
                data:{
                    uname:$("#uname").val(),
                    upwd:$("#upwd").val(),
                },success:function (jieguo) {
                    if(jieguo.data==1){
                        $("#name_check").addClass('hidden').html('');
                        window.location.replace(jieguo.url);
                    }
                    else{
                        $("#name_check").removeClass('hidden').html('用户名或密码错误')
                    }
                }
            })
        })
    })