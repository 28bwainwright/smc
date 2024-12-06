import streamlit as st
import pandas as pd

st.set_page_config('SMC Branson Volunteer Schedule Builder', layout='centered')
st.html(r'styles.html')


data = pd.read_excel(r'SMC Volunteer Schedule 2024.xlsx', sheet_name='Volunteer Schedule')

data = data.set_index(keys='NAME')
# data = data.T

# st.dataframe(data, use_container_width=True)


volunteer = st.selectbox('Volunteer Name', options=data.index)

# st.write(data.columns)

view = data.loc[volunteer]
view = view.dropna()

view.to_dict()
# st.dataframe(view, use_container_width=True)



for key, value in view.to_dict().items():

    with st.container(border=True):
        cols = st.columns(2)
        with cols[0]:
            st.html(f"<h4>{key}</h4>")

        with cols[1]:
            st.write(value)

