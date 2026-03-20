# SkillBridge AI 🎯

SkillBridge is an Agentic Career & Learning Intelligence Platform that bridges the gap between what you build (via GitHub), what employers need (Job Market Demand), and what we teach (NCCU Course Catalog). 

This project uses a multi-agent system powered by CrewAI to automatically analyze your public GitHub repositories, map your skills to your target career goal, and create a personalized learning roadmap. 

## Requirements

- **Python Version**: Recommended `3.12` or older (specifically tested with `Python 3.12.10`).
- **OpenAI API Key**: Used by the AI agents for analysis.
- **GitHub Personal Access Token**: Used to fetch your public GitHub repositories.

## Setup Instructions

### 1. Create a Virtual Environment

It is highly recommended to use a virtual environment (`.venv`) to manage the project dependencies.

```bash
# Navigate to the project directory
cd path_to_project/skillbridge

# Create the virtual environment using Python 3.12
py -3.12 -m venv .venv (**Note** : using CrewAI requires no newer than Python 3.12 )
# Or using standard python
python -m venv .venv

# Activate the virtual environment (Windows)
.\.venv\Scripts\activate
```

### 2. Install Dependencies

Once your virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables (`.env`)

You will need to provide your API keys to run the agents. Create a `.env` file within the `skillbridge` directory (you can copy the structure from the provided `.env.example`) and add your keys:

```ini
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_personal_access_token_here
```

*(Note: If you do not have a `.env` file configured, the app allows you to securely enter your OpenAI API key directly from the Streamlit sidebar before running the analysis).*

## How to Run

Launch the interactive dashboard using Streamlit with the following command:

```bash
streamlit run app.py
```

This will automatically open your default browser to `http://localhost:8501/`. 

### Using the App:
1. Enter a **GitHub Profile URL**.
2. Enter a **Career Goal** (e.g., Software Engineer, Data Scientist).
3. Click the **Run SkillBridge Analysis** button to let the multi-agent AI framework start! Check the terminal for background process outputs (such as repository links).
