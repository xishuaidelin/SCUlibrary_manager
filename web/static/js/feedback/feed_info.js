/**
 * Created by 蟋蟀的林 on 2018/11/30.
 */
;
var feed_info_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_feedback_set .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var feedback_target = $(".wrap_feedback_set textarea[name=feedback]");
            var feedback= feedback_target.val();

           //参数有效性判断
            if( feedback.length < 1){
                common_ops.tip( "请输入要回复的内容~",feedback_target );
                return false;
            }

            btn_target.addClass("disabled");//当最初这层检查过关后，将这个保存按钮禁止掉
            var data={
                feedback:feedback,
                id: $(".wrap_feedback_set input[name=id]").val()
            };
            $.ajax({
                url:common_ops.buildUrl("/feedback/feed_info"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");//将禁止解除
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/feedback/feedback");
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
    feed_info_ops.init();
} );