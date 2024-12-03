import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.title("Conversational Recipe Innovation Bot")
st.write("Get innovative recipes based on your preferences and ingredients.")

# State management
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Input section
user_input = st.text_input("Your input:")
if user_input:
    st.session_state.conversation.append(f"You: {user_input}")
    if "ingredients" in user_input.lower():
        st.session_state.conversation.append("Bot: What ingredients do you have?")
    else:
        st.session_state.conversation.append("Bot: Let's refine your query further!")

# Display conversation
for message in st.session_state.conversation:
    st.write(message)

# Submit button for ingredients
if st.button("Submit Ingredients"):
    ingredients = st.text_input("Enter ingredients (comma-separated):")
    if ingredients:
        response = requests.post(
            f"{API_BASE_URL}/generate_recipe/",
            json={"ingredients": ingredients.split(","), "preferences": {}},
        )
        if response.status_code == 200:
            recipes = response.json().get("recipes", [])
            st.write("Here are some recipe suggestions:")
            for recipe in recipes:
                st.write(f"- {recipe.get('title', 'Unknown Recipe')}")
        else:
            st.write("Error: Could not fetch recipes.")
