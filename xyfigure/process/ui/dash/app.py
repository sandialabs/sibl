# app.py

# standard libraries
import base64
import csv
import datetime
import io

# third-party libraries
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go

import pandas as pd

# local libraries

app = dash.Dash(__name__)
app.title = "xyfigure"

style_upload = dict(
    width="98%",
    height="60px",
    lineHeight="60px",
    borderWidth="2px",
    borderStyle="dashed",
    borderRadius="5px",
    textAlign="center",
    margin="10px",
)

style_error = dict(
    width="98%",
    borderWidth="2px",
    borderColor="red",
    textAlign="center",
    backgroundColor="lightgray",
    margin="10px",
)

style_trace = dict(mode="lines+markers", marker=dict(color="blue"))

# sliders:
# https://dash.plotly.com/dash-core-components/slider

# marks={i: 'Label {}'.format(i) for i in range(10)},

# sliders, for future reference
#    html.Div(
#        id='id-header',
#        children="Headers:",
#        style={'textAlign': 'center', 'width': '100px', 'visibility': 'hidden'}
#    ),
#    html.Div([
#        html.Div(
#            dcc.Slider(
#                id='header-slider',
#                min=0,
#                max=1,
#                marks={0: 'off', 1: 'on'},
#                value=1
#            ),
#            style={'width': '100px', 'display': 'inline-block', 'visibility': 'hidden'}
#        ),
#        html.Div(
#            id='slider-feedback',
#            style={'display': 'inline-block', 'font-size': 'xx-small', 'vertical-align': 'top', 'visibility': 'hidden'}
#        )]
#    ),


app.layout = html.Div(
    [
        html.Div(
            id="id-header", children=html.H2("xyfigure"), style={"textAlign": "center"}
        ),
        dcc.Upload(
            id="data-upload",
            children=html.Div(
                ["Drag and drop files here, or ", html.A("click to select files")]
            ),
            style=style_upload,
            multiple=True,  # allow mutiples files, not just singletons
        ),
        html.Div(id="data-upload-output"),
    ]
)


def parse_contents(contents, filename, date):
    _, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    has_header = True  # assume headers exist by default, implement non-headers later
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            if has_header:
                df = pd.read_csv(
                    io.StringIO(decoded.decode("utf-8")), sep=",", header="infer"
                )
            else:
                df = pd.read_csv(
                    io.StringIO(decoded.decode("utf-8")), sep=",", header=None
                )

        elif "xls" in filename:  # full implementation will come later
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(
            [
                dcc.Textarea(
                    value=f"There was an error opening the file {filename}.  Error {e}",
                    style=style_error,
                )
            ]
        )

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1], **style_trace))

    fig.update_xaxes(title_text=df.columns[0])
    fig.update_yaxes(title_text=df.columns[1])

    return html.Div(
        [
            dcc.Graph(figure=fig),
            html.H5(filename),
            html.P(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
            ),
            html.Hr()  # horizontal line
            ##  html.Hr(),  # horizontal line
            ##  # For debugging, display the raw contents provided by the web browser
            ##  html.Div('Raw Content'),
            ##  html.Pre(contents[0:200] + '...', style={
            ##      'whiteSpace': 'pre-wrap',
            ##      'wordBreak': 'break-all'
            ##  })
        ]
    )


@app.callback(
    Output("data-upload-output", "children"),
    [Input("data-upload", "contents")],
    [State("data-upload", "filename"), State("data-upload", "last_modified")],
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


# @app.callback(Output('slider-feedback', 'children'),
#               [Input('header-slider', 'value')])
# def update_header_slider(value):
#     # return 'You have selected "{}"'.format(value)
#     if value:
#         return 'First row of data file contains the header.'
#     else:
#         return 'First row of data file contains data (no headers).'

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
