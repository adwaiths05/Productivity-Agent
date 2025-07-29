# Productivity AI Agent - Phase 1

A beginner-friendly AI agent for task management, syncing tasks to a Notion database. Built with CrewAI, Streamlit, SQLite, and Notion API, it assigns energy levels to tasks and lays the foundation for energy-based prioritization and productivity enhancement.

---

## Features

- **Add tasks** with automatic energy level assignment (high, medium, low).
- **View tasks** with energy and priority details.
- **Sync tasks to a Notion database.**
- **Simple web interface via Streamlit.**

---

## Tech Stack

- **Python:** Core scripting.
- **CrewAI:** Agent orchestration.
- **Streamlit:** Web UI.
- **SQLite:** Task storage.
- **Notion API:** Sync tasks to Notion.
- **requests:** API calls.

---

## Prerequisites

- Python 3.8+
- Notion account with API token and database
- Git (optional, for cloning)

---

## Setup Instructions

### 1. Clone the Repository (if hosted on GitHub)
```bash
git clone https://github.com/your-repo/productivity-agent.git
cd productivity-agent
```

### 2. Install Dependencies
```bash
pip install streamlit crewai crewai-tools sqlite3 requests
```

### 3. Set Up Notion

- Go to [Notion Integrations](https://www.notion.so/my-integrations) and create an integration to get your API token.
- Create a Notion database with columns:
  - **Task** (Title)
  - **Priority** (Select)
  - **Energy** (Select)
  - **Date** (Text)
- Share the database with your integration.
- Get the **Database ID** from the Notion URL (e.g., `https://www.notion.so/your-workspace/DATABASE_ID?v=...`).
- Update `NOTION_TOKEN` and `NOTION_DB_ID` in `phase1_productivity_agent.py`.

### 4. Run the Application
```bash
streamlit run phase1_productivity_agent.py
```

---

## Usage

- Open the Streamlit app in your browser (default: [http://localhost:8501](http://localhost:8501)).
- Enter commands:
  - **Add tasks:**  
    `Add task: Write report`
  - **View tasks:**  
    `View tasks`

- Tasks are saved in SQLite and synced to Notion.

---

## Project Structure

- `phase1_productivity_agent.py`: Main script with task management and Notion sync.
- `productivity.db`: SQLite database (auto-created) for task storage.

---

## Next Steps

- **Phase 2:** Add end-of-day survey for task feedback and energy inference.
- **Phase 3:** Implement dynamic task prioritization and lifestyle suggestions.
- **Phase 4:** Add machine learning for continuous improvement and external API integration (e.g., productivity articles).

---

## Notes

- Replace the mock LLM with Grok 3 (xAI API: https://x.ai/api) for real parsing.
- Ensure Notion API token has read/write access to the database.
- For issues, check Notion API response logs or Streamlit console.

---

## License

MIT License
