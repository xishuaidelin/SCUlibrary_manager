/**
 * Created by 蟋蟀的林 on 2018/11/20.
 */
;
var reset_pwd = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $("#save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var old_password = $("#old_password").val();
            var new_password = $("#new_password").val();

           //参数有效性判断
            if( !old_password){
                common_ops.alert( "请输入正确的原始密码~~" );
                return false;
            }
            if( !new_password || new_password.length < 6){
                common_ops.alert( "请输入不少于6位的新密码~~" );
                return false;
            }
            btn_target.addClass("disabled");//当最初这层检查过关后，将这个保存按钮禁止掉
            var data={
                    old_password : old_password,
                    new_password : new_password
            };

            $.ajax({
                url:common_ops.buildUrl("/user/reset-pwd"), //这里是提交到路径不是方法
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");//将禁止解除
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};

$(document).ready( function(){
    reset_pwd.init();
} );