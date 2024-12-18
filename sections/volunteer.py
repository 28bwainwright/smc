import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

view_all, jan2, jan3, jan4, jan5 = st.tabs(['All Days', 'January 2nd', 'January 3rd', 'January 4th', 'January 5th'])

with jan2:
    data = conn.read(worksheet=0)
    st.dataframe(data)

with jan3:
    data = conn.read(worksheet=2)
    st.dataframe(data)

with jan4:
    data = conn.read(worksheet=3)
    st.dataframe(data)

with jan5:
    data = conn.read(worksheet=4)
    st.dataframe(data)

