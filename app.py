import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Load Data
url = 'https://raw.githubusercontent.com/dirkkoolmees/CO2_emissions_per-region/master/Carbondioxide_python.csv'
df = pd.read_csv(url, index_col = 'Year')

df_1950_2014 = pd.DataFrame(df[df.index >= 1950])

max_year = 2014

min_year = 1950

df_range = df_1950_2014[df_1950_2014.index <= max_year]

df_range = df_range[df_range.index >= min_year]

df_range_sum = df_range.groupby('Region').sum(numeric_only = True)

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H3("CO2 Emissions per region"),
        html.Div([
        dcc.Dropdown(
            id='column', clearable=False,
            value='Total CO2 emissions from fossil-fuels and cement production (thousand metric tons of C)',
            options=[
                {'label': c, 'value': c}
                for c in df_range_sum.columns
            ]),
        ],style={'display': 'inline', 'width': '15%'}),
    
    html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=min_year,
        max=max_year,
        step=1,
        value=[min_year, max_year]
    ),
    html.Div(id='output-container-range-slider')
],style={'display': 'inline', 'width': '15%'}),
        
        html.Div([
        dcc.Graph(id='graph_1'),
    ],style={'display': 'inline-block', 'width': '55%'}),
        
        html.Div([
        dcc.Graph(id='graph_2'),
    ],style={'display': 'inline-block', 'width': '45%'}),
    
     html.Div([
        dcc.Graph(id='graph_3'),
    ],style={'display': 'inline-block', 'width': '100%'})
])

def create_graphs(column, value):
    
    min_year = value[0]
    max_year = value[1]
    
    df_range = df_1950_2014[df_1950_2014.index <= max_year]

    df_range = df_range[df_range.index >= min_year]

    df_range_sum = df_range.groupby('Region').sum(numeric_only = True)
    
    fig1 = px.area(df_range, x=df_range.index, y=column,
                   color='Region',
                   color_discrete_sequence=px.colors.sequential.RdBu)
    
    title = column + ' from ' + str(min_year) + ' to '+ str(max_year)

    fig1.update_layout(
    title=title,
    yaxis_title= 'CO2 Emissions',
    xaxis_title= '',
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=1.05),
    )
    
    fig2 = px.pie(df_range_sum, values = column, names = df_range_sum.index, color = df_range_sum.index,
             color_discrete_sequence=px.colors.sequential.RdBu,
             labels={column:column},
             hole = 0.3)

    fig2.update_layout(title_text='', showlegend = False)
    
    fig2.update_traces(textposition='outside', textinfo='percent+label')

    fig3 = px.box(df_range, x='Region', y = column, color_discrete_sequence=px.colors.sequential.RdBu, points = False)

    fig3.update_traces(quartilemethod="inclusive") # or "exclusive", or "linear" by default

    fig3.update_layout(
    title='Distribution of ' + column + ' per region' + ' from ' + str(min_year) + ' to '+ str(max_year),
    yaxis_title=column,
    xaxis_title=' '
    )

    return fig1, fig2, fig3

# Define callback to update graph
@app.callback(
    [
    Output('output-container-range-slider', 'children')],
    [Input("column", "value"), Input('my-range-slider', 'value')]
)

@app.callback(
    [Output('graph_1', 'figure'),
     Output('graph_2', 'figure'),
     Output('graph_3', 'figure')],
    [Input("column", "value"), Input('my-range-slider', 'value')]
)

def update(column, value):
    return create_graphs(column,value)



# Run app
if __name__ == '__main__':
    app.run_server()
