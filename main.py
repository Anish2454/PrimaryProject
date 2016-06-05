#! /usr/bin/python
import cgi
import cgitb
import json

cgitb.enable()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

HTML_HEADER = 'Content-type: text/html\n\n'

Top_HTML = '''
<html>
<head>
<title>Sample Python Forms-responder</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<link href='https://fonts.googleapis.com/css?family=Playfair+Display' rel='stylesheet' type='text/css'>
</head>
<body>
<style>
.nav{
	border:1px solid #ccc;
    border-width:1px 0;
    list-style:none;
    margin:0;
    padding:0;
    text-align:center;
}
.nav li{
    display:inline;
}
.nav a{
    display:inline-block;
    padding:10px;
    color: #008FD5;
    text-decoration: none;
    font-size: 17px;
    line-height: 26px;
    font-family: AtlasGrotesk, 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.nav a:hover {
  font-size: 30px;
  }

</style>
<ul class = "nav">
  <li><a href="http://marge.stuy.edu/~anish.shenoy/Final_Project/main.py">Home</a></li>
  <li><a href="https://www.washingtonpost.com/graphics/politics/2016-election/primaries/schedule/">Primary Dates</a></li>
  <li><a href="https://votesmart.org/education/presidential-primary#.V1NTW7grKUk">Information on Primaries</a></li>

</ul>
'''

Bottom_HTML = "</body></html>"

def convertListToJs(list):
    finalString = "["
    for i in list:
        finalString += "'" + str(i) + "', "
    finalString += "]"
    return finalString

def openFile(filename):
    f = open(filename, "rU")
    s = f.read()
    f.close()
    return s

def organize():
    s = openFile("demdata.csv")
    stateByState = s.split("\n")
    lst = [i.split(",") for i in stateByState]
    keys = lst[0]
    mD = {}
    for i in lst[1:-1]:
       d = {}
       for n in range(len(keys)):
           if n < len(i):
               d[keys[n]] = i[n]
           else:
               d[keys[n]] = ""
       if d["Bernie Delegates"] != "" and d["Clinton Delegates"] != "":
           if max(int(d["Bernie Delegates"]), int(d["Clinton Delegates"])) == int(d["Bernie Delegates"]):
               d["Winner"] = "Bernie"
           else:
               d["Winner"] = "Clinton"
       else:
           d["Winner"] = "None"
       if i[0] in us_state_abbrev:
           mD[us_state_abbrev.get(i[0], "")] = d
       else:
           mD[i[0]] = d

    return mD

def locationsAndValues(masterDict):
    winnerDict = {"Bernie":0, "Clinton":1, "None":0.5}
    locations =[]
    values = []
    for i in masterDict:
        if len(i) == 2:
            if "Winner" in masterDict[i]:
                locations.append(i)
                values.append(winnerDict[masterDict[i]["Winner"]])
    return [locations, values]

def displayMap(masterDict):
    locationsValues = locationsAndValues(masterDict)
    js = '''
    var chartDiv = document.getElementById('chart-div');
    var data = [{
    type: "choropleth",
    locations: ''' + convertListToJs(locationsValues[0]) + "," + '''
    locationmode: "USA-states",
    colorscale: [[0,"rgb(102, 187, 106)"], [1,"rgb(21, 101, 192)"]],
    showscale: false,
    hoverinfo: "location",
    z: ''' + convertListToJs(locationsValues[1]) + ''',
    marker: {
    line: {
    width: 2,
    color: "white"
    }
    }
    }];
    var layout = {
    autosize: false,
    width: window.innerWidth,
    height: window.innerHeight - 100,
    geo: {
      scope: "usa",
      showlakes: true,
      lakecolor: 'cyan'
    },
    font: {
       family: 'Playfair Display, serif',
       size: 24,
       color: "Black",
       bold: true
       }
    };
    Plotly.plot(chartDiv, data, layout);

    chartDiv.on("plotly_click", function(data){
    window.open("main.py?state=" + data.points[0].location);
    });
    '''
    print('<div id="page">')
    print('<center><div id="header"><h1> <font size=10>2016 Democratic Primaries</font></h1><p>With the upcoming elections predicted to be one of the most influential elections in history, it is imperative that we have some of the most informed voters in history. This map is updated daily with results from the democratic primaries; click on a state for more information about the results from that state.</p></div></center>')
    style = '''
    <style>
    #header {
        position: relative;
    }
    </style>
    '''
    print('<center><div id="chart-div"></div></center>')
    print('</div>')
    print(style)
    print("<script>")
    print(js)
    print("</script>")

def plotDelgateGraph(bernieDel, clintonDel, state, divName):
    js = '''
    var trace1 = {
        x: ''' + convertListToJs([bernieDel]) + "," + '''
        y: ["Sanders"],
        name: "Bernie Sanders",
        orientation: 'h',
        type: 'bar',
        marker: {
            color: 'rgba(102, 187, 106, .5)',
            width: 1
        }
    };

    var trace2 = {
        x: ''' + convertListToJs([clintonDel]) +',' + '''
        y: ["Clinton"],
        name: 'Hillary Cinton',
        orientation: 'h',
        type: 'bar',
        marker: {
            color: "rgba(21, 101, 192, 0.5)",
            width: 1
        }
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'The ''' + states[state] + ''' Delegate Count',
        width: 1024,
        height: 350,
        font: {
           family: 'Playfair Display, serif',
           size: 20,
           color: 666
           }
    };

    Plotly.newPlot("''' + divName + '''", data, layout);
    '''
    return js

def plotDelgatePie(bernieDel, clintonDel, state, divName):
    values = [bernieDel, clintonDel]
    js = '''
    var data = [{
      values: ''' + convertListToJs(values) + ',' + '''
      labels: ['Bernie Sanders', 'Hillary Clinton'],
      type: 'pie',
      marker :{
        colors: ['rgba(102, 187, 106, .5)', 'rgba(21, 101, 192, 0.5)']
        }
    }];

    var layout = {
     title: 'The ''' + states[state] + ''' Delegate Count by %',
     height: 400,
     width: 1000,
     font: {
        family: 'Playfair Display, serif',
        size: 20,
        color: "Black"
        },
    autoexpand: false
    };
    Plotly.newPlot(''' + "'" + divName + "'" + ''', data, layout);
    '''
    return js

def plotVoteGraph(bernieVotes, clintonVotes, state, divName):
    js = '''
    var trace1 = {
        x: ''' + convertListToJs([bernieVotes]) + "," + '''
        y: ["Sanders"],
        name: "Bernie Sanders",
        orientation: 'h',
        type: 'bar',
        marker: {
            color: 'rgba(102, 187, 106, .5)',
            width: 1
        }
    };

    var trace2 = {
        x: ''' + convertListToJs([clintonVotes]) +',' + '''
        y: ["Clinton"],
        name: 'Hillary Cinton',
        orientation: 'h',
        type: 'bar',
        marker: {
            color: "rgba(21, 101, 192, 0.5)",
            width: 1
        }
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'The ''' + states[state] + ''' Popular Vote',
        width: 1024,
        height: 350,
        font: {
           family: 'Playfair Display, serif',
           size: 20,
           color: 666
           }
    };

    Plotly.newPlot("''' + divName + '''", data, layout);
    '''
    return js

def plotVotePieChart(bernieVotes, clintonVotes, state, divName):
    values = [bernieVotes, clintonVotes]
    js = '''
    var data = [{
      values: ''' + convertListToJs(values) + ',' + '''
      labels: ['Bernie Sanders', 'Hillary Clinton'],
      type: 'pie',
      marker :{
        colors: ['rgba(102, 187, 106, .5)', 'rgba(21, 101, 192, 0.5)']
        }
    }];

    var layout = {
     title: 'The ''' + states[state] + ''' Popular Vote by %',
     height: 400,
     width: 1000,
     font: {
        family: 'Playfair Display, serif',
        size: 20,
        color: "Black"
        },
    autoexpand: false
    };
    Plotly.newPlot(''' + "'" + divName + "'" + ''', data, layout);
    '''
    return js

def stateNotVoted(state):
    print(states[state]  + " Has Not Voted Yet")

def displayStatePage(state, masterDict):
    print('<center><div id="delegate-div">')
    print('<div id="delegate-horiz"></div>')
    print('<div id="delegate-pie"></div>')
    print('</div></center>')
    print('<center><div id="pop-div">')
    print('<div id="pop-horiz"></div>')
    print('<div id="pop-pie"></div>')
    print('</div></center>')
    style = '''
    <style>
    #delegate-pie, #delegate-horiz, #pop-pie, #pop-horiz {
        display: inline-block;
    }
    </style>
    '''
    print(style)
    if state in masterDict:
        stateInfo = masterDict[state]
    if stateInfo["Bernie Delegates"] != "" and stateInfo["Clinton Delegates"] != "":
        bernieDel = int(stateInfo["Bernie Delegates"])
        clintonDel = int(stateInfo["Clinton Delegates"])
        print("<script>")
        print(plotDelgateGraph(bernieDel, clintonDel, state, "delegate-horiz"))
        print(plotDelgatePie(bernieDel, clintonDel, state, "delegate-pie"))
        print("</script>")
    else:
        stateNotVoted(state)
    if stateInfo["Bernie Votes"] != "" and stateInfo["Clinton Votes"] != "":
        bernieVotes = int(stateInfo["Bernie Votes"])
        clintonVotes = int(stateInfo["Clinton Votes"])
        print("<script>")
        print(plotVoteGraph(bernieVotes, clintonVotes, state, "pop-horiz"))
        print(plotVotePieChart(bernieVotes, clintonVotes, state, "pop-pie"))
        print("</script>")

def main():
    masterDict = organize()
    print(HTML_HEADER)
    print(Top_HTML)
    elements = cgi.FieldStorage()
    keys = elements.keys()
    if "state" in keys:
        displayStatePage(str(elements.getvalue("state")), masterDict)
    else:
        displayMap(masterDict)
    print(Bottom_HTML)

main()
