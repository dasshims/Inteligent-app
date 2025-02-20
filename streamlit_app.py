import os

import streamlit as st
from openai import OpenAI
import helper.github_helper as gh
import json

# Show title and description.
st.title("💬Intelligent Chatbot")
st.write("This is an intelligent chatBot to help with your project data."
         "The app is connected with your Jira issues and github data.")

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def read_data(directory="resources"):
    all_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r") as file:
                    data = json.load(file)
                    all_data.append(data)
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

    return all_data

if 'app_initialized' not in st.session_state:
    gh_repos = gh.fetch_github_repos()
    # stored_data = read_data()
    # system_message = "These are the information from Jira, can you remember this: " + str(stored_data)
    # messages = [
    #     {"role": "system", "content": system_message}
    # ]
    #
    # # Call the OpenAI API
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",  # Adjust model as needed
    #     messages=messages
    # )
    #(f"data fed successfully {response.model.title()}")
    st.session_state.app_initialized = True

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stored_data = read_data()
    system_message = "These are the information from Jira and github, can you remember this: " + str(stored_data)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            *[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                ]
        ],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
