from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calcAdd(a: float, b:float) -> str:
    """useful for performing basic arithmetic calculations with numbers"""
    print("ClacAdd Tool is called")
    return f"Sum of {a} and {b} is {a + b}"

@tool
def calcSub(a: float, b:float) -> str:
    """useful for performing basic arithmetic calculations with numbers"""
    print("CalcSub Tool is called")
    return f"Subtrcation of {a} and {b} is {a - b}"

@tool
def travel_info(info: str) -> str:
    """"Useful for getting info about places"""
    print("Travel Tool is called")
    return f"{info}"

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calcAdd, calcSub, travel_info]
    agent_executor = create_react_agent(model, tools)

    print("Welcome, I am your AI assistant, Type 'quit' to exit.")
    print("You can request travel info and basic arithmetic calculation of numbers")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistance: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()
    

if __name__ == "__main__":
    main()
