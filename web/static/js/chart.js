;
//画图通用组件，在对应要画图的页面里的js中直接调用方法就可以了

var chart_ops = {
    speech_setOption:function(){
        Highcharts.setOptions({
    chart: {
        type: 'bar'
    },
    title: {
        text: '讲座预约统计'
    },
    yAxis: {
        min: 0,
        title: {
            text: '人数',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: '人次'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true,
                allowOverlap: true // 允许数据标签重叠
            }
        }
    }/*
    series: [{
        name: '1800 年',
        data: [107, 31, 635, 203, 2]
    }, {
        name: '1900 年',
        data: [133, 156, 947, 408, 6]
    }, {
        name: '2008 年',
        data: [973, 914, 4054, 732, 34]
    }]*/
});

    },
    index_setOption:function(){
        Highcharts.setOptions({
		chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false,
				type: 'pie'
		},
		title: {
				text: '书籍借阅分类统计'
		},
		tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
		},
		plotOptions: {
				pie: {
						allowPointSelect: true,
						cursor: 'pointer',
						dataLabels: {
								enabled: true,
								format: '<b>{point.name}</b>: {point.percentage:.1f} %',
								style: {
										color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
								}
						}
				}
		}

});
    },
    drawSpeech:function( target ,data ){
        target.highcharts({
            chart: {
                type: 'bar'
            },
            xAxis: {
                categories: data.categories,
                title: {
            text: '讲座'
        }
            },
            series: data.series,
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -40,
                y: 100,
                floating: true,
                borderWidth: 1,
                backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                shadow: true
    }
        });
        return chart;
    },
     drawPie:function( target ,data ){
        target.highcharts({
            chart: {
                type: 'pie'
            },
            series: [{
				name: 'Brands',
				colorByPoint: true,
                data: data.series
            }]
        });
        return chart;
    }
};