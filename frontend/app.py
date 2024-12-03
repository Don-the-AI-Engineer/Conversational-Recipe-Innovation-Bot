import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.title("Conversational Recipe Innovation Bot")
st.write("Get innovative recipes based on your preferences and ingredients.")

# Initialize conversation state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display conversation
st.write("### Conversation")
for message in st.session_state.conversation:
    st.write(message)

# Input section
user_input = st.text_input("Your input:")
if user_input:
    # Display user input
    st.session_state.conversation.append(f"You: {user_input}")
    
    # Check if the user mentioned a cuisine or ingredients
    if "italian" in user_input.lower():
        st.session_state.conversation.append("Bot: Great! Do you have any specific ingredients in mind?")
    elif "ingredients" in user_input.lower():
        st.session_state.conversation.append("Bot: What ingredients do you have?")
    elif "help" in user_input.lower():
        st.session_state.conversation.append("Bot: I can help you create recipes! Just tell me what cuisine or ingredients you want to use.")
    else:
        st.session_state.conversation.append("Bot: Could you provide more details? For example, the cuisine or ingredients you'd like to use.")

# Submit button for ingredients
if st.button("Submit Ingredients"):
    ingredients = st.text_input("Enter ingredients (comma-separated):")
    if ingredients:
        # Send ingredients to the backend
        response = requests.post(
            f"{API_BASE_URL}/generate_recipe/",
            json={"ingredients": ingredients.split(","), "preferences": {}},
        )
        if response.status_code == 200:
            recipes = response.json().get("recipes", [])
            if recipes:
                st.session_state.conversation.append("Bot: Here are some recipe suggestions:")
                for recipe in recipes:
                    st.session_state.conversation.append(f"- {recipe.get('title', 'Unknown Recipe')}")
            else:
                st.session_state.conversation.append("Bot: Sorry, I couldn't find any recipes with those ingredients.")
        else:
            st.session_state.conversation.append("Bot: There was an error fetching recipes. Please try again later.")
