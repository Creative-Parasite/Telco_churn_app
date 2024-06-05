import streamlit as st
import pandas as pd
import numpy as np
import pyodbc 
from Utils.features import markdown_table

st.set_page_config(page_title="Data Page", page_icon="📑", layout="wide")
st.header("DATA PREVIEW")

col1, col2 = st.columns(spec=[3,3])
with col1:
    container = st.container(height=500,border=False)
    with container:
        st.markdown("<h3 style='text-align: center;'>FEATURE NAMES 🏷️</h3>", unsafe_allow_html=True)
        st.markdown(""" 
            Here is a display list of all the features available and their usage for reference. 
            """)
        with st.expander("Feature names"):
            st.write(markdown_table)
## create a connection to a database
@st.cache_resource(show_spinner="connecting to database...")
def init_connection():
    connection_string = (
        "DRIVER={SQL Server};"
        "SERVER=" + st.secrets['SERVER'] + ";"
        "DATABASE=" + st.secrets['DATABASE'] + ";"
        "UID=" + st.secrets['USERNAME'] + ";"
        "PWD=" + st.secrets['PASSWORD']
    )
    return pyodbc.connect(connection_string)
 
conn = init_connection()

@st.cache_data(show_spinner="Running query...")
def running_query(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame.from_records(rows, columns=columns)
    return df
 
def get_all_columns():
    sql_query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"
    df = running_query(sql_query)
    return df
## load dataset
data1= get_all_columns()
data2 = pd.read_csv("Datafiles\LP2_Telco-churn-second-2000.csv")
df= pd.concat([data1, data2], axis=0)

## Identify columns in dataset
categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()
numerical_columns = df.select_dtypes(include= ["number"]).columns.tolist()

## Create a select box
with col2:
    st.markdown("""
        <style>
    .stSelectbox > div[data-baseweb="select"] > div {
         width: 500px; /* adjust the width here */
     }
     </style>
    """, unsafe_allow_html=True)
    container = st.container(height=500, border=False)  # adjust the width here
    with container:
        st.markdown("<h2 style='text-align: center;'>DATASET🛢️ </h2>", unsafe_allow_html=True)
        options= st.selectbox("Select", ('all columns', 'numerical_columns', 'categorical_columns'))
        if options == "all columns":
            st.write(df)
        elif options == "categorical_columns":
            st.write(df[categorical_columns])
        elif options == "numerical_columns":
            st.write(df[numerical_columns])

