// Global variables for rendering chart
var date = "00010101";
var selectedValue = "";
var baseURL = "https://yusy-assignment.herokuapp.com";

// Function gets executed when we select the comparison value from select box
changeFunc = () => {
  let selectBox = document.getElementById("selectBox");
  let selected = selectBox.options[selectBox.selectedIndex].value;
  selectedValue = selected;
  displayChart();
};

// Function to get the range value
getRange = range => {
  switch (range) {
    case "1M":
      date = "20190918";
      break;
    case "6M":
      date = "20190318";
      break;
    case "Y2D":
      date = "20190101";
      break;
    case "1Y":
      date = "20180918";
      break;
    case "5Y":
      date = "20150918";
      break;
    default:
      date = "00010101";
  }
  t = document.getElementsByClassName("selected-range");
  for (let i = 0; i < t.length; i++) {
    t[i].className = "";
  }
  document.getElementById(range).className = "selected-range";
  displayChart();
};

// main function that displays the chart in canvas based on global values
displayChart = async () => {
  if (selectedValue == "60S40B") {
    var url2 = `${baseURL}/getStockBond?stockdate=${date}&stock=60&bond=40`;
  } else if (selectedValue == "20S80B") {
    var url2 = `${baseURL}/getStockBond?stockdate=${date}&stock=20&bond=80`;
  }

  url1 = `${baseURL}/getNetPrice?stockdate=${date}`;

  let response = await fetch(url1);
  let data = await response.json();
  dp1 = data;

  response = await fetch(url2);
  data = await response.json();
  dp2 = data;

  var title = "StashAway 14%   Vs  " + dp2["title"];

  let chart = new CanvasJS.Chart("chartContainer", {
    zoomEnabled: true,
    animationEnabled: true,
    toolTip: {
      shared: true,
      contentFormatter: function(e) {
        var content = " ";
        for (var i = 0; i < e.entries.length; i++) {
          content +=
            e.entries[i].dataSeries.name +
            "<br>" +
            "<strong>" +
            "$" +
            e.entries[i].dataPoint.y +
            "</strong>";
          content += "<br/>";
        }
        return content;
      }
    },
    axisX: {
      valueFormatString: "DD MMM YY"
    },
    axisY: {
      includeZero: false
    },
    data: [
      {
        type: "line",
        name: "StashAway 14%",
        showInLegend: true,
        legendText: dp1["title"],
        xValueType: "dateTime",
        dataPoints: dp1["data"]
      },
      {
        type: "line",
        name: dp2["title"],
        showInLegend: true,
        legendText: dp2["title"],
        xValueType: "dateTime",
        dataPoints: dp2["data"]
      }
    ]
  });

  chart.render();
};
