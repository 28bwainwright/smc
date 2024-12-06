import streamlit as st
import pandas as pd

st.set_page_config('SMC Branson Volunteer Schedule Builder', layout='centered')
st.html(r'styles.html')

@st.cache_data(ttl=3600)
def read_data():
    data = pd.read_excel(r'SMC Volunteer Schedule 2024.xlsx', sheet_name='Volunteer Schedule')
    data = data.set_index(keys='NAME')
    return data

data = read_data()
st.title('Welcome to SMC Branson.')
st.subheader('Thank you for volunteering please select your name below')
volunteer = st.selectbox('Volunteer Name', options=data.index)

view = data.loc[volunteer]
view = view.dropna()
view.to_dict()

for key, value in view.to_dict().items():

    with st.container(border=True):
        cols = st.columns(2)
        with cols[0]:
            st.html(f"<h4>{key}</h4>")

        with cols[1]:
            st.write(value)

