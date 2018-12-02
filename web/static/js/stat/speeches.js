/**
 * Created by 蟋蟀的林 on 2018/12/1.
 */
;
var speech_index={
    init:function(){
        this.draw();
    },
        draw:function () {
        chart_ops.speech_setOption();
        $.ajax({
            url:common_ops.buildUrl("/chart/speeches"),
            dataType:'json',
            success:function( res ){
                chart_ops.drawSpeech( $('#container'),res.data )
            }
        });
    }
};

$(document).ready(function () {
    speech_index.init();
});