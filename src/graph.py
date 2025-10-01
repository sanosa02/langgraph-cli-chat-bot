import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agents.chat_agent import chatbot
from state import State
from tools.search_tool import search_tool


# создаём (или открываем) файл базы данных
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)

# инициализируем чекпоинтер
memory = SqliteSaver(conn)

graph_builder = StateGraph(State)

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[search_tool]))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)
