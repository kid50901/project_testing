var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

var updateFrequency = 4000;
var dimension = 0;

var countryColors = {"Colombia":"#00008b",
"United States":"#f00",
"China":"#ffde00",
"European Union":"#002a8f",
"Brazil":"#003580",
"France":"#ed2939",
"Turkey":"#000",
"United Kingdom":"#003897",
"India":"#f93",
"Japan":"#bc002d",
"Thailand":"#024fa2",
"Indonesia":"#000",
"Mexico":"#00247d",
"Argentina":"#ef2b2d",
"Peru":"#dc143c",
"Russia":"#d52b1e",
"Spain":"#e30a17",
"Italy":"#00247d",
"Germany":"#b22234"};
var countryColors_srt = {"哥倫比亞":"#00008b",
"美國":"#f00",
"中國":"#ffde00",
"歐盟":"#002a8f",
"巴西":"#003580",
"法國":"#ed2939",
"土耳其":"#000",
"英國":"#003897",
"印度":"#f93",
"日本":"#bc002d",
"泰國":"#024fa2",
"印尼":"#000",
"墨西哥":"#00247d",
"阿根廷":"#ef2b2d",
"秘魯":"#dc143c",
"俄羅斯":"#d52b1e",
"西班牙":"#e30a17",
"義大利":"#00247d",
"德國":"#b22234"};
$.when(
    $.getJSON('http://localhost:3000/data')
).done(function (result) {
    var data = [];
    console.log(result)
    for(var i=0;i<result.length;i++){
        data.push(Object.values(result[i]))
    }
    console.log(data)
    
    var timelist = [];
    for (var i = 0; i < result.length; ++i) {
       timelist.push(result[i].time)
    }
    console.log(timelist)

    function getFlag(countryName) {
        if (!countryName) {
            return '';
        }
        return (flags.find(function (item) {
            return item.name === countryName;
        }) || {}).emoji;
    }
    var startIndex = 0;
    var startYear = timelist[startIndex];
    var test=data.slice(1).filter(function (d) {
        return d[4] === startYear;
    })
    console.log(test)
    var option = {
        title: {
            text: 'Covid-19 月新增病例國家排名',
            subtext: 'source:https://covid.ourworldindata.org/data/owid-covid-data.csv'
        },
        
        xAxis: {
            max: 'dataMax',
            label: {
                formatter: function (n) {
                    return Math.round(n);
                }
            }
        },
        dataset: {
            source: data.slice(1).filter(function (d) {
                return d[4] === startYear;
            })
        },
        yAxis: {
            type: 'category',
            inverse: true,
            max: 10,
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 14
                },
                //formatter: function (value) {
                    //console.log('x',value + '{flag|' + getFlag(value) + '}')
                    //return value;
                //},
                rich: {
                    flag: {
                        fontSize: 25,
                        padding: 5
                    }
                }
            },
            animationDuration: 300,
            animationDurationUpdate: 300
        },
        series: [{
            realtimeSort: true,
            seriesLayoutBy: 'column',
            type: 'bar',
            itemStyle: {
                color: function (param) {
                    //console.log('param',param)
                    //console.log('value[3]',value[3])
                    return countryColors_srt[param.value[3]] || '#5470c6';
                }
            },
            encode: {
                x: dimension,
                y: 3
            },
            label: {
                show: true,
                precision: 1,
                position: 'right',
                valueAnimation: true,
                fontFamily: 'monospace'
            }
        }],
        // Disable init animation.
        animationDuration: 0,
        animationDurationUpdate: updateFrequency,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear',
        graphic: {
            elements: [{
                type: 'text',
                right: 160,
                bottom: 60,
                style: {
                    text: startYear,
                    font: 'bolder 80px monospace',
                    fill: 'rgba(100, 100, 100, 0.25)'
                },
                z: 100
            }]
        }
    };
    // console.log(option);
    myChart.setOption(option);

    for (var i = startIndex; i < timelist.length - 1; ++i) {
        (function (i) {
            setTimeout(function () {
                updateYear(timelist[i + 1]);
            }, (i - startIndex) * updateFrequency);
        })(i);
    }
    console.log(data)
    function updateYear(year) {
        var source = data.slice(1).filter(function (d) {
            return d[4] === year;
        });
        option.series[0].data = source;
        option.graphic.elements[0].style.text = year;
        myChart.setOption(option);
    }
})

option && myChart.setOption(option);