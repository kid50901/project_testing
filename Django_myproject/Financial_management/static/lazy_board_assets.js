
function generateAssetsChart(year_month_list,assets_TWD_list,debt_TWD_list){
    var chartDom = document.getElementById('assets');
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
            data: ['assets', 'debt',]
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
                name: 'assets',
                type: 'bar',
                stack: 'Ad',
                data: assets_TWD_list
            },
            {
                name: 'debt',
                type: 'bar',
                stack: 'Ad',
                data: debt_TWD_list
            },
        ]
    };

    option && myChart.setOption(option);
}
