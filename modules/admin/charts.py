import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def pie_chart(series, title):
    fig, ax = plt.subplots()
    series.value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    ax.set_title(title)
    st.pyplot(fig)


def donut_chart(series, title):
    fig, ax = plt.subplots()
    counts = series.value_counts()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%")
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title(title)
    st.pyplot(fig)


def histogram(series, title):
    fig, ax = plt.subplots()
    ax.hist(series, bins=50)
    ax.set_title(title)
    st.pyplot(fig)


def line_trend(df, column, title):
    trend = df.groupby(column).size()
    st.line_chart(trend)


def bar_chart(series, title):
    st.bar_chart(series.value_counts())


def box_plot(df, x, y, title):
    fig, ax = plt.subplots()
    df.boxplot(column=y, by=x, ax=ax)
    ax.set_title(title)
    plt.suptitle("")
    st.pyplot(fig)


def correlation_heatmap(df):
    fig, ax = plt.subplots()
    corr = df.corr()
    cax = ax.matshow(corr)
    fig.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)
    st.pyplot(fig)