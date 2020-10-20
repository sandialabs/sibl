# app.py

# standard libraries
import base64

# import csv
import datetime
import io

# third-party libraries
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go

import numpy as np
import pandas as pd
from scipy import signal

# local libraries
from controls import SIGNAL_PROC_TYPES  # multi-dropdown options

app = dash.Dash(__name__)
app.title = "zplot"

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
style_trace_filtered = dict(mode="lines+markers", marker=dict(color="red"))

# create controls

signal_process_options = [
    {"label": str(SIGNAL_PROC_TYPES[signal_proc_type]), "value": str(signal_proc_type)}
    for signal_proc_type in SIGNAL_PROC_TYPES
]

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
            id="id_header", children=html.H2("zplot"), style={"textAlign": "center"}
        ),
        dcc.Upload(
            id="id_data_upload",
            children=html.Div(
                ["Drag and drop files here, or ", html.A("click to select files")]
            ),
            style=style_upload,
            multiple=True,  # allow mutiples files, not just singletons
        ),
        html.P("Apply a process to the signal:"),
        # dcc.RadioItems(
        #     id="signal_process_radio",
        #     options=[
        #         {"label": "All ", "value": "all"},
        #         {"label": "Butterworth only ", "value": "butterworth"},
        #         {"label": "Customize ", "value": "custom"},
        #     ],
        #     value="all",
        #     # value="butterworth",
        #     # value="custom",
        #     labelStyle={"display": "inline-block"},
        #     className="dcc_control",
        # ),
        dcc.Dropdown(
            id="id_signal_processes_dropdown",
            options=signal_process_options,
            # multi=True,
            multi=False,
            # value=list(SIGNAL_PROC_TYPES.keys()),
            value=[],
            className="dcc_control",
        ),
        html.Div(id="id_data_upload_output"),
    ]
)


def parse_contents(contents, signal_process, filename, date):
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

    # if signal_process == "DIFF":
    #     y=df.iloc[:, 1]
    #     fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1], **style_trace))

    # else:
    #     fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1], **style_trace))
    x_data = df.iloc[:, 0]
    y_data = df.iloc[:, 1]

    # fig.update_xaxes(title_text=df.columns[0])
    # fig.update_yaxes(title_text=df.columns[1])
    x_title = df.columns[0]
    y_title = df.columns[1]

    if signal_process == "DIFF":
        y_data = np.gradient(y_data, x_data, edge_order=2)  # y before x in this API!
        y_title = "d/dt of " + y_title

    fig.add_trace(go.Scatter(x=x_data, y=y_data, **style_trace))

    if signal_process == "BW":
        dt = x_data[1] - x_data[0]  # sample delta t, assumed uniform
        fs = 1.0 / dt  # Hz
        fc = 5  # Hz, cutoff frequency, hard code for now
        filter_order = 4  # 4th order filter, hard code for now
        filter_type = "low"  # low-pass filter, hard code for now
        Wn = fc / (fs / 2.0)  # Hz/Hz, normalized frequency
        b, a = signal.butter(filter_order, Wn, filter_type)
        y_data_filtered = signal.filtfilt(b, a, y_data)
        fig.add_trace(go.Scatter(x=x_data, y=y_data_filtered, **style_trace_filtered))

    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)

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
            #  html.Hr(),  # horizontal line
            #  # For debugging, display the raw contents provided by the web browser
            #  html.Div('Raw Content'),
            #  html.Pre(contents[0:200] + '...', style={
            #      'whiteSpace': 'pre-wrap',
            #      'wordBreak': 'break-all'
            #  })
        ]
    )


# Radio -> multi
# @app.callback(
#     Output("signal_process_dropdown", "value"), [Input("signal_process_radio", "value")]
# )
# def update_signal_processes_dropdown(input_value):
#     if input_value == "all":
#         return list(SIGNAL_PROC_TYPES.keys())
#     elif input_value == "butterworth":
#         return ["BW"]
#     return []


@app.callback(
    Output("id_data_upload_output", "children"),
    [
        Input("id_data_upload", "contents"),
        Input("id_signal_processes_dropdown", "value"),
    ],
    [State("id_data_upload", "filename"), State("id_data_upload", "last_modified")],
)
def update_output(list_of_contents, signal_process, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, signal_process, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


# if __name__ == "__main__":
#     app.run_server(debug=True, use_reloader=False)

if __name__ == "__main__":
    # app.run_server(debug=False, port=8080, host="0.0.0.0")  # not secure note
    app.run_server(debug=False, port=8050, host="127.0.0.1")  # preferred


# References
# https://community.plotly.com/t/how-to-deploy-dash-app-on-local-network/7169
