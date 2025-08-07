import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table, Input, Output, State
import json

# Load data
path = "./data/"

df_info = pd.read_csv(path + "bills_info.csv")
df_info = df_info[['bill_number', 'title', 'companion', 'subject', 'relevant', 'session', 'status', 'status_date', 'source', 'chat']]

df_history = pd.read_csv(path + "bills_history.csv")
df_history = df_history[['bill_number', 'title', 'date', 'chamber', 'action']]

df_progress = pd.read_csv(path + "bills_progress.csv")
df_progress = df_progress[['bill_number', 'title', 'date', 'event']]

df_calendar = pd.read_csv(path + "bills_calendar.csv")
df_calendar = df_calendar[['bill_number', 'title', 'type', 'date', 'time', 'location', 'description']]

# relevancy dict
with open(path+'Gemini/relevancy_results.json', "r") as f:
    relevancy_dict = json.load(f)
# add relevancy to each bill
df_info['relevant'] = df_info['bill_number'].map(relevancy_dict)
df_history['relevant'] = df_history['bill_number'].map(relevancy_dict)
df_progress['relevant'] = df_progress['bill_number'].map(relevancy_dict)
df_calendar['relevant'] = df_calendar['bill_number'].map(relevancy_dict)

# Initialize app
app = dash.Dash(__name__)
app.title = "Legislature Bill Tracking"

# Dropdown options
bill_number_options = [{'label': num, 'value': num} for num in df_info['bill_number'].unique()]
relevancy_options = [{'label': num, 'value': num} for num in df_info['relevant'].unique()]
title_options = [{'label': title, 'value': title} for title in df_info['title'].unique()]

# Layout
app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/logo2.png", style={'height': '100px', 'marginBottom': '10px'}),
        html.H1("Legislature Bill Tracking", style={'margin': '0'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Div([
        html.H2('Filter Bills'),
        dcc.Dropdown(
            id='common-title-filter',
            options=title_options,
            placeholder="Filter by Title",
            multi=True,
            style={'margin-bottom': '10px', 'width': '600px'}
        ),
        dcc.Dropdown(
            id='common-relevancy-filter',
            options=relevancy_options,
            placeholder="Filter by Relevancy",
            multi=True,
            style={'margin-bottom': '10px', 'width': '600px'}
        ),
        dcc.Dropdown(
            id='common-bill-number-filter',
            options=bill_number_options,
            placeholder="Filter by Bill Number",
            multi=True,
            style={'margin-bottom': '20px', 'width': '200px'}
        ),
        html.Button('Reset Filters', id='reset-common', n_clicks=0, style={'margin-bottom': '40px'}),
    ], style={'margin-bottom': '40px'}),

    html.Div([
        html.H2('Bill Info'),
        html.Button("Download CSV", id="download-info-btn", n_clicks=0, style={'marginBottom': '10px'}),
        dcc.Download(id="download-info-csv"),
        dash_table.DataTable(
            id='info-table',
            columns=[
                {"name": i, "id": i, "presentation": "markdown"} if i == 'source' else {"name": i, "id": i}
                for i in df_info.columns
            ],
            data=df_info.assign(
                source=df_info['source'].apply(lambda x: f"[link]({x})" if pd.notnull(x) else "")
            ).to_dict('records'),
            filter_action="native",
            sort_action="native",
            page_size=5,
            style_table={'overflowX': 'auto'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'rgb(173, 216, 230)',
                'textAlign': 'left',
                'fontSize': '16px',
            },
            style_cell={
                'textAlign': 'left',
                'padding': '8px',
                'height': 'auto',
                'fontSize': '14px',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                {'if': {'state': 'active'}, 'backgroundColor': 'rgb(220, 230, 241)', 'border': '1px solid #0074D9'}
            ]
        )
    ], style={'margin-bottom': '60px'}),

    html.Div([
        html.H2('Bill Calendar'),
        html.Button("Download CSV", id="download-calendar-btn", n_clicks=0, style={'marginBottom': '10px'}),
        dcc.Download(id="download-calendar-csv"),
        dash_table.DataTable(
            id='calendar-table',
            columns=[{"name": i, "id": i} for i in df_calendar.columns if i != 'relevant'],
            data=df_calendar.to_dict('records'),
            filter_action="native",
            sort_action="native",
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'rgb(173, 216, 230)',
                'textAlign': 'left',
                'fontSize': '16px',
            },
            style_cell={
                'textAlign': 'left',
                'padding': '8px',
                'fontSize': '14px',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                {'if': {'state': 'active'}, 'backgroundColor': 'rgb(220, 230, 241)', 'border': '1px solid #0074D9'}
            ]
        )
    ], style={'margin-bottom': '60px'}),

    html.Div([
        html.H2('Bill History'),
        html.Button("Download CSV", id="download-history-btn", n_clicks=0, style={'marginBottom': '10px'}),
        dcc.Download(id="download-history-csv"),
        dash_table.DataTable(
            id='history-table',
            columns=[{"name": i, "id": i} for i in df_history.columns if i != 'relevant'],
            data=df_history.to_dict('records'),
            filter_action="native",
            sort_action="native",
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'rgb(173, 216, 230)',
                'textAlign': 'left',
                'fontSize': '16px',
            },
            style_cell={
                'textAlign': 'left',
                'padding': '8px',
                'fontSize': '14px',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                {'if': {'state': 'active'}, 'backgroundColor': 'rgb(220, 230, 241)', 'border': '1px solid #0074D9'}
            ]
        )
    ], style={'margin-bottom': '60px'}),

    html.Div([
        html.H2('Bill Progress (Select a Bill)'),
        dcc.Graph(id='progress-timeline')
    ], style={
        'margin-bottom': '60px',
        'backgroundColor': 'rgb(240, 248, 255)',
        'border': '2px solid rgb(173, 216, 230)',
        'borderRadius': '10px',
        'padding': '20px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),
], style={'margin-left': '150px', 'margin-right': '150px'})


# Callbacks
@app.callback(
    Output('info-table', 'data'),
    Output('calendar-table', 'data'),
    Output('history-table', 'data'),
    Output('progress-timeline', 'figure'),
    Output('common-bill-number-filter', 'options'),
    Input('common-bill-number-filter', 'value'),
    Input('common-title-filter', 'value'),
    Input('common-relevancy-filter', 'value')
)
def update_tables_and_progress(bill_numbers, titles, relevancies):
    # Info table
    dff_info = df_info.copy()
    if bill_numbers:
        dff_info = dff_info[dff_info['bill_number'].isin(bill_numbers)]
    if titles:
        dff_info = dff_info[dff_info['title'].isin(titles)]
    if relevancies:
        dff_info = dff_info[dff_info['relevant'].isin(relevancies)]
    dff_info['source'] = dff_info['source'].apply(lambda x: f"[link]({x})" if pd.notnull(x) else "")

    # Calendar table
    dff_calendar = df_calendar.copy()
    if bill_numbers:
        dff_calendar = dff_calendar[dff_calendar['bill_number'].isin(bill_numbers)]
    if titles:
        dff_calendar = dff_calendar[dff_calendar['title'].isin(titles)]
    if relevancies:
        dff_calendar = dff_calendar[dff_calendar['relevant'].isin(relevancies)]

    # History table
    dff_history = df_history.copy()
    if bill_numbers:
        dff_history = dff_history[dff_history['bill_number'].isin(bill_numbers)]
    if titles:
        dff_history = dff_history[dff_history['title'].isin(titles)]
    if relevancies:
        dff_history = dff_history[dff_history['relevant'].isin(relevancies)]

    # Progress
    if bill_numbers:
        dff_progress = df_progress[df_progress['bill_number'].isin(bill_numbers)].copy()
    else:
        dff_progress = pd.DataFrame()

    # Recompute bill-number options if filtering by title and relevancy
    dff_filtered = df_info.copy()
    if titles:
        dff_filtered = dff_filtered[dff_filtered['title'].isin(titles)]
    if relevancies:
        dff_filtered = dff_filtered[dff_filtered['relevant'].isin(relevancies)]
    
    filtered_bill_numbers = dff_filtered['bill_number'].unique()
    bill_number_options = [{'label': num, 'value': num} for num in filtered_bill_numbers]

    # Build timeline figure
    if not bill_numbers:
        fig = go.Figure()
        title_text = "Progress Timeline"
        if bill_numbers:
            title_text += f" for {', '.join(bill_numbers)}"
        fig.update_layout(
            title=title_text,
            xaxis_title="Date",
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            xaxis=dict(showgrid=True),
            showlegend=False,
            margin={"r":10,"t":40,"l":10,"b":10},
            height=600
        )
    elif not dff_progress.empty:
        dff_progress['date'] = pd.to_datetime(dff_progress['date'], yearfirst=True, errors='coerce')
        dff_progress = dff_progress.sort_values('date')
        dff_progress['y_pos'] = np.arange(len(dff_progress))[::-1]

        unique_events = dff_progress['event'].unique()
        color_palette = px.colors.qualitative.Plotly
        color_map = {event: color_palette[i % len(color_palette)] for i, event in enumerate(unique_events)}

        fig = go.Figure()
        fig.add_shape(
            type='line',
            x0=dff_progress['date'].min(),
            x1=dff_progress['date'].max(),
            y0=0,
            y1=0,
            line=dict(color='black', width=6)
        )

        fig.add_trace(
            go.Scatter(
                x=dff_progress['date'],
                y=dff_progress['y_pos'],
                mode='markers+text',
                marker=dict(
                    size=16,
                    color=[color_map[event] for event in dff_progress['event']],
                    line=dict(width=2, color='DarkSlateGrey')
                ),
                text=dff_progress['event'],
                textposition='top center',
                hovertemplate= "<b>Date:</b> %{x|%Y-%m-%d}<extra></extra>"
            )
        )

        title_text = "Progress Timeline"
        if bill_numbers:
            title_text += f" for {', '.join(bill_numbers)}"
        fig.update_layout(
            title=title_text,
            xaxis_title="Date",
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            xaxis=dict(showgrid=True),
            showlegend=False,
            margin={"r":10,"t":40,"l":10,"b":10},
            height=600
        )
    else:
        fig = go.Figure()
        fig.update_layout(title='Bill Progress', height=600)

    return dff_info.to_dict('records'), dff_calendar.to_dict('records'), dff_history.to_dict('records'), fig, bill_number_options


# Reset filters
@app.callback(
    Output('common-bill-number-filter', 'value'),
    Output('common-title-filter', 'value'),
    Output('common-relevancy-filter', 'value'),
    Input('reset-common', 'n_clicks')
)
def reset_filters(n_clicks):
    return None, None, None


# CSV download callbacks
@app.callback(
    Output("download-info-csv", "data"),
    Input("download-info-btn", "n_clicks"),
    State("info-table", "data"),
    prevent_initial_call=True
)
def download_info(n_clicks, table_data):
    return dcc.send_data_frame(pd.DataFrame(table_data).to_csv, filename="bill_info.csv", index=False)

@app.callback(
    Output("download-calendar-csv", "data"),
    Input("download-calendar-btn", "n_clicks"),
    State("calendar-table", "data"),
    prevent_initial_call=True
)
def download_calendar(n_clicks, table_data):
    return dcc.send_data_frame(pd.DataFrame(table_data).to_csv, filename="bill_calendar.csv", index=False)

@app.callback(
    Output("download-history-csv", "data"),
    Input("download-history-btn", "n_clicks"),
    State("history-table", "data"),
    prevent_initial_call=True
)
def download_history(n_clicks, table_data):
    return dcc.send_data_frame(pd.DataFrame(table_data).to_csv, filename="bill_history.csv", index=False)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
