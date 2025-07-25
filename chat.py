from flask import Flask, request, jsonify, render_template, Blueprint, current_app

#imported flask related packages.



import sqlite3
import os
import asyncio





from mcp_use import MCPClient, MCPAgent
from langchain_groq import ChatGroq # Changed from langchain_openai import ChatOpenAI









# MCP Config
MCP_CONFIG = {
    "mcpServers": {
        "sqlite": {
            "command": "npx",
            "args": [
                "-y",
                "@executeautomation/database-server",
                "D:\\pythonFiles\\python_restart\\chat_to_AI\\flask_apps\\projects\\team1\\complete_project\\VAsmartAssisstent\\webinar_registration.db"
            ]
        }
    }
}

# Load Agent once
agent = None
def setup_agent():
    global agent
    if agent is None:
        client = MCPClient.from_dict(MCP_CONFIG)
        # Changed from ChatOpenAI to ChatGroq
        # Choose a Groq model. 'llama-3.3-70b-versatile' is a strong option for complex tasks,
        # 'llama-3.1-8b-instant' is faster for simpler tasks.
        # Ensure GROQ_API_KEY is set in your .env file or environment variables.
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile", # Using a powerful Groq model
            # Groq API key is typically loaded from the environment variable GROQ_API_KEY
            # You can explicitly pass it if needed, but using os.getenv is recommended.
            groq_api_key = "your api key hear." #os.getenv("GROQ_API_KEY") # No need for a placeholder like "sk-..."
        )
        agent = MCPAgent(llm=llm, client=client, max_steps=10)

setup_agent()

# Chat function
def answer_query(user_input):
    try:
        if not user_input.strip():
            return {"reply":"no input found"}

        result = asyncio.run(agent.run(user_input))
        return {"reply": result}
    except Exception as e:
        import traceback
        return {"reply":e}



chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chatpage")
def chatPage():
    return render_template("chat.html")  # ✅ Loads HTML from templates/



@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()


    user_input = data.get("message", "")
    current_app.logger.info(f"the recieved data  is: {user_input}")

    response = answer_query(user_input)
    current_app.logger.info(f"the response back to server is: {response}")
    return jsonify(response)
