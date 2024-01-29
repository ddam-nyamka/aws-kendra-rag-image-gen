import streamlit as st
import json
from utils.Kendra import Kendra
from utils.Bedrock import Bedrock
from utils.PromptBase import PromptBase

bedrock = Bedrock()
kendra = Kendra()
prompt_base = PromptBase()

kendra_description = kendra.describe()

try:
    st.title('Chatbot with Kendra RAG Engine')
    st.subheader("Powered by Amazon Bedrock")

    md = f"""
    *Kendra*: **{kendra_description['Name']}**\n
    *Total docs*: **{kendra_description['IndexStatistics']['TextDocumentStatistics']['IndexedTextDocumentsCount']}**\n
    """
    st.markdown(md)
except Exception as e:
    st.error("Kendra not found.")

model_id = st.selectbox(
    'Text Models',
    (
        "anthropic.claude-instant-v1",
        "anthropic.claude-v2"
    )
)
with st.chat_message('assistant'):
    st.markdown("Hello there! How can I assist you today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "kendra_items" not in st.session_state:
    st.session_state.kendra_items = []

for message in st.session_state.messages:
    display_role = 'user'
    if message['role'] == 'Assistant':
        display_role = 'assistant'

    with st.chat_message(display_role):
        st.markdown(message["content"])


def get_history() -> str:
    history = [
        f"{record['role']}: {record['content']}" for record in st.session_state.messages
    ]
    return '\n\n'.join(history)


if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append({"role": "Human", "content": prompt})
    with st.chat_message("Human"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        history = get_history()

        kendra_response = kendra.retrieve(prompt)
        kendra_items = kendra_response.get('ResultItems', [])
        st.session_state.kendra_items = kendra_items

        kendra_items_prompt = []
        for idx, item in enumerate(kendra_items):
            json_item = json.loads(json.dumps(item))
            kendra_items_prompt.append({
                "SourceId": idx,
                "DocumentId": item['DocumentId'],
                "DocumentTitle": item['DocumentTitle'],
                "Content": item['Content']
            })

        assistant_prompt = prompt_base.generate_answer_kendra_prompt(
            kendra_items_prompt
        )
        response = bedrock.answer(history, assistant_prompt, model_id)

        stream = response.get('body')
        if stream:
            for event in stream:
                chunk = event.get('chunk')
                if chunk:
                    full_response += json.loads(chunk.get('bytes').decode())[
                        'completion'] or ""
                    message_placeholder.markdown(full_response + "▌")

    st.session_state.messages.append(
        {"role": "Assistant", "content": full_response}
    )

with st.sidebar:
    st.subheader("History")
    history_list = [
        f"{record['role']}: {record['content'][:50]}..." for record in st.session_state.messages
    ]
    st.write(history_list)

    st.subheader("Found items Kendra:")
    kendra_list = [
        f"{record['DocumentTitle']}: {record['Content'][:50]}..." for record in st.session_state.kendra_items
    ]
    st.write(kendra_list)
