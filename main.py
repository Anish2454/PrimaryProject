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
</head>
<body>
<div id="chart-div" height="100%" width="100%"></div>
<div id="chart-div-2"></div>
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
    colorscale: [[0,"green"], [1,"blue"]],
    showscale: false,
    hoverinfo: "location",
    z: ''' + convertListToJs(locationsValues[1]) + '''
    }];
    var layout = {
    title: "Anish's Map",
    autosize: false,
    width: window.innerWidth,
    height: window.innerHeight,
    geo: {
      scope: "usa",
      showlakes: true,
      lakecolor: 'cyan'
    }
    };
    Plotly.plot(chartDiv, data, layout);

    chartDiv.on("plotly_click", function(data){
    window.open("main.py?state=" + data.points[0].location);
    });
    '''
    print("<script>")
    print(js)
    print("</script>")

def displayStatePage(state, masterDict):
    if state in masterDict:
        stateInfo = masterDict[state]
    if "Bernie Delegates" in stateInfo and "Clinton Delegates" in stateInfo:
        xBernie = [stateInfo["Bernie Delegates"]]
        xClinton = [stateInfo["Clinton Delegates"]]
    else:
        xBernie = 0
        xClinton = 0
    js = '''
    var trace1 = {
        x: ''' + convertListToJs(xBernie) + "," + '''
        y: ["Sanders"],
        name: "Bernie Sanders",
        orientation: 'h',
        type: 'bar',
        marker: {
            color: 'rgba(55,128,191,0.6)',
            width: 1
        }
    };

    var trace2 = {
        x: ''' + convertListToJs(xClinton) +',' + '''
        y: ["Clinton"],
        name: 'Hillary Cinton',
        orientation: 'h',
        type: 'bar',
        marker: {
            color: "Blue",
            width: 1
        }
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'The ''' + states[state] + ''' Delegate Count',
        width: (window.innerWidth / 2),
        height: (window.innerHeight / 2),
        font: {
            family: 'Arial',
            size: 24,
            color: "Black"
        }
    };

    Plotly.newPlot('chart-div', data, layout);
    '''
    print("<script>")
    print(js)
    print("</script")

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
