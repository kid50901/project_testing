function generatePie(divID,pieData,pieLengend){
  var chartDom = document.getElementById(divID);
  var myChart = echarts.init(chartDom);
  var option;
  var dataList=[]
  console.log(pieData,pieLengend)
  for (var i = 0;i<pieData.length;i++) {
    dataList.push({ value: pieData[i], name: pieLengend[i] })
  }
  console.log(dataList)
  option = {

    tooltip: {
      trigger: 'item'
    },
  
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '50%',
        data: dataList,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  option && myChart.setOption(option);

}
