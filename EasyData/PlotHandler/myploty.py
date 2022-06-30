import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd


def show_df_value_counts(df, col="category", topk=None, title=""):
    cnt = df[col].value_counts().reset_index()
    cnt.columns = [ 'c' , 'n']
    if topk:
        cnt = cnt.loc[:topk]

    fig = px.bar(
        cnt , x = 'c', y = 'n' , text_auto='.2s',
        title = title
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.show()
    return fig, cnt


def show_df_bar(df, col_x, col_y, color=None, title=""):
    if color is not None:
        fig = px.bar(
            df , x = col_x, y = col_y , text_auto='.2s',
            color = color,
            title = title,
        )
    else:
        fig = px.bar(
            df , x = col_x, y = col_y,
            title = title,
        )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.show()


def show_df_sactter(df, x_col, y_col):
    _df = df.sort_values(by=y_col, ascending=False, inplace=False)
    fig = px.scatter(_df, x=x_col, y=y_col, trendline="ols")
    fig.show()

def show_df_pie(df, x_col, y_col):
    fig = px.pie(df, values=y_col, names=x_col,
                title='Total operations',
                hover_data=[y_col])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=600, width=600, autosize = False) # size
    fig.show()