import streamlit as st
import streamlit as st
import polars as pl
import polars.selectors as cs

from streamlit_gsheets import GSheetsConnection
from pathlib import Path
from datetime import date

conn = st.connection("gsheets", type=GSheetsConnection)

class Main:
    static: Path
    year: int
    conn = st.connection("gsheets", type=GSheetsConnection)

    def __init__(self) -> None:
        if date.today().month == 1:
            self.year = date.today().year

        else:
            self.year = date.today().year+1
        self.static = Path.cwd().joinpath(str(self.year))

    @property
    def logo(self): 
        return self.static.joinpath('logo.png')
    
    @property
    def title(self): 
        return self.static.joinpath('title.png')
    
    @property
    def map(self): 
        return self.static.joinpath('map.png')
    
    @property
    def schedule(self): 
        return self.static.joinpath('schedule.png')

    def landing(self):
        st.set_page_config(page_title=f'SMC {self.year} Volunteers', page_icon=self.logo)
        st.logo(image=self.logo, size='medium')

        with st.container(horizontal=True, horizontal_alignment='center'):
            st.image(self.title, width='stretch')

        with st.container(horizontal=True, horizontal_alignment='center'):
            st.subheader(f'Thank you for volunteering at SMC {self.year}!', text_alignment='center')

    def map_page(self):
        self.landing()
        st.container().image(self.map)

    def schedule_page(self):
        self.landing()
        st.container().image(self.schedule)

    @st.fragment()
    def volunteer(self):

        self.landing()
        with st.container(border=True):

            volunteers = self.get_data_from_sheet(day=1)
            volunteer: str | None = st.selectbox(label='Volunteer Name', index=None, options=volunteers.select('full name').unique().sort(by='full name'), placeholder='Select a name to view volunteer schedule')
            if volunteer is None:
                st.warning('Please select a volunteer to view the schedule')
                st.stop()

            days = {'January 2nd': 2, 'January 3rd': 3, 'January 4th': 4, 'January 5th': 5}
            tabs = st.tabs(list(days.keys()))

            for tab, day in zip(tabs, days):
                with tab:
                    df = self.get_data_from_sheet(day=days.get(day, 2))
                    df = (
                        df
                        .filter(pl.col('full name')==volunteer)
                        .drop(cs.contains('first name', 'last name', 'full name'))
                    )

                    if df.is_empty():
                        st.warning(f"{volunteer} not scheduled for {day}")
                    else:
                        try:
                            self.display_schedule(df=df, volunteer=volunteer, day=day)
                        except Exception as e:
                            
                            st.warning(f"Unable to display {volunteer}'s schedule for {day}")

    
    def get_data_from_sheet(self, day: int) -> pl.DataFrame:
        full_name = pl.concat_str(cs.contains('first name').str.strip_chars(), cs.contains('last name').str.strip_chars(), separator=' ').alias('full name')
        return (
            pl.from_pandas(self.conn.read(worksheet=day))
            .rename(lambda x: x.lower())
            .with_columns(full_name,)
            )

    def display_schedule(self, df: pl.DataFrame, volunteer: str, day: str) -> None: 

        df = df.transpose(include_header=True, header_name='event').rename({'column_0': 'details'}).drop_nulls()
        if df.is_empty():
            st.warning(f"{volunteer} not scheduled for {day}")

        else:
            for event, details in df.iter_rows(named=False):

                event: str = event
                details: str = details

                if details: 
                    with st.expander(label=f"**{event.upper().strip()}**", expanded=True):
                        for idx, info in enumerate(details.split(';')):
                            if idx == 0:
                                st.subheader(info, text_alignment='center', width='stretch')
                            else:
                                st.text(info, text_alignment='center', width='stretch')

    def pages(self):

        map_page = st.Page(
            page=self.map_page,
            title='Map of SMC',
            icon=":material/map:"
            )

        schedule_page = st.Page(
            page=self.schedule_page,
            title='Full Schedule',
            icon=":material/event_upcoming:"
            )

        volunteer_page = st.Page(
            page=self.volunteer,
            title='Volunteer', 
            default=True,
            icon=':material/groups:'
            )

        return {
            'SMC Volunteer App': [volunteer_page, schedule_page, map_page],
        }

main = Main()
pg = st.navigation(pages=main.pages())
pg.run()
