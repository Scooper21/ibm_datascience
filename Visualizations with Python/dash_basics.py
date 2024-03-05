# Import required packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights') 

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Airline Dashboard', 
                                        style={'textAlign': 'center', 
                                               'color': '#503D36', 
                                               'font-size': 40}
                                        ), 
                                        html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010'),],
                                        style={}),
                                        html.Br(), 
                                        html.Br(),
                                        html.Div(dcc.Graph(id='line-plot')),
                                        #html.P('Proportion of distance group (250 mile distance interval group) by flights.', style={'textAlign':'center', 'color': '#F57241'}), 
                                        #dcc.Graph(figure=fig),
                                ]
                        )
@app.callback(Output(component_id='line-plot', component_property='figure'),
              Input(component_id='input-year', component_property='value'))

def get_graph(entered_year): 
    df = airline_data[airline_data['Year']==int(entered_year)]

    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title="Month vs Average Flight Delay Time", xaxis_title="Month", yaxis_title="ArrDelay")
    return fig

if __name__ == '__main__': 
    app.run_server()