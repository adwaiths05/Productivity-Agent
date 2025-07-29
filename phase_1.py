import sqlite3
import streamlit as st
import requests
from crewai import Agent, Task, Crew
from crewai_tools import tool
from datetime import datetime

# Replace with your Notion API token and database ID
NOTION_TOKEN = "YOUR_NOTION_API_TOKEN"
NOTION_DB_ID = "YOUR_NOTION_DATABASE_ID"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, energy TEXT, priority TEXT)")
    conn.commit()
    conn.close()

# Mock Grok 3 API (replace with xAI API: https://x.ai/api)
def mock_grok_api(prompt):
    prompt = prompt.lower()
    if "add" in prompt:
        task = prompt.split("add", 1)[1].strip() if len(prompt.split("add", 1)) > 1 else None
        if not task:
            return {"action": "clarify", "message": "What task would you like to add?"}
        energy_map = {"coding": "high", "meeting": "high", "email": "low", "reading": "low", "study": "medium"}
        energy = next((e for k, e in energy_map.items() if k in task.lower()), "medium")
        return {"action": "add", "task": task, "energy": energy}
    elif "view" in prompt:
        return {"action": "view"}
    return {"action": "unknown", "message": "Try 'add' or 'view'."}

# Task Manager Tool
@tool("Task Manager")
def task_manager(action: str, task: str = None, energy: str = None) -> str:
    """Manages tasks in SQLite."""
    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()
    
    if action == "add" and task:
        priority = "medium"  # Default, will be dynamic in later phases
        cursor.execute("INSERT INTO tasks (name, energy, priority) VALUES (?, ?, ?)", 
                      (task, energy, priority))
        conn.commit()
        conn.close()
        return f"Added task: {task} (Energy: {energy})"
    elif action == "view":
        cursor.execute("SELECT name, energy, priority FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        return [(t[0], t[2], t[1]) for t in tasks] or ["No tasks."]
    conn.close()
    return "Invalid action."

# Notion Sync Tool
@tool("Notion Sync")
def notion_sync(tasks: list) -> str:
    """Syncs tasks to Notion database."""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    for task_name, priority, energy in tasks:
        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "Task": {"title": [{"text": {"content": task_name}}]},
                "Priority": {"select": {"name": priority}},
                "Energy": {"select": {"name": energy}},
                "Date": {"rich_text": [{"text": {"content": datetime.now().strftime("%Y-%m-%d")}}]}
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Failed to sync: {response.text}"
    return f"Synced {len(tasks)} tasks to Notion"

# Agents
parser_agent = Agent(
    role="Input Parser",
    goal="Parse user input for task actions.",
    tools=[],
    llm=mock_grok_api
)

task_manager_agent = Agent(
    role="Task Manager",
    goal="Manage tasks and sync to Notion.",
    tools=[task_manager, notion_sync]
)

# Streamlit UI
def main():
    st.title("Productivity AI Agent - Phase 1")
    init_db()
    
    user_input = st.text_input("Enter command (e.g., 'Add task: Write report', 'View tasks')")
    if st.button("Submit"):
        parsed = mock_grok_api(user_input)
        if parsed["action"] == "clarify":
            st.write(parsed["message"])
        elif parsed["action"] == "add":
            result = task_manager(parsed["action"], task=parsed["task"], energy=parsed["energy"])
            st.write(result)
        elif parsed["action"] == "view":
            tasks = task_manager(parsed["action"])
            st.write("Task List:")
            for task, priority, energy in tasks:
                st.write(f"{task} (Priority: {priority}, Energy: {energy})")
            notion_result = notion_sync(tasks)
            st.write(notion_result)

if __name__ == "__main__":
    main()
