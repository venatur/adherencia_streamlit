# Import convention
import streamlit as st
import psycopg2
import pandas as pd
import streamlit_pandas as sp

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()



@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
rows = run_query("select * from pausasxmes")

data = pd.DataFrame(rows)
data.columns=["usuario","pausa","mes","year"]

all_widgets = sp.create_widgets(data)
res = sp.filter_df(data, all_widgets)
st.write(res)
res["pausa"] = res["pausa"].astype(float)
restobar = res.copy()
st.bar_chart(restobar, x="usuario", y=["pausa"], color="mes")
