/**
 * Created by 蟋蟀的林 on 2018/11/10.
 */
;
var new_speech = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_speech_set .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var title_target = $(".wrap_speech_set input[name=title]");
            var title= title_target.val();

            var address_target = $(".wrap_speech_set input[name=address]");
            var address= address_target.val();

            var teacher_target = $(".wrap_speech_set input[name=teacher]");
            var teacher= teacher_target.val();

            var email_target = $(".wrap_speech_set input[name=email]");
            var email= email_target.val();

            var time_target = $(".wrap_speech_set input[name=time]");
            var time= time_target.val();


            var speech_intro_target = $(".wrap_speech_set textarea[name=speech_intro]");
            var speech_intro= speech_intro_target.val();

            var teacher_intro_target = $(".wrap_speech_set textarea[name=teacher_intro]");
            var teacher_intro= teacher_intro_target.val();


           //参数有效性判断
            if( title.length < 2){
                common_ops.tip( "请输入规范的标题名，字数不少于或等于2~~",title_target );
                return false;
            }
            if( teacher.length < 1){
                common_ops.tip( "请输入讲座老师的名字~~",teacher_target );
                return false;
            }
            if( email!=""){
                var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
                var isok=reg.test(email);
                if (!isok) {
                    common_ops.tip( "请输入规范的邮箱~~",email_target );
                    return false;
                }

            }
            if( teacher_intro.length < 1){
                common_ops.tip( "请输入老师简介内容~~",teacher_intro_target );
                return false;
            }
            if( speech_intro.length < 1){
                common_ops.tip( "请输入讲座简介内容~~",speech_intro_target );
                return false;
            }
            if( time.length < 1){
                common_ops.tip( "请输入讲座时间~~",time_target );
                return false;
            }
            if( address.length < 1){
                common_ops.tip( "请输入规范的讲座地址~~",address_target );
                return false;
            }
            common_ops.alert('time',time);
            btn_target.addClass("disabled");//当最初这层检查过关后，将这个保存按钮禁止掉
            var data={
                title:title,
                teacher:teacher,
                email:email,
                teacher_intro:teacher_intro,
                speech_intro:speech_intro,
                time:time,
                address:address
            };
            $.ajax({
                url:common_ops.buildUrl("/dong_tai/new_speech"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");//将禁止解除
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/dong_tai/speeches");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                },
                error :function(res){
                    btn_target.removeClass("disabled");//将禁止解除
                    common_ops.alert( "后台错误，请稍后再试~~" );

                }
            });
        } );
    }
};

$(document).ready( function(){
    new_speech.init();
} );