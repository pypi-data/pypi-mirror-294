import streamlit as st
from clickable_textbox import my_component

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

sample_llm_response="""This result comes from Excerpt 1. Excerpt 2 is not mentioned, but maybe you can find what you want in excerpt 3? A bi-directional Streamlit Component has two parts: A frontend, which is built out of HTML and any other web tech you like (JavaScript, React, Vue, etc.), and gets rendered in Streamlit apps via an iframe tag. 
A Python API, which Streamlit apps use to instantiate and talk to that frontend 
To make the process of creating bi-directional Streamlit Components easier, we've created a React template and a TypeScript-only template in the Streamlit Component-template GitHub repo. We also provide some example Components in the same repo.

not sure if a new para works, hopefully it does otherwise we are gonna have to troubleshoot again!"""

excerpt_selected = my_component(llm_response=sample_llm_response, height=400, width=500)
st.markdown(f"You've selected {excerpt_selected}")

st.markdown("---")