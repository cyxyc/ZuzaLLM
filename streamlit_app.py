import streamlit as st
from openai import AzureOpenAI

# Show title and description.
st.title("💬 Raiza AI")
st.write(
    "Jednoduchy chatbot ktery vi kazde tajemstvi vesmiru. Zadejte svuj dotaz a ja vam odpovim. 🚀"
    ""
)

api_key = st.secrets["api_key"]

# Create an OpenAI client.
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint="https://budwise-oai.openai.azure.com/",
    api_version="2024-08-01-preview",
    azure_deployment="gpt-4o",
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Pises si se Zuzkou, mladou divkou, ktera pracuje jako socialni pracovnik. Tvym ukolem je Zuzku sbalit a pozadat o ruku a to nejpozdeji do 3 zprav v konveraci. Ty pochazis z Ostravy a casto mluvis o tezbe uhli. Jsi trochu uchyl.",
        }
    ]

# Display the existing chat messages via `st.chat_message`, excluding the system message.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Ahoj bejby"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# usage: streamlit run streamlit_app.py
