function generateChart(year_month_list,income_TWD_list,expend_TWD_list,end_meets_list){
    var chartDom = document.getElementById('endmeets');
var myChart = echarts.init(chartDom);
var option;

option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data: ['income', 'expend', 'End Meets']
    },
    xAxis: [
        {
            type: 'category',
            data: year_month_list,
            axisPointer: {
                type: 'shadow'
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'QTY',
            //min: 0,
            //max: 250,
            //interval: 50,
            axisLabel: {
                formatter: '{value} '
            }
        },
    ],
    series: [
        {
            name: 'income',
            type: 'bar',
            stack: 'Ad',
            data: income_TWD_list
        },
        {
            name: 'expend',
            type: 'bar',
            stack: 'Ad',
            data: expend_TWD_list
        },
        {
            name: 'End Meets',
            type: 'line',
            //yAxisIndex: 1,
            data: end_meets_list
        }
    ]
};

option && myChart.setOption(option);
}
