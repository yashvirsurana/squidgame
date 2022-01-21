# streamlit_app.py
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from streamlit_autorefresh import st_autorefresh
import plotly.io as pio
import plotly.graph_objects as go
from PIL import Image
import base64
import random

ENV=open(".streamlit/config.toml").read().splitlines()[1].split('=')[1].strip('\"')

if ENV=="dark":
    pio.templates.default = "plotly_dark"
    line_col = "rgb(255, 255, 255)"
elif ENV=="light":
    pio.templates.default = "plotly_white"
    line_col = "rgb(0, 0, 0)"

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

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


count = st_autorefresh(interval=2000, limit=10000, key="fizzbuzzcounter")
count += 15

st.write(random_line('cons.txt')[:50])

img_src = "1.jpg"
if count % 4 == 0:
    img_src = "1.jpg"
elif count % 4 == 1:
    img_src = "2.jpg"
elif count % 4 == 2:
    img_src = "3.jpg"
elif count % 4 == 3:
    img_src = "4.jpg"


@st.cache(persist=True, show_spinner=False)
def get_img(sourcef):
    image = Image.open(sourcef)
    return image

conn = connect()

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
#sheet_url = """https://docs.google.com/spreadsheets/d/1jLnhybJCZVIAhlGAhjtHkhZlPIhu0oaOiFJVZzoUmCc/edit#gid=0"""
rows = run_query(f'SELECT * FROM "{sheet_url}"')

df = pd.DataFrame(rows)
df['c'] = 1
a = df.groupby('name').sum().reset_index().sort_values(by='c', ascending=True)
a.c = a.c-1

@st.cache(persist=True, show_spinner=False)
def give_fig(x,y):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            base=0.0001,
            marker=go.bar.Marker(
                color="rgb(250, 56, 113)",
                line=dict(color=line_col,
                          width=3)
            ),
            orientation="h",
        )
    )

    # update layout properties
    fig.update_layout(
        #title=("Winner Winner Chicken Dinner!"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        font=dict(
            # family="Courier New, monospace",
            family="Game of Squids",
            size=10
        ),
        margin=dict(r=0, l=0, b=0, t=0),
    )

    return fig

col1, col2 = st.columns(2)

with col1:

    #st.header(random_line('cons.txt')[:11])
    st.header("Welcome...")
    st.image(get_img(img_src))

with col2:

    st.plotly_chart(give_fig(a.c,a.name), use_container_width=True)

st.markdown(
        """
        <style>
@font-face {
  font-family: 'Game Of Squids';
  font-style: normal;
  font-weight: 400;
  src: url('squidfont.woff2') format('woff2');
}

    html, body, [class*="css"]  {
    font-family: 'Game Of Squids';
    }
    </style>

    """,
        unsafe_allow_html=True,
    )

quote = open('quotes.txt').read().splitlines()
num = (str(count)[-2])
st.write(quote[int(num)*7%15])

if count % 10 == 0:
    st.balloons()
