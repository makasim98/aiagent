# Test AI Agent
A simple project used to explore and build a toy version of an AI agent (akin to Cursor/Zed agentic mode) using the free tier of Google Gemini. <br>
It is restricted to run inside a predefined working directory ```./calculator```, which is a simple CLI calculator ap, and can manage its files using pre-programmed function calls:

## Available calls to the AI agent:
- List the content of directories
- Read the contents of a given file
- Run a python script at a given path
- Write to a file at a given path

## Running the Agent
To run and play around with it, follow the follwing procedure:

### Requirements
- Python 3 installed
- UV package manager installed
    * You can skip this if you will install required dependencies manually specified in ```uv.lock``` file

### Install
1. Clone the ```main``` branch of the project repository
2. Create a VENV for the uv project and activate it
    1. Create a VENV with ```uv venv``` when inside project directory
    2. Activate the virtual environment with ```source .venv/bin/activate```
3. Create a ```.env``` file and provide and API key to Gemeni to the ```GEMINI_API_KEY``` variable. you can create one [here](https://aistudio.google.com/prompts/new_chat)
4. Run the agent with ```uv run main.py "your-prompt-here" [--verbose]``` will automatically install all required packages before prompting the agent.

### Notes
- Inside ```config.py``` the constant ```WORKING_DIR``` defines the directory the agent can work with relative the directory you run the program from. You can redefine it but BE EXTREMELY CAREFUL as the agent can do anything to the contents of that directory.
    - __Example:__ If launching this program from ```/home/user/``` the agent can do anything in ```/home/user/<WORKING_DIR>/```

