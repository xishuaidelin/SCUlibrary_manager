;
var index={
    init:function(){
        this.drawPie();
    },
    drawPie:function(){
         chart_ops.index_setOption();
        $.ajax({
            url:common_ops.buildUrl("/chart/Pie"),
            dataType:'json',
            success:function( res ){
                chart_ops.drawPie( $('#container'),res.data )
            }
        });
}
};

$(document).ready(function () {
    index.init();
});