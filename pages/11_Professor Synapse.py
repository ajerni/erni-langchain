import streamlit as st
from langchain.agents import AgentExecutor, ConversationalChatAgent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.tools import DuckDuckGoSearchRun

from synapse_prompt import sprompt

import os
os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

def initialize_page():
    st.set_page_config(
        page_title="LangChain: Chat with search", 
        page_icon="🦜",
        layout="wide"
    )

    st.title(":parrot: LangChain: Chat with search", anchor=False)

def handle_messages(messages, steps):
    avatars = {"human": "user", "ai": "assistant"}
    for idx, msg in enumerate(messages):
        with st.chat_message(avatars[msg.type]):
            # Render intermediate steps if any were saved
            for step in steps.get(str(idx), []):
                if step[0].tool == "_Exception":
                    continue
                with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                    st.write(step[0].log)
                    st.write(f"{step[1]}")
            st.write(msg.content)

def get_prompt():
    return st.chat_input(placeholder="use /start /new /save etc.")

def handle_chat(prompt, openai_api_key, msgs, memory):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", 
        openai_api_key=openai_api_key, 
        streaming=True)
    tools = [DuckDuckGoSearchRun(name="Search")]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(
            st.container(), 
            expand_new_thoughts=False, 
            collapse_completed_thoughts=False)
        response = executor(prompt, callbacks=[st_cb])
        st.write(response["output"])
        return response["intermediate_steps"]

# Initializing the app
initialize_page()
st.info("Powered by GPT-3.5-turbo and DuckDuckGo search, this chatbot provides real-time answers, accurate search results, and remembers past conversations.", icon="💡")
openai_api_key = st.secrets['openai_api_key']
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, 
    return_messages=True, 
    memory_key="chat_history", 
    output_key="output")

if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

handle_messages(msgs.messages, st.session_state.steps)
prompt = get_prompt()

sp = '''
Act as Professor Synapse 🧙🏾‍♂️, a conductor of expert agents. Your job is to support the user in accomplishing their goals by aligning with their goals and preference, then calling upon an expert agent perfectly suited to the task by initializing "Synapse_COR" = "\${emoji}: I am an expert in \${role}. I know \${context}. I will reason step-by-step to determine the best course of action to achieve \${goal}. I can use \${tools} to help in this process

I will help you accomplish your goal by following these steps:
${reasoned steps}

My task ends when ${completion}.

${first step, question}."

Follow these steps:
1. 🧙🏾‍♂️, Start each interaction by gathering context, relevant information and clarifying the user’s goals by asking them questions
2. Once user has confirmed, initialize “Synapse_CoR”
3. 🧙🏾‍♂️ and the expert agent, support the user until the goal is accomplished

Commands:\n
/start - introduce yourself and begin with step one \n
/save - restate SMART goal, summarize progress so far, and recommend a next step \n
/reason - Professor Synapse and Agent reason step by step together and make a recommendation for how the user should proceed \n
/settings - update goal or agent \n
/new - Forget previous input \n

Rules:
- End every output with a question or a recommended next step
- List your commands in your first output or if the user asks
- 🧙🏾‍♂️, ask before generating a new agent
'''

st.chat_message("user").write(sp)
st.session_state.steps[str(len(msgs.messages) - 1)] = handle_chat(sp, openai_api_key, msgs, memory)

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.steps[str(len(msgs.messages) - 1)] = handle_chat(prompt, openai_api_key, msgs, memory)