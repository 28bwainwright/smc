import streamlit as st
from pathlib import Path

st.set_page_config('SMC 2025 Volunteers', page_icon='smc_logo.png')
st.logo(image='smc_logo.png')
st.html('styles.html')
st.image('smc_main.png', use_container_width=True)
st.html('<h4>Thank you for volunteering at SMC!</h4>')

map_page = st.Page(
    page=Path.cwd().joinpath('sections').joinpath('map.py'),
    title='Map of SMC',
    icon=":material/map:"
    )

schedule_page = st.Page(
    page=Path.cwd().joinpath('sections').joinpath('schedule.py'),
    title='Full Schedule',
    icon=":material/event_upcoming:"
    )

volunteer_page = st.Page(
    page=Path.cwd().joinpath('sections').joinpath('volunteer.py'),
    title='Volunteer', 
    default=True,
    icon=':material/groups:'
    )

pages = {
    'SMC Volunteer App': [volunteer_page, schedule_page, map_page],
}

pg = st.navigation(pages=pages)
pg.run()
