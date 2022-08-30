import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import plotly as py

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
                    value='Bachelor\'s Degree Holders'
                ),
                dcc.Dropdown(
                    id='options-drop2',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='Bachelor\'s Degree Holders'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='five columns'),
        html.Div([dcc.Graph(id='figure-2'),
            ], className='five columns'),
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
@app.callback(Output('figure-1', 'figure'),
             Output('figure-2', 'figure'),
             Output('figure-3', 'figure'),
             Output('figure-4', 'figure'),
             Input('options-drop1', 'value'),
             Input('options-drop2', 'value'))
def make_figure(varname1,varname2):
    mycolorbartitle = "Bachelor Degree Holders"
    mygraphtitle = f'Female Rate for Bachelor Degree of {varname1} in 2019'
    mycolorscale = 'Sunset' # Note: The error message will list possible color scales.
    
    se = pd.DataFrame(df,columns = ['Code','Sex',varname1])
    se[varname1] = se[varname1].replace(",","", regex=True).astype(float)
    total_se = se[se['Sex']=='Total'].groupby(['Code'],as_index = False).sum().rename(columns={varname1:"Total"})
    female_se = se[se['Sex']=='Female'].groupby(['Code'],as_index = False).sum().rename(columns={varname1:"Female"})
    female_rate_se = pd.DataFrame()
    female_rate_se['Code']  = df['State'].map(us_state_to_abbrev)
    female_rate_se = pd.merge(female_se,total_se,on=['Code'])
    female_rate_se['Female Rate'] = female_rate_se['Female']/female_rate_se['Total']

    data=go.Choropleth(
        locations=female_rate_se['Code'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = female_rate_se['Female Rate'].astype(float), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig1 = go.Figure(data)
    fig1.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    
    fig1=fig
    fig2=fig
    fig3=fig
    fig4=fig
    return fig1,fig2,fig3,fig4



############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
