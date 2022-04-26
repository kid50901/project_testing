function getMystationset(selectdataset){
    var stationlist=[]
    var stationset=[]

    ///取出stationlist
    for(var i=0;i<selectdataset.length;i++){
        stationlist.push(selectdataset[i].prcess_name)
    }
    stationlist = [...new Set(stationlist)]
    console.log('stationlist',stationlist)

    ///依站點分割資料，放入stationset
    var stationset=[]
    for (var i=0;i<stationlist.length;i++){
        stationset[i]=selectdataset.filter(function(x){
            return x.prcess_name === stationlist[i]
        })
    }
    console.log('stationset',stationset)
    return [stationlist,stationset]
}
function getMychartdata(stationset_element){
    console.log(Object.values(stationset_element[0]))
    var chartdata=[]
    var chartdataT=[]
    for(var i=0;i<stationset_element.length;i++){
        chartdata.push(Object.values(stationset_element[i]))
    }
    console.log('chartdata',chartdata)
    ///轉置
    chartdataT = chartdata[0].map(function(col, i) {
        return chartdata.map(function(row) {
        return row[i];
        })
    });
    console.log('chartdataT',chartdataT)
    return chartdataT
}
function definechart(mychartdataTList,mystationlist,uphtarget,yieldtarget){
    ////畫圖
    var input_line_list=[]
    var output_line_list=[]
    var fpy_line_list=[]
    var lpy_line_list=[]
    var data=[]
    var timelist=mychartdataTList[0][8]

    //////定義uph input 線
    for (var i=0;i<mychartdataTList.length;i++){
        input_line_list[i] = {
        type: "scatter",
        mode: "lines",
        name: `INPUT ${mystationlist[i]}`,
        x: timelist,//timelsit
        y: mychartdataTList[i][11],
        //visible: false,
        }
        data.push(input_line_list[i])
    }
    //////定義uph output線
    for (var i=0;i<mychartdataTList.length;i++){
        output_line_list[i] = {
        type: "scatter",
        mode: "lines",
        name: `OUTPUT ${mystationlist[i]}`,
        x: timelist,//timelsit
        y: mychartdataTList[i][12],
        //visible: false,
        }
        data.push(output_line_list[i])
    }
    for (var i=0;i<mychartdataTList.length;i++){
        fpy_line_list[i] = {
        type: "scatter",
        mode: "lines",
        name: `FPY ${mystationlist[i]}`,
        x: timelist,//timelsit
        y: mychartdataTList[i][1],
        yaxis: 'y2',
        //visible: false,
        }
        data.push(fpy_line_list[i])
    }
    for (var i=0;i<mychartdataTList.length;i++){
        lpy_line_list[i] = {
        type: "scatter",
        mode: "lines",
        name: `LPY ${mystationlist[i]}`,
        x: timelist,//timelsit
        y: mychartdataTList[i][2],
        yaxis: 'y2',
        //visible: false,
        }
        data.push(lpy_line_list[i])
    }
    var makeUPHtarget=[]
    for (i=0;i<timelist.length;i++){
        makeUPHtarget.push(uphtarget)
    }
    var UPH_Target = {
        type: "scatter",
        mode: "lines",
        name: 'UPH_Target',
        x: timelist,
        y: makeUPHtarget,
        line: {color: '#FF0000',
                width:1,
                dash: 'dashdot' },
        
        //visible: false,
        //yaxis: 'y2'
        }
    var makeYtarget=[]
    for (i=0;i<timelist.length;i++){
        makeYtarget.push(yieldtarget)
    }
    var FPY_Target = {
        type: "scatter",
        mode: "lines",
        name: 'Yield_Target',
        //fill: 'tozeroy',
        x: timelist,
        y: makeYtarget,
        yaxis: 'y2',
        line: {color: '#FF0000',
                width:1 ,
                dash: 'dashdot'},
        }
    data.push(UPH_Target)
    data.push(FPY_Target)
    return data
    console.log('data',data)
}
function definelayout(mychartdataTList){
    var timelist=mychartdataTList[0][8]
    var hourlist=[]
    var hourliststr=[]
    //////定義時間軸
    for (let j = 0; j < 25 ; j++) {
        hourlist.push(timelist[j*6])
    }
    for (let k = 0; k < 25 ; k++) {
        T=(k+8)%24;
        hourliststr.push(`${T}`)
    }
    var layout = {

        plot_bgcolor: "#F3F3FA",
        legend: {
            //bgcolor: 'white',
            //borderwidth: 1,
            //bordercolor: 'black',
            title:{
                'side' : 'left'
            },
            orientation: 'h',
            //xanchor: 'left',
            //x: 0.5,
            font: {
              size: 8,
            }
          },
        xaxis: {
            showline: true,
            showgrid: true,
            gridcolor:'white',
            linecolor: 'rgb(204,204,204)',
            linewidth: 2,
            
            tickvals : hourlist,
            ticktext : hourliststr,
            ticks: 'outside',
            tickcolor: 'rgb(204,204,204)',
            tickwidth: 2,
            ticklen: 5,
            tickfont: {
              family: 'Arial',
              size: 12,
              color: 'rgb(82, 82, 82)'
            },
          //autorange: true,
          //tickmode: "auto",
          rangemode: 'tozero',
          //showgrid: false,
          zeroline: false,
          //showline: false,
          //range: [timelist[0], timelist[143]],
          //rangeslider: {range: [timelist[0], timelist[143]]},
          
          
          type: 'category',
        },
        yaxis: {
          showline: true,
          rangemode: 'nonnegative',
          showgrid: true,
          gridcolor:'white',
          autorange: true,
          //range: [0,50],
          type: 'linear',
          //overlaying: 'y2'
          title: {
            text: 'UPH(qty)',
            font: {
              family: 'Courier New, monospace',
              size: 18,
              color: '#7f7f7f'
            }
          }
        },
        yaxis2: {
          showline: true,
          showgrid: true,
          gridcolor:'white',
          rangemode: 'nonnegative',
          autorange: true,
          title: {
            text: 'Yield(%)',
            font: {
              family: 'Courier New, monospace',
              size: 18,
              color: '#7f7f7f'
            }
          }
          //range: [0,250],
          //overlaying: 'y',
          //side: 'right'
        },
        grid: {
          rows: 2,
          columns: 1,
          subplots:['xy','xy2'],
          roworder:'bottom to top'
        },
        updatemenus: [
            {
            y: 1.15,
            x: 0.21,
            //xanchor: 'center',
            buttons: [
                {
                    method: 'restyle',
                    args: ['visible', [false,//input_Audio
                        true,//input_OT,
                        true,//input_AL_systom
                        true,//input_Cam,
                        true,//input_ACOS,
                        true,//input_Total,
                        true,//output_Audio
                        
                        ]],
                    label: 'FATP-RING-LED'
                    },
                ]
            }
        ]
       
        
    };
    return layout
}
ajaxfn=$.ajax({ 
    type: 'GET',
    url: 'http://localhost:3000/data', 
    success: function (result) {
        console.log(Object.keys(result[0]))
        var x = getMystationset(result)//依站點切割資料集
        var mystationlist=x[0]
        var mystationset=x[1]
        var mychartdataTList= []//轉置資料集為chart可用資料
        for (var i=0;i<mystationset.length;i++){
            mychartdataTList[i]=getMychartdata(mystationset[i])
        }
        console.log('mychartdataTList',mychartdataTList)
        
        var mydata=definechart(mychartdataTList,mystationlist,220,96)//定義圖表數據
        var mylayout=definelayout(mychartdataTList)//定義圖表呈現
        var config = {responsive: true}//響應式
        Plotly.newPlot('myDiv', mydata, mylayout,config);//生成圖表
    }
})

document.getElementById('countId').onclick = function(){
    projectname = document.getElementById('projectname').value;
    linename = document.getElementById('linename').value;
    ajaxfn
}

