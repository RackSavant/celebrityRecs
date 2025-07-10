import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from core.config import settings

st.title("Minimal Streamlit + Pydantic Settings Example")

st.write(f"API Key: {settings.api_key}")
st.write(f"Temperature: {settings.temperature}")
