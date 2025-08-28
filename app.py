import streamlit as st
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
from langchain.agents import initialize_agent,AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

#Title 
st.title("🔎Search Engine Using Tools and Agents")

#Using Arxiv and Wikipedia as search engine tools for this project
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

#Search Engine
search = DuckDuckGoSearchRun(name="search")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API key",type="password")

if api_key:
    #If you never explicitly set st.session_state["messages"], then by default it doesn’t exist.
    #That’s why the code checks if it’s missing — to initialize it before using it.
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role":"assistant","content":"Hi, I am a Search engine chatbot who can search the Web!!"}
        ]
        
    for msgs in st.session_state.messages:
        st.chat_message(msgs["role"]).write(msgs["content"])
        
    if prompt:=st.chat_input(placeholder="What is machine learning?"):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").write(prompt)
        
        #llm model
        llm = ChatGroq(model_name="llama-3.1-8b-instant",groq_api_key=api_key,streaming=True)
        
        #tools
        tools = [search,arxiv,wiki]
        
        search_agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_error=True,max_iteration=6)
        
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            
            response = search_agent.run(prompt,callbacks=[st_cb])
            
            st.session_state.messages.append({"role":"assistant","content":response})
            
            st.write(response)
