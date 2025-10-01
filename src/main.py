from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from langchain_core.runnables import RunnableConfig
from graph import graph

config: RunnableConfig = {"configurable": {"thread_id": "1"}}


def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]}, config=config
    ):
        for value in event.values():
            value["messages"][-1].pretty_print()


if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
            current_state_snapshot = graph.get_state(config)
        except Exception:
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
