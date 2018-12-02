/**
 * Created by 蟋蟀的林 on 2018/11/30.
 */
;
var index = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        $(".wrap_search select[name=status]").change( function(){
            $(".wrap_search").submit();
        });


    }

};

$(document).ready( function(){
    index.init();
} )