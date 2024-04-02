import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

if 'update_trigger' not in st.session_state:
    st.session_state.update_trigger = 0

add_page_title()

show_pages(
    [
        Page("homepage.py", "Home", "🏠"),
        Section(name="Knowledge_Base", icon=":book:"),
        Page("view_all_kb.py", "All_Knowledgebases"),
        Page("manage_kb.py", "Manage_Knowledgebases"),
        Page('view_kb.py', "View_Knowledgebases"),
        Section(name="Knowledge_Chat", icon="💬"),
        Page("chat.py", "Chat!"),
    ]
)


