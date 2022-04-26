$.ajax({ 
    type: 'GET',
    url:'/lazy_borad_data',
    //data:'income_data',
    //async: false,
    success: function (data) {
        endMeetsList=data.endMeets_data
        endMeetsListT=[]

        year_month_list=[]
        for (i=0;i<endMeetsList.length;i++){
            year_month_list.push(endMeetsList[i].year_month)
            }
        income_TWD_list=[]
        for (i=0;i<endMeetsList.length;i++){
            income_TWD_list.push(endMeetsList[i].income_TWD)
            }
        expend_TWD_list=[]
        for (i=0;i<endMeetsList.length;i++){
            x=-(endMeetsList[i].expend_TWD)
            expend_TWD_list.push(x)
            }
        end_meets_list=[]
        for (i=0;i<endMeetsList.length;i++){
            end_meets_list.push(endMeetsList[i].end_meets)
            }
        assets_TWD_list=[]
        for (i=0;i<endMeetsList.length;i++){
            assets_TWD_list.push(endMeetsList[i].assets_TWD)
            }
        debt_TWD_list=[]
        for (i=0;i<endMeetsList.length;i++){
            x=-(endMeetsList[i].debt_TWD)
            debt_TWD_list.push(x)
            }

        endmeetsThisMonth=end_meets_list[(end_meets_list.length)-1]
        endmeetsLastMonth=end_meets_list[(end_meets_list.length)-2]
        assetsThisMonth=assets_TWD_list[(assets_TWD_list.length)-1]
        assetsLastMonth=assets_TWD_list[(assets_TWD_list.length)-2]

        assetsDetailList=data.assets_data
        date_assetsDetailList=[]
        for (i=0;i<assetsDetailList.length;i++){
            date_assetsDetailList.push(assetsDetailList[i].date)
            }
        var thisMonth=date_assetsDetailList[(date_assetsDetailList.length)-1]
        var assetsDetailListThisMounth=[]
        for (i=0;i<assetsDetailList.length;i++) {
            if(assetsDetailList[i].date===thisMonth){
                assetsDetailListThisMounth.push(assetsDetailList[i])
            }
        }
        console.log(assetsDetailListThisMounth)
        pieAssetsData=[]
        for (i=0;i<assetsDetailListThisMounth.length;i++){
            pieAssetsData.push(assetsDetailListThisMounth[i].TWD_exchange*assetsDetailListThisMounth[i].assets_QTY)
            }
        pieAssetsLengend=[]
        for (i=0;i<assetsDetailListThisMounth.length;i++){
            pieAssetsLengend.push(assetsDetailListThisMounth[i].account)
            }
        console.log(pieAssetsData,pieAssetsLengend)
        generateChart(year_month_list,income_TWD_list,expend_TWD_list,end_meets_list)
        generateAssetsChart(year_month_list,assets_TWD_list,debt_TWD_list)
        generateIndicator(endmeetsThisMonth,endmeetsLastMonth,assetsThisMonth,assetsLastMonth)
        generatePie('assetsPie',pieAssetsData,pieAssetsLengend )
    }    
}
)