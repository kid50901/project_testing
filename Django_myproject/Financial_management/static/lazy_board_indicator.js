
function generateIndicator(endmeetsThisMonth,endmeetsLastMonth,assetsThisMonth,assetsLastMonth){
    //setting
    var titlesize=15
    var indicatorsize=30
    if (endmeetsThisMonth>0){
        indcatorColor='green'
    }
    else{
        indcatorColor='red'
    }
    data=[
        {
            title: { text: 'Endmeets',
            font: {
                //family: 'Courier New, monospace',
                size: titlesize,
                //color: 'blue'
                }},
            type: "indicator",
            mode: "number+delta",
            value: endmeetsThisMonth,
            number: { suffix: " TW" ,
            font: {
                //family: 'Courier New, monospace',
                size: indicatorsize,
                color: indcatorColor
                },},
            delta: { reference: endmeetsLastMonth,}
            },
        ]
    layout = {  
        height: 120,
        width :180,
        margin: {
            l: 5,
            r: 1,
            b: 10,
            t: 10,
        },
    };
    Plotly.newPlot('indicator', data,layout);  


    if(assetsThisMonth<assetsLastMonth){
        assetsColor='red'
    }
    else{
        assetsColor='green'
    }
    data1=[
        {
            title: { text: 'Assets',
            font: {
                //family: 'Courier New, monospace',
                size: titlesize,
                //color: 'blue'
                }},
            type: "indicator",
            mode: "number+delta",
            value: assetsThisMonth,
            number: { suffix: " TW" ,
            font: {
                //family: 'Courier New, monospace',
                size: indicatorsize,
                color: assetsColor
                },},
            delta: { reference: assetsLastMonth}
            },
        ]
    layout1 = {  
        height: 120,
        width :180,
        margin: {
            l: 5,
            r: 1,
            b: 10,
            t: 10,
        },
    };

    Plotly.newPlot('indicator1', data1,layout1);
}

//Plotly.newPlot(divinlist[0], datalist[0],layoutlist[0]); 
//Plotly.newPlot(divinlist[1], datalist[1],layoutlist[1]);
//Plotly.newPlot(divinlist[2], datalist[2],layoutlist[2]); 
//Plotly.newPlot(divinlist[3], datalist[3],layoutlist[3]);
//Plotly.newPlot(divinlist[4], datalist[4],layoutlist[4]);

//Plotly.newPlot('myDivin_1', datalist[0],layoutlist[0]); 
//Plotly.newPlot('myDivin_2', datalist[1],layoutlist[1]);
//Plotly.newPlot('myDivin_3', datalist[2],layoutlist[2]); 
//Plotly.newPlot('myDivin_4', datalist[3],layoutlist[3]);
//Plotly.newPlot('myDivin_5', datalist[4],layoutlist[4]);
