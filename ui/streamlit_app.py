import streamlit as st
from core.config import settings
from core.models import FashionItem, UserPreferences
from agents.base_agent import BaseAgent
import requests
import json

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = UserPreferences(
        preferred_styles=["casual", "streetwear"],
        preferred_brands=[],
        preferred_colors=[],
        sizes=["M", "L"],
        categories=["shirt", "pants"]
    )

# Configure page
st.set_page_config(
    page_title="Racksavant - Fashion Recommendation System",
    layout="wide"
)

# Sidebar - User Preferences
with st.sidebar:
    st.header("Your Preferences")
    
    # Style preferences
    st.subheader("Preferred Styles")
    styles = st.multiselect(
        "Select your preferred styles",
        ["casual", "streetwear", "business", "sporty", "vintage"],
        default=st.session_state.user_preferences.preferred_styles
    )
    
    # Size preferences
    st.subheader("Sizes")
    sizes = st.multiselect(
        "Select your sizes",
        ["XS", "S", "M", "L", "XL", "XXL"],
        default=st.session_state.user_preferences.sizes
    )
    
    # Save preferences
    if st.button("Save Preferences"):
        st.session_state.user_preferences.preferred_styles = styles
        st.session_state.user_preferences.sizes = sizes
        st.success("Preferences saved!")

# Main content
st.title("Racksavant - Your Personal Fashion Assistant")

# Chat interface
st.subheader("Chat with Your Fashion Assistant")

# Input form
user_input = st.text_input("Ask about fashion or upload an image:")

if user_input:
    # Send request to MCP server
    response = requests.post(
        f"http://localhost:8000/agents/conversation",
        json={
            "agent_type": "conversation",
            "input_data": {
                "message": user_input
            }
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        st.session_state.conversation_history.append({
            "user": user_input,
            "assistant": result["data"]["response"]
        })
    else:
        st.error("Error processing request")

# Display conversation history
for msg in st.session_state.conversation_history:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Assistant:** {msg['assistant']}")

# Recommendations section
st.subheader("Personalized Recommendations")

# TODO: Implement actual recommendation display
st.info("Recommendations will appear here once you interact with the system")
