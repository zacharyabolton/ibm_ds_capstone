# 1. Which site has the largest successful launches?
#    ANSWER: VAFB SLC-43
# 2. Which site has the highest launch success rate?
#    ANSWER: KSC LC-39A
# 3. Which payload range(s) has the highest launch success rate?
#    ANSWER: 1k - 2k; 5k - 7k;
# 4. Which payload range(s) has the lowest launch success rate?
# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
#    launch success rate?

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

# dynamically build drop down options based on unique launch sites in data
drop_down_options = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites = spacex_df[["Launch Site"]].value_counts().index
drop_down_options.extend(
    {'label': site[0], 'value': site[0]} for site in launch_sites)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...)
    dcc.Dropdown(
        id='site-dropdown',
        options=drop_down_options,
        value='ALL',
        placeholder="Select a Launch Site Here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    # dcc.RangeSlider(id='payload-slider',...)
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    ),
    Input(
        component_id='payload-slider',
        component_property='value'
    )
)
def get_pie_chart(entered_site, entered_payload_range):
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] > entered_payload_range[0]) &
        (spacex_df["Payload Mass (kg)"] < entered_payload_range[1])
    ]
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )
        fig2 = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        fig2.update_layout(
            yaxis={'tickvals': [0, 1]}
        )
        return fig, fig2
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(
            filtered_df[filtered_df["Launch Site"] == entered_site],
            names='class',
            title='Total Success Launches for Site {}'.format(entered_site)
        )
        fig2 = px.scatter(
            filtered_df[filtered_df["Launch Site"] == entered_site],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        fig2.update_layout(
            yaxis={'tickvals': [0, 1]}
        )
        return fig, fig2


# Run the app
if __name__ == '__main__':
    app.run_server()
