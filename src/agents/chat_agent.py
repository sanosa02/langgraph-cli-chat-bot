from langchain.chat_models import init_chat_model
import os

from state import State
from tools.search_tool import search_tool

llm = init_chat_model(
    os.getenv("LLM_MODEL"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

llm_with_tools = llm.bind_tools([search_tool])


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
