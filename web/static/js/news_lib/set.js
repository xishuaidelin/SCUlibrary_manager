/**
 * Created by 蟋蟀的林 on 2018/11/10.
 */
;
var news_set_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_account_set .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var title_target = $(".wrap_account_set input[name=title]");
            var title= title_target.val();

            var location_target = $("#location  option:selected");
            var location= location_target.text();

            var content_target = $(".wrap_account_set textarea[name=content]");
            var content= content_target.val();

            var id = $(".wrap_account_set input[name=id]").val();
           //参数有效性判断
            if( title.length < 2){
                common_ops.tip( "请输入规范的标题名，字数不少于或等于2~~",title_target );
                return false;
            }
            if( location.length < 5){
                common_ops.tip( "请按照提示输入正确的具体图书馆名~~",location_target );
                return false;
            }
            if( content.length < 1){
                common_ops.tip( "请输入相关公告内容~~",content_target );
                return false;
            }

            btn_target.addClass("disabled");//当最初这层检查过关后，将这个保存按钮禁止掉
            var data={
                title:title,
                location:location,
                content:content,
                id:id
            };
            $.ajax({
                url:common_ops.buildUrl("/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");//将禁止解除
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/");
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
    news_set_ops.init();
} );