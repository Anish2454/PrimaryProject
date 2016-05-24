import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import plotly.tools as tools

trace = {"type": "choropleth", "locations": ["NY", "MN", "VT", "FL", "OH", "CA"], "locationmode":"USA-states",
"colorscale":[[0,"green"], [0.1,"blue"], [0.2, "red"], [0.3, "orange"], [1, "purple"]],
"z":[0.1,1,0,0.2,0.3,0], "hoverinfo":"location", "showscale":False}
lyt = {"geo": {"scope":'usa'}, "title":"Anish's Map"}
map = go.Figure(data = [trace], layout=lyt)
py.plot(map, filename="my plot")
