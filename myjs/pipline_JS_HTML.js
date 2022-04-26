document.getElementById('countId').onclick = function(){
    //用變數設定漢堡跟可樂的售價
    var hamPrice = 80;
    var cokePrice = 20;
    //選取輸入欄位的 DOM 並宣告變數名，用 value 帶出輸入欄的值。
    var hamNum = parseInt(document.getElementById('hamNumId').value);
    var cokeNum = parseInt(document.getElementById('cokeNumId').value);
    //再用一個變數儲存金額加總
    var total = hamNum*hamPrice + cokeNum*cokePrice;
    //把總金額渲染至網頁上
    document.getElementById('totalId').textContent = total;
  }