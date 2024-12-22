import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)


def make_full_name(df: pd.DataFrame) -> pd.DataFrame:
    df['FULL NAME'] = df['FIRST NAME'] + ' ' + df['LAST NAME'] 
    df['FULL NAME'] = df['FULL NAME'].str.strip()
    df = df.drop(labels=['FIRST NAME', 'LAST NAME'], axis=1)
    return df.set_index('FULL NAME')


def display_volunteer_roles(df: pd.DataFrame, date: str, volunteer: str) -> None:
    
    if not volunteer:
        st.warning('Please select a volunteer to view a schedule')

    else:
        df = df[df.index==volunteer]
        df: pd.DataFrame = df.T.dropna()

        if df.empty:
            st.warning(f'No roles for {volunteer} on {date}')

        else:
            for idx, row in df.itertuples(index=True, name='Role'):
                with st.container(border=True):
                    st.html(f'<h3>{idx}</h3>')
                    if isinstance(row, str):
                        values = row.split(sep=";")
                        for v in values:
                            st.html(f"<p>{v}</p>")


users = conn.read(worksheet=1)
users = make_full_name(df=users)

volunteer = st.selectbox(
    label='Volunteer Name', 
    index=None,
    options=sorted(users.index.unique()),  
    placeholder='Choose a volunteer to view their schedule')

jan2, jan3, jan4, jan5 = st.tabs(['January 2nd', 'January 3rd', 'January 4th', 'January 5th'])


with jan2:
    df = conn.read(worksheet=2)
    df = make_full_name(df=df)
    # st.write(df)
    display_volunteer_roles(df=df, date='January 2nd', volunteer=volunteer)

with jan3:
    df = conn.read(worksheet=3)
    df = make_full_name(df=df)
    # st.write(df)
    display_volunteer_roles(df=df, date='January 3rd', volunteer=volunteer)

with jan4:
    df = conn.read(worksheet=4)
    df = make_full_name(df=df)
    display_volunteer_roles(df=df, date='January 4th', volunteer=volunteer)

with jan5:
    df = conn.read(worksheet=5)
    df = make_full_name(df=df)
    display_volunteer_roles(df=df, date='January 5th', volunteer=volunteer)


