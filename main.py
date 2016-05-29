#! /usr/bin/python
import cgi
import cgitb
import json

cgitb.enable()

def convertListToJs(list):
    finalString = "["
    for i in list:
        finalString += "'" + str(i) + "', "
    finalString += "]"
    return finalString

locations = ["NY", "MN", "VT", "FL", "OH", "CA"]
values = [1,0,0,1,1,0]

HTML_HEADER = 'Content-type: text/html\n\n'
Top_HTML = '''
<html>
<head>
<title>Sample Python Forms-responder</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
<div id="chart-div" height="100%" width="100%"></div>
<script>
'''

Bottom_HTML = "</script></body></html>"

js = '''
var chartDiv = document.getElementById('chart-div');
var data = [{
    type: "choropleth",
    locations: ''' + convertListToJs(locations) + "," + '''
    locationmode: "USA-states",
    colorscale: [[0,"green"], [1,"blue"]],
    showscale: false,
    hoverinfo: "location",
    z: ''' + convertListToJs(values) + '''
  }];
  var layout = {
    title: "Anish's Map",
    autosize: false,
    width: window.innerWidth,
    height: window.innerHeight,
    geo: {
      scope: "usa"
    }
  };
  Plotly.plot(chartDiv, data, layout);

  chartDiv.on("plotly_click", function(data){
    window.open("http://bert.stuy.edu/pbrooks/ml2/SampleQuestionsAnswers.py?CheckArithmetic=ON&FirstNum=5&Operator=%2F&SecondNum=12&CheckString=ON&TheString=%22Anish%22&RadioString=Lower&TheSubmitButton=Get+the+answers");
  });
'''


def main():
    print(HTML_HEADER)
    print(Top_HTML)
    print(js)
    print(Bottom_HTML)

main()
