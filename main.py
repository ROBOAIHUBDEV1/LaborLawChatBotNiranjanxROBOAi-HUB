



import streamlit as st

import google.generativeai as genai
import openai

import time
import os

openai.api_key  = os.getenv('OPENAI_API_KEY')
ligeminiapi= os.getenv('ligeminiapi')
st.title("Trial Chatbot on Labour Laws for MBA students : NIRANJAN X ROBOAi HUB")
st.text("Disclaimer: Please note that the provided links may not always be up-to-date or accessible. We recommend consulting a qualified lawyer for official legal advice tailored to your specific situation.")

# Initialize ChatNVIDIA client

# Initialize session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ""

# Track if the page was just reloaded
if "last_reload_time" not in st.session_state:
    st.session_state.last_reload_time = time.time()  # Set to current time on first load

# If it's been a fresh page load or reload (since we set the last reload time), reset the chat history
if time.time() - st.session_state.last_reload_time < 2:  # 2 seconds window for considering it as a reload
    st.session_state.messages = []
    st.session_state.memory = ""

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Initialize Google Gemini client
genai.configure(api_key=ligeminiapi)  # Replace with your actual API key for Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit title and chat history initialization

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Step 1: Get case-related information from Google Gemini
    case_query = f"""  You are an AI designed to assist with labor law inquiries, and your task is to provide users with relevant data, including legal case details and references. When a user asks for information regarding a specific labor law case or similar legal issues, do the following:

    Provide the necessary data first – Summarize the core details or relevant information about the case(s) requested, including the main legal points, rulings, or precedents.

    Follow with relevant document links and resources – After the data, include links to trusted, up-to-date resources such as legal databases, court rulings, official government publications, law journals, or similar authoritative websites. Ensure the links are valid, reliable, and lead directly to the relevant documents or case summaries.

    Do not reject the query – If the case or legal issue is available online, proceed with retrieving the relevant data and links, even if there are multiple results. Only reject queries if no relevant information is accessible or the topic is outside your legal jurisdiction.

    Formatting – Present the information in the following order:
        First, the summarized data.
        Then, a list of links to relevant resources, formatted as clickable hyperlinks, for easy access to the full documents or case information. {prompt}
.  """# also links having similar cases links and url must be there "
    gemini_response = model.generate_content(case_query)
    case_data = gemini_response.text.strip()  # Collect the case-related links and data
    reshaped_data = case_data


    openai_response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the desired model, e.g., gpt-3.5-turbo or gpt-4
        messages=[
            {"role": "system", "content": """You are an AI chatbot designed to assist with labor law inquiries, known as "the Labor Law Chatbot by Niranjan x ROBOAi HUB." When responding to a user's question, if the topic pertains to specific labor law cases or legal precedents, you should include links to relevant documents or case studies (such as court rulings, legal articles, or case summaries) that provide further context. Your responses should remain clear, professional, and helpful, guiding the user to the most relevant and reliable resources for their queries. Make sure to ensure that the links you provide are accurate and up-to-date.boundaries limit to the indian labor laws. now answer the query . """},
            {"role": "user", "content": case_query},
        ],
        temperature=0.2,
        max_tokens=1024,
        top_p=0.7,
    )    
    reshaped_data = openai_response['choices'][0]['message']['content'].strip()
    # Step 2: Process the case-related data through NVIDIA Nemotron for reshaping

    
    # Step 3: Display reshaped data as assistant response
    with st.chat_message("system"):
        st.markdown(reshaped_data)
    
    # Add assistant reshaped response to chat history
    st.session_state.messages.append({"role": "system", "content": reshaped_data})
