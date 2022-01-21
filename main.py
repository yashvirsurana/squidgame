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
    font-family: 'squid';
    src: url('data:font/woff2;charset=utf-8;base64,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') format('woff2');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

        html, body, [class*="css"]  {
        font-family: 'squid';
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
