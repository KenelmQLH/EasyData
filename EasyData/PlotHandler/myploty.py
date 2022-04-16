import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd


def show_df_value_counts(df, col="category", title=""):
    cnt = df[col].value_counts().reset_index()
    cnt.columns = [ 'c' , 'n']

    fig = px.bar(
        cnt , x = 'c', y = 'n' , text_auto='.2s',
        title = title
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.show()


def show_df_bar(df, col_x, col_y, color="", title=""):
    fig = px.bar(
        df , x = col_x, y = col_y , text_auto='.2s',
        color = color,
        title = title
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.show()
