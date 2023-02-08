# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'site1'},
                    {'label': 'VAFB SLC-4E' ,'value': 'site2'},
                    {'label':'KSC LC-39A' ,'value':'site3'},
                    {'label':'CCAFS SLC-40' , 'value':'site4'}
                ], value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                ), 
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100',
                       1500: '1500',
                       2500:'2500',
                       5000:'5000',
                       7500:'7500',
                       10000:'10000'},
                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart' , component_property='figure'),
            Input(component_id='site-dropdown' , component_property='value'))
def show(selected):
    if  str(selected)=='ALL':
        df=spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig=px.pie(df, values='class' , names='Launch Site')
        return fig
    else:
        if str(selected)=='site1':
            dfi=spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']['class'].value_counts().reset_index()
            dfi.columns=['cl' , 'val']
            fig=px.pie(dfi, values='val' , names='cl')
            return fig
        if str(selected)=='site2':
            dfi=spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']['class'].value_counts().reset_index()
            dfi.columns=['cl' , 'val']
            fig=px.pie(dfi, values='val' , names='cl')
            return fig
        if str(selected)=='site3':
            dfi=spacex_df[spacex_df['Launch Site']=='KSC LC-39A']['class'].value_counts().reset_index()
            dfi.columns=['cl' , 'val']
            fig=px.pie(dfi, values='val' , names='cl')
            return fig
        if str(selected)=='site4':
            dfi=spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']['class'].value_counts().reset_index()
            dfi.columns=['cl' , 'val']
            fig=px.pie(dfi, values='val' , names='cl')
            return fig


            
            

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart' ,component_property='figure'),
[Input(component_id='site-dropdown' ,component_property='value') , Input(component_id='payload-slider' , component_property='value')])
def call(site,payload):
    if str(site)=='ALL':
        dfi=spacex_df[(spacex_df['Payload Mass (kg)']>min_payload) & (spacex_df['Payload Mass (kg)']<max_payload)]
        fig=px.scatter(dfi,x='Payload Mass (kg)',y='class' , color='Booster Version Category')
        return fig
    else:
        if str(site)=='site1':
            dfi=spacex_df[(spacex_df['Payload Mass (kg)']>min_payload) & (spacex_df['Payload Mass (kg)']<max_payload) & (spacex_df['Launch Site']=='CCAFS LC-40')]
            fig=px.scatter(dfi,x='Payload Mass (kg)',y='class' , color='Booster Version Category')
            return fig
        if str(site)=='site2':
            dfi=spacex_df[(spacex_df['Payload Mass (kg)']>min_payload) & (spacex_df['Payload Mass (kg)']<max_payload) & (spacex_df['Launch Site']=='VAFB SLC-4E')]
            fig=px.scatter(dfi,x='Payload Mass (kg)',y='class' , color='Booster Version Category')
            return fig
        if str(site)=='site3':
            dfi=spacex_df[(spacex_df['Payload Mass (kg)']>min_payload) & (spacex_df['Payload Mass (kg)']<max_payload) & (spacex_df['Launch Site']=='KSC LC-39A')]
            fig=px.scatter(dfi,x='Payload Mass (kg)',y='class' , color='Booster Version Category')
            return fig
        if str(site)=='site4':
            dfi=spacex_df[(spacex_df['Payload Mass (kg)']>min_payload) & (spacex_df['Payload Mass (kg)']<max_payload) & (spacex_df['Launch Site']=='CCAFS SLC-40')]
            fig=px.scatter(dfi,x='Payload Mass (kg)',y='class' , color='Booster Version Category')
            return fig





# Run the app
if __name__ == '__main__':
    app.run_server()