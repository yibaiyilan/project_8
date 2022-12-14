import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import plotly as py
import plotly.express as px

# from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

########### Define your variables ######

tabtitle = 'Bachelor Degree'
sourceurl = 'https://www.kaggle.com/datasets/tjkyner/bachelor-degree-majors-by-age-sex-and-state'
githublink = 'https://github.com/yibaiyilan/project_8.git'
# here's the list of possible columns to choose from.
list_of_columns =['Bachelor\'s Degree Holders','Science and Engineering','Science and Engineering Related Fields','Business','Education','Arts, Humanities and Others']


########## Set up the chart

df = pd.read_csv('Bachelor_Degree_Majors.csv',encoding='latin1',on_bad_lines='skip')

########## US States to Code
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
df['Code'] = df['State'].map(us_state_to_abbrev)
df=df[df['Age Group']!='25 and older']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2019 Female Rate for Bachelor Degree, by State'),
    html.Div([
        html.Div([
                html.H6('Select a major for analysis:'),
                dcc.Dropdown(
                    id='options-drop1',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='Science and Engineering'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='five columns'),
        html.Div([dcc.Graph(id='figure-2'),
            ], className='five columns'),
    ], className='twelve columns'),
    html.Div([
        html.Div([
                html.H6('Select a major for analysis:'),
                dcc.Dropdown(
                    id='options-drop2',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='Arts, Humanities and Others'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-3'),
            ], className='five columns'),
        html.Div([dcc.Graph(id='figure-4'),
            ], className='five columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.

def make_figure(varname):
    mycolorbartitle = "Bachelor Degree Holders"
    mygraphtitle = f'Female Rate for Bachelor Degree of {varname} in 2019'
    mycolorscale = 'Sunset' # Note: The error message will list possible color scales.
    
    major = pd.DataFrame(df,columns = ['Code','Sex',varname])
    major[varname] = major[varname].replace(",","", regex=True).astype(float)
    total = major[major['Sex']=='Total'].groupby(['Code'],as_index = False).sum().rename(columns={varname:"Total"})
    female = major[major['Sex']=='Female'].groupby(['Code'],as_index = False).sum().rename(columns={varname:"Female"})
    male = major[major['Sex']=='Female'].groupby(['Code'],as_index = False).sum().rename(columns={varname:"Male"})
    female_rate = pd.DataFrame()
    female_rate['Code']  = df['State'].map(us_state_to_abbrev)
    female_rate = pd.merge(female,male,on=['Code']).merge(total,on=['Code'])
    female_rate['Female Rate'] = female_rate['Female']/female_rate['Total']

    data1=go.Choropleth(
        locations=female_rate['Code'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = female_rate['Female Rate'].astype(float), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig1 = go.Figure(data1)
    fig1.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=500
    )
    
    data2 = df[['Code','Sex',varname]]
    data2[varname] = data2[varname].replace(",","", regex=True).astype(float)
    data2 = data2[data2['Sex']!='Total'].groupby(['Code','Sex'],as_index = False).sum()
    color_discrete_sequence = ['#009ACD','#FFB6C1']
    fig2 = px.bar(data2, x="Code", y=varname, 
                 color="Sex", barmode="group",color_discrete_sequence=color_discrete_sequence)
    fig2.update_layout(
        width=1200,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig1,fig2

@app.callback(Output('figure-1', 'figure'),
             Output('figure-2', 'figure'),
             Input('options-drop1', 'value'))

def figure_callback1(varname):
    return make_figure(varname)

@app.callback(Output('figure-3', 'figure'),
             Output('figure-4', 'figure'),
             Input('options-drop2', 'value'))

def figure_callback2(varname):
    return make_figure(varname)

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
