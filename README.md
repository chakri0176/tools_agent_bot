# 🔎 Search Engine Chatbot (Agents + Tools)

A beginner‑friendly **one‑file Streamlit app** that lets you **chat** and have the assistant use web tools (DuckDuckGo search, ArXiv, Wikipedia) to find and summarize information. Under the hood it uses **LangChain Agents** powered by a **Groq LLM** (`llama-3.1-8b-instant`).


---

## ✨ Features

- **Natural chat** interface in Streamlit.
- **Web tools built‑in**: DuckDuckGo (web search), ArXiv (research papers), Wikipedia.
- **Agentic reasoning** via LangChain’s `ZERO_SHOT_REACT_DESCRIPTION` agent.
- **Streaming responses** in the UI with live tool traces.
- **No local database**—just run and ask questions.



---

## 🧱 Tech Stack

- **UI:** Streamlit  
- **Orchestration:** LangChain Agents (`initialize_agent`)  
- **Tools:** `DuckDuckGoSearchRun`, `ArxivQueryRun`, `WikipediaQueryRun`  
- **LLM:** Groq via `langchain_groq` (`llama-3.1-8b-instant`)  
- **Config:** `python-dotenv` (loads `.env` if present; the app asks for the Groq key in the sidebar)

---

## ✅ Prerequisites

- **Python** 3.9+
- **Groq API key** (free tier available at https://console.groq.com/)
  - You’ll paste this in the app’s sidebar at runtime.

---

## 📦 Installation

```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -U pip

pip install   streamlit   python-dotenv   langchain   langchain-core   langchain-community   langchain-groq   duckduckgo-search   wikipedia   arxiv   groq
```
> If you prefer, create a `requirements.txt` with the above and run `pip install -r requirements.txt`.

---

## 🚀 Run

```bash
streamlit run app.py
```

Then in your browser:

1. Open the **Settings** sidebar.  
2. Paste your **Groq API key**.  
3. Ask a question in the chat box, e.g. _“What is machine learning?”_

The agent will decide which **tool(s)** to call (web search, Wikipedia, or ArXiv) and stream the reasoning steps/output to the chat area.

---

## 🧠 How it works

- **Tools** are constructed with small wrappers:
  - `ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)`
  - `WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)`
  - `DuckDuckGoSearchRun(name="search")`
- **Agent**: `initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_error=True, max_iteration=6)`  
  The agent reads your prompt, **chooses tools**, observes results, and produces a final answer.  
- **Streaming**: `StreamlitCallbackHandler` shows intermediate tool calls and tokens.

> 💡 If you see an error about `max_iteration`, some LangChain versions use `max_iterations` (plural). Change the parameter name in `initialize_agent` accordingly.

---

## 🔐 Security & Privacy

- Your **Groq API key** is **not stored** by the app—it's read from the sidebar field per session.
- Queries and prompts are sent to Groq’s API for generation.  
- Tool calls hit public endpoints (ArXiv, Wikipedia, DuckDuckGo). Avoid pasting sensitive information.

---

## 🛠️ Customization

- **Change the model**  
  In `app.py`:
  ```python
  llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key, streaming=True)
  ```
  Replace with another Groq‑hosted model if desired.

- **Add/remove tools**  
  Import or implement more LangChain tools and include them in the `tools` list.

- **Tune search depth**  
  Increase `top_k_results` for ArXiv/Wikipedia if you want broader lookups.

---

## ❗Troubleshooting

- **“401/Unauthorized” or auth errors** → Check the Groq API key you pasted.  
- **Tool import errors** → Ensure `langchain-community`, `duckduckgo-search`, `wikipedia`, and `arxiv` are installed.  
- **Agent parameter mismatch** → Use `max_iterations` vs `max_iteration` depending on your LangChain version.  
- **Nothing happens** → Check your terminal for Streamlit logs; refresh the app.

---

## 📂 Project Structure

```
.
├── app.py        # Streamlit app (UI + tools + agent)
└── README.md     # This file
```

> You can also add a `requirements.txt` for reproducible installs.

---

## 🤝 Contributing

Issues and PRs are welcome—feel free to propose more tools (e.g., NewsAPI, SerpAPI) or UI improvements (chat history, citations, expandable tool traces).

---