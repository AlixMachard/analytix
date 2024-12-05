from groq import Groq
from utils import setup_data
import pandas as pd
from chart_template_generation import generate_chart_from_data
from prompt.imdb import PROMPT_SYSTEM

data = setup_data()
pd.set_option("display.max_columns", None)
sample = data.sample(n=5)
prompt_system = PROMPT_SYSTEM.format(
    types=data.dtypes,
    head=sample,
)
python_response = """```python
import pandas as pd
from utils import setup_data

df = setup_data()"""

# "How many trips per user do we have per day in average ?"
# "How many bikes in need warehouse do we have per day compare to available bikes ?"
user_query = "Plot the 10 first rated movies"
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
df = df.applymap(lambda x: x.replace('"', "'") if isinstance(x, str) else x)

if "day" in df:
    df["day"] = pd.to_datetime(df["day"])

    df = df.sort_values(by="day")
# df["day"] = df["day"].dt.strftime("%Y-%m-%d")

local_vars = {}
exec(generated_json, globals(), local_vars)
json_obj = local_vars["json_obj"]

generate_chart_from_data(str(json_obj))
