from groq import Groq
from utils import setup_data
import pandas as pd
from chart_template_generation import generate_chart_from_data


PROMPT_SYSTEM = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

You are a data analyst expert using python and JSON. You have to write a python code that returns a JSON to answer to the QUERY.

You are given a Pandas DataFrame. It represents informations about the bike-sharing FIFTEEN company with one line per day:
- Columns:
{types}

- df.head():
{head}

Your script MUST conclude by assigning a JSON dictionary which will be loadable. It will be a json object named json_obj, it is MANDATORY. It needs to have a plot_type key and the value needs to be one of the following: "bar", "line", "scatter".
It also needs to have in a "data" section, the values that will be needed to answer the query. And finally, x and y values need to be precised so we will create a chart from it. You have to generate the values of the DataFrame not python code.
Here are some examples of result:
- {{"plot_title": "Number of available bikes per day", "plot_type": "line", "data": {{'days': {{str(index): date for index, date in enumerate(list(df["day"]))}},'available_bikes': df["available_bikes"].to_dict()}}, "x": "days", "y": "available_bikes"}}
- {{"plot_title": "Trips per user per day", "plot_type": "bar", "data": {{'days': df["day"].to_dict(),'trips_per_user': {{i: round(val, 2) for i, val in enumerate(df['trips_per_user'])}}}}, "x": "days", "y": "trips_per_user"}}
- {{"plot_title": "Number of bikes in need of warehouse per day compared to available bikes", "plot_type": "bar", "data": {{'days': df["day"].to_dict(),'Need_Warehouse': df["Need_Warehouse"].to_dict(), "available_bikes": df["available_bikes"].to_dict()}}, "x": "days", "y": ["need_warehouse", "available"]}}

**Important Notes:**
- Not all DataFrame columns may be relevant for answering the specific QUERY. Focus only on the necessary ones.
- Field maintenance, Lost, InSearch, To Deploy, Warehouse Maintenance, Need Warehouse, Functional represent all bikes status.
- Bad, Good, Top represent user satisfaction.
- Ensure your code is ERROR-FREE and can be executed directly.
- Include comments in your script to explain your logic and steps taken.
- Let's Think Step by Step."""

data = setup_data()
pd.set_option("display.max_columns", None)
sample = data.sample(n=5)
prompt_system = PROMPT_SYSTEM.format(
    types=data.dtypes,
    head=sample,
    data_day_dict=data["day"].to_dict(),
    data_bikes_dict=data["available_bikes"].to_dict(),
    data_need_warehouse_dict=data["Need_Warehouse"].to_dict(),
)
python_response = """```python
import pandas as pd
from utils import setup_data

df = setup_data()"""

# "How many trips per user do we have per day in average ?"
# "How many bikes in need warehouse do we have per day compare to available bikes ?"
user_query = "Plot bikes per maintenance state per month"
prompt = [
    {"content": prompt_system, "role": "system"},
    {"content": user_query, "role": "user"},
    {"content": python_response, "role": "assistant"},
]


GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

generated_code = groq_client.chat.completions.create(
    messages=prompt,
    model="llama3-70b-8192",
)

generated_json = (generated_code.choices[0].message.content).split("```")[0]


# Assuming your dataframe is set up here
df = setup_data()
df = df.reset_index()
df["day"] = pd.to_datetime(df["day"])

df = df.sort_values(by="day")
# df["day"] = df["day"].dt.strftime("%Y-%m-%d")

local_vars = {}
exec(generated_json, globals(), local_vars)
json_obj = local_vars["json_obj"]

generate_chart_from_data(str(json_obj))
