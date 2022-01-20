# streamlit_app.py
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

import base64

@st.cache(allow_output_mutation=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('aaa.png')

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=2000, limit=10000, key="fizzbuzzcounter")

# The function returns a counter for number of refreshes. This allows the
# ability to make special requests at different intervals based on the count
if count == 0:
    st.write("welcome")
elif count % 3 == 0 and count % 5 == 0:
    st.write("game")
elif count % 3 == 0:
    st.write("squid")
elif count % 5 == 0:
    st.write("game")
else:
    st.write(f"Count: {count}")
# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=6)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

#sheet_url = st.secrets["public_gsheets_url"]
sheet_url = """https://docs.google.com/spreadsheets/d/1jLnhybJCZVIAhlGAhjtHkhZlPIhu0oaOiFJVZzoUmCc/edit#gid=0"""
rows = run_query(f'SELECT * FROM "{sheet_url}"')

df = pd.DataFrame(rows)
df['c'] = 1
a = df.groupby('name').sum().reset_index()
fig = px.bar(a, x='name', y='c')


col1, col2 = st.columns(2)

with col1:

    st.header("A hjnfgdh")
    st.image("https://static.streamlit.io/examples/owl.jpg")

with col2:

    st.header("Asdgdsgd dos")
    st.plotly_chart(fig, use_container_width=True)


# Print results.
#for row in rows:
#    st.write(f"{row.name} has a playerrr:")