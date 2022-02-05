import streamlit as st

from pager import AppPager
from pages import demo

#
# Wide Mode
#
st.set_page_config(layout="wide")
st.title("TartanHacks 2022")

#
# Apps
#
apps = AppPager()
apps.add("Demo", demo.app)
apps.run()