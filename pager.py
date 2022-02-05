import streamlit as st


class AppPager:
    def __init__(self) -> None:
        self.apps = []

    def add(self, title, render_func) -> None:
        self.apps.append({
            "title": title,
            "renderer": render_func
        })

    def run(self):
        app = st.sidebar.selectbox(
            'App Navigation',
            self.apps,
            format_func=lambda p: p['title']
        )

        app['renderer']()