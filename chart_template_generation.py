import plotly.graph_objs as go
from jinja2 import Template
import json
from utils import setup_data
import os
import re


def convert_to_proper_json_like_string(data_string):
    # Add double quotes around any sequence of characters that is followed by a colon
    data_string = re.sub(r"(?<=\b)(\w+)(?=\s*:)", r'"\1"', data_string)

    # Add double quotes around numerical keys
    data_string = re.sub(r'(?<="{)\b(\d+)\b(?=":)', r'"\1"', data_string)

    return data_string


def generate_chart_from_data(json_data):
    # Define the Jinja template for different chart types
    chart_template = """
import plotly.graph_objs as go
import json
import os

def create_chart(data):
    data = json.loads(data)
    fig = go.Figure()
    x = data.get("x")
    y = data.get("y")
    {% if chart_type == 'bar' %}
    for i in y:
        fig.add_trace(go.Bar(x=list(data.get("data").get(x).values()), y=list(data.get("data").get(i).values())))
    {% elif chart_type == 'line' %}
    fig.add_trace(go.Scatter(x=list(data.get("data").get(x).values()), y=list(data.get("data").get(y).values()), mode='lines+markers'))
    {% elif chart_type == 'scatter' %}
    fig.add_trace(go.Scatter(x=list(data.keys()), y=list(data.values()), mode='markers'))
    {% endif %}
    fig.update_layout(title='{{ chart_title }}', xaxis_title=x, yaxis_title="hello")
    # fig.show()

    if not os.path.exists("images"):
        os.mkdir("images")
    fig.write_image("images/fig1.png")

create_chart('''{{ data_json }}''')"""

    # Create a template object
    template = Template(chart_template)

    converted_data = convert_to_proper_json_like_string(json_data)
    data_json = json.loads(converted_data.replace("'", '"').strip())

    # Render the template with specific chart type and data
    # We serialize data to JSON to handle it easily within the template
    rendered_script = template.render(
        chart_title=data_json.get("plot_title"),
        chart_type=data_json.get("plot_type"),
        data_json=converted_data.replace("'", '"').strip(),
    )

    # Execute the rendered script
    exec(rendered_script)
