from flask import Flask, request, jsonify, render_template, Blueprint, current_app
import asyncio
from mcp_use import MCPClient, MCPAgent
from langchain_openai import ChatOpenAI
import os
import logging


from pathlib import Path

# Path to the current file
BASE_DIR = Path(__file__).resolve().parent

# Database path
DB_PATH = BASE_DIR / "volunteers.db"



# ----------------------------------------
# CONFIGURATION
# ----------------------------------------

# Enable detailed logs for debugging
logging.basicConfig(level=logging.INFO)

# MCP Configuration (ensure this path and server are correct)
MCP_CONFIG = {
    "mcpServers": {
        "sqlite": {
            "command": "npx",
            "args": [
                "-y",
                "@executeautomation/database-server",
#                str(DB_PATH)
                r"C:\Users\Administrator\Desktop\volunteersAI\volunteers.db"
            ]
        }
    }
}

# Global agent variable
agent = None


# ----------------------------------------
# AGENT SETUP
# ----------------------------------------

def setup_agent():
    """Initialize the MCP + OpenAI Agent once globally."""
    global agent
    if agent is not None:
        return

    current_app.logger.info("🧠 Initializing MCP Agent with OpenAI LLM...")

    # Initialize MCP client
    client = MCPClient.from_dict(MCP_CONFIG)

    # Initialize OpenAI LLM (ChatGPT-4 / GPT-4o)
    llm = ChatOpenAI(
        model="gpt-4o",  # or "gpt-4-turbo" for cheaper/faster
        temperature=0.0,
        openai_api_key="",
    )

    # Create the MCP Agent with a strong factual system prompt
    system_prompt = """
You are a helpful assistant that answers questions based on a SQLite database of volunteers.

You can query the database through the SQLite MCP tool.

Your goal is to give accurate answers that reflect real data in the database.

When a user question mentions any possible value 
(e.g., a volunteer’s name, email, city, skill, or any text)
that might exist in the 'volunteers' table, 
ALWAYS run an SQLite query to verify whether it exists.

Examples:
- "volunteers from Mumbai" → SELECT * FROM volunteers WHERE current_place_of_residence LIKE '%Mumbai%';
- "volunteers skilled in Python" → SELECT * FROM volunteers WHERE my_skillset LIKE '%Python%';
- "tell me more about Pankaj" → SELECT * FROM volunteers WHERE name LIKE '%Pankaj%';
- "who registered recently" → SELECT * FROM volunteers ORDER BY created_at DESC LIMIT 5;

Do not decide based on your own knowledge of what values exist — 
always query the database to find out.

If a database query returns results, use them to answer clearly and naturally.
If a database query runs successfully but returns no matching rows,
then respond:
"I'm not sure about that based on the available data."

Never guess or fabricate data — but when in doubt, always query first.

You are connected to a database named 'volunteers.db' containing this table:

TABLE: volunteers
-------------------------------------------------
submission_id INTEGER PRIMARY KEY
name TEXT
email TEXT
phone TEXT
current_place_of_residence TEXT
my_skillset TEXT
field_1c8f11d TEXT
form_name_id TEXT
created_at TEXT
user_id INTEGER
user_agent TEXT
user_ip TEXT
referrer TEXT
-------------------------------------------------

"""

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt,
    )

    current_app.logger.info("✅ MCP Agent setup complete.")


# ----------------------------------------
# CHAT HANDLER
# ----------------------------------------

def answer_query(user_input: str):
    """Run the user query through the MCP agent."""
    try:
        if not user_input.strip():
            return {"reply": "No input received."}

        setup_agent()  # ensure agent is ready

        # Force the model to use the database tool explicitly
        final_query = f"""
Always verify your response using the SQLite MCP tool before answering.
Question: {user_input}
"""

        result = asyncio.run(agent.run(final_query))

        if isinstance(result, dict):
            reply = result.get("output") or str(result)
        else:
            reply = str(result)

        current_app.logger.info(f"🧩 Final reply: {reply}")
        return {"reply": reply}

    except Exception as e:
        error_message = f"{type(e).__name__}: {str(e)}"
        current_app.logger.error(f"❌ Error during agent execution: {error_message}")
        return {"reply": "Database connection error or internal issue."}


# ----------------------------------------
# FLASK BLUEPRINT
# ----------------------------------------

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chatpage")
def chatPage():
    return render_template("chat.html")

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from frontend."""
    data = request.get_json()
    user_input = data.get("message", "").strip()

    current_app.logger.info(f"📥 Received user input: {user_input}")
    response = answer_query(user_input)
    current_app.logger.info(f"📤 Sending response: {response}")

    return jsonify(response)
