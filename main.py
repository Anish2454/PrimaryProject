#! /usr/bin/python
import cgi
import cgitb
#import plotly.plotly as py
#import plotly
#import plotly.graph_objs as go
#import plotly.tools as tools

cgitb.enable()
HTML_HEADER = 'Content-type: text/html\n\n'
Top_HTML = '''
<html>
<head>
<title>Sample Python Forms-responder</title>
</head>
<body>
'''

Bottom_HTML = "</body></html>"

def main():
    #trace = {"type": "choropleth", "locations": ["NY", "MN", "VT", "FL", "OH"], "locationmode":"USA-states",
    #"colorscale":[[0,"green"], [0.1,"blue"], [0.2, "red"], [0.3, "orange"], [1, "purple"]],
    #"z":[0.1,1,0,0.2,0.3], "hoverinfo":"location", "showscale":False}
    #lyt = {"geo": {"scope":'usa'}, "title":"Anish's Map"}
    #map = go.Figure(data = [trace], layout=lyt)
    print(HTML_HEADER)
    print(Top_HTML)
    print('<iframe width="900" height="800" frameborder="0" scrolling="no" src="https://plot.ly/~introcs2/14.embed"></iframe>')
    print(Bottom_HTML)

main()
