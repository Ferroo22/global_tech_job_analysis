import streamlit as st

# CONFIGURATION
st.set_page_config(page_title="Home", layout="wide")

st.title("Data Science Salaries Explorer")

st.markdown("""
Welcome to the Data Science Salaries Explorer!  
Use the sidebar to navigate between pages:

- **Global Analysis:** Explore data science jobs and salaries globally
- **US Analysis:** Explore data science jobs and salaries in the United States.
- **Compare US vs Others:** Compare US data with other countries.


---

**Instructions:**  
Select a page from the sidebar to get started.
""")

st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar links above to switch pages.")

