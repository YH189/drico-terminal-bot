
# Drico-Bot

Drico-Bot is a Python command-line chatbot and AI tools router.

It helps developers discover useful tools, understand programming concepts, explore command references, and perform simple calculations directly from the terminal.

The project focuses on keeping things simple. Drico uses predefined knowledge, keyword matching, and basic input processing rather than relying on an external AI model.

## Features

Drico includes several built-in features:

- AI tool recommendations
- AI and machine learning concept explanations
- Git command references
- Python references
- Java references
- C references
- C++ references
- Basic arithmetic
- Simple terminal conversations
- Case-insensitive input handling
- Common concept aliases
- Basic punctuation handling
- No external runtime dependencies

Drico is designed to be lightweight and easy to run on Windows, macOS, and Linux.

## Requirements

Before installing Drico, make sure you have:

- Python 3.9 or newer
- pipx
- A working terminal

Check your Python version:

```bash
python --version
```

On some Linux and macOS systems:

```bash
python3 --version
```

## Installation

The recommended way to install Drico-Bot is with `pipx`.

It installs Drico in an isolated Python environment and makes the `drico-bot` command available in your terminal.

### Windows

Install pipx using PowerShell:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Close PowerShell completely and open a new window.

Install Drico:

```powershell
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Start the application:

```powershell
drico-bot
```

### macOS

Install pipx:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal.

Install Drico:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Start Drico:

```bash
drico-bot
```

### Linux

Install pipx if it is not already available.

On Ubuntu, you can use:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

Open a new terminal and install Drico:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Start Drico:

```bash
drico-bot
```

## Getting Started

After installation, launch Drico:

```bash
drico-bot
```

You should see:

```text
--------------------------------------------------
        DRICO - AI TOOLS ROUTER
--------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

User  >
```

You can now interact with Drico directly from the terminal.

Type:

```text
show
```

to see the built-in help menu.

To close Drico:

```text
exit
```

## Core Commands

| Command | Description |
|---------|-------------|
| `automation` | Discover automation tools |
| `research` | Discover research tools |
| `creative` | Discover creative AI tools |
| `development` | Discover development tools |
| `tools` | Display the complete tool directory |
| `links` | Display the complete tool directory |
| `show` | Display the help menu |
| `exit` | Close Drico |
| `quit` | Close Drico |
| `bye` | Close Drico |

Drico also recognizes several alternative words.

For example, these inputs open the development category:

```text
build
website
app
code
develop
```

## AI Tool Directory

Drico contains a built-in directory of tools grouped by their main use cases.

### Automation

Tools available in this category:

- CrewAI
- LangChain
- AutoGen
- Make.com
- Zapier
- n8n

Example:

```text
User  > automation
```

### Research

Tools available in this category:

- Perplexity
- NotebookLM
- Grok
- Elicit
- Consensus

Example:

```text
User  > research
```

### Creative

Tools available in this category:

- Midjourney
- Runway
- Gemini
- ChatGPT
- Ideogram

Example:

```text
User  > creative
```

### Development

Tools available in this category:

- Claude
- Cursor
- GitHub Copilot
- Base44
- Lovable
- Replit

Example:

```text
User  > development
```

## Concept Explanations

Drico includes explanations of several technical concepts.

Core topics include:

- Git
- GitHub
- Python
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Large Language Models
- Neural Networks
- APIs
- Retrieval-Augmented Generation

Example inputs:

```text
what is AI?
what is machine learning?
explain RAG
what is LLM?
what is neural network?
what is API?
tell me about Python
```

Drico recognizes different capitalization styles:

```text
what is ai
what is AI
what is Ai
```

Basic punctuation is also supported:

```text
what is AI?
what is ML?
explain RAG?
```

## Programming References

Drico provides short explanations of commonly used commands and programming concepts.

### Git

Supported Git references include:

```text
git status
git add .
git commit
git push
git pull
git branch
git checkout
git clone
```

Example:

```text
User  > git status

Drico > Searching...
Drico > git status: Shows the current changes in the project.
```

### Python

Supported Python references:

```text
python range
python len
python enumerate
python zip
python lambda
```

### Java

Supported Java references:

```text
java main
java system.out.println
java for loop
java arraylist
java class
```

### C

Supported C references:

```text
c main
c printf
c scanf
c pointer
c malloc
```

### C++

Supported C++ references:

```text
c++ main
c++ cout
c++ cin
c++ class
c++ vector
```

## Calculator

Drico can perform basic arithmetic using two numbers.

Supported operators:

| Operator | Operation |
|----------|-----------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo |

Examples:

```text
12+13
20*4
100/5
9%2
-5+10
```

Example output:

```text
User  > 12+13

Drico > Calculating...
Drico > The result is: 25
```

Division by zero is handled without crashing the application.

```text
User  > 10/0

Drico > Calculating...
Drico > The result is: Error: cannot divide by 0
```

## Example Session

```text
--------------------------------------------------
        DRICO - AI TOOLS ROUTER
--------------------------------------------------

User  > hello

Drico > Hello! How can I help you?

User  > git status

Drico > Searching...
Drico > git status: Shows the current changes in the project.

User  > 5+5

Drico > Calculating...
Drico > The result is: 10

User  > who are you

Drico > I am Drico, a simple Python AI tools router.

User  > exit

Drico > Thanks for using Drico.
```

## How Drico Works

Drico uses a rule-based approach to process user requests.

The application follows a simple workflow:

1. Read the user's terminal input.
2. Normalize the input text.
3. Check whether the input matches a built-in command.
4. Check for supported mathematical expressions.
5. Identify concept questions and aliases.
6. Search programming references.
7. Match keywords to tool categories.
8. Display the corresponding response.

If Drico does not understand a request, it displays a fallback message instead of generating an unsupported answer.

```text
Drico > I don't understand that yet.
Drico > Type 'show' to see what I can do.
```

## Project Structure

The Python package is organized as follows:

```text
drico-terminal-bot/
├── drico_bot/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## CLI Entry Point

The application is launched using the `drico-bot` command.

The entry point in `pyproject.toml` is:

```toml
[project.scripts]
drico-bot = "drico_bot.main:run"
```

This connects the terminal command to the `run()` function inside `drico_bot/main.py`.

Users who install Drico with pipx do not need to manually execute the Python source file.

## Development

Developers can work directly with the source code.

Clone the repository:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
```

Enter the project directory:

```bash
cd drico-terminal-bot
```

Run the application:

```bash
python -m drico_bot.main
```

On Linux or macOS:

```bash
python3 -m drico_bot.main
```

## Updating Drico

To install the latest version from the main branch:

```bash
pipx uninstall drico-bot
```

Then reinstall:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```bash
drico-bot
```

## Troubleshooting

### The drico-bot command is not recognized

Make sure pipx is installed and its application directory is available in your PATH.

On Windows:

```powershell
python -m pipx ensurepath
```

On macOS or Linux:

```bash
pipx ensurepath
```

Restart your terminal and try again.

### An older version of Drico starts

Remove the existing pipx installation:

```bash
pipx uninstall drico-bot
```

If an older pip installation exists, remove that as well.

Windows:

```powershell
python -m pip uninstall drico-bot
```

macOS or Linux:

```bash
python3 -m pip uninstall drico-bot
```

Then reinstall the current version using pipx.

### ImportError: cannot import name run_bot

Older development versions used a different CLI entry point.

The current entry point should reference:

```text
drico_bot.main:run
```

If an older launcher is still installed, remove it and reinstall Drico.

### Repository already exists

If Git reports:

```text
fatal: destination path 'drico-terminal-bot' already exists
```

enter the existing repository instead of cloning it again:

```bash
cd drico-terminal-bot
git pull
```

## Scope

Drico is a rule-based terminal assistant.

It uses:

- Python dictionaries
- Regular expressions
- Keyword matching
- Predefined explanations
- Programming references
- Terminal input and output

Drico currently does not use:

- Large language models
- External AI APIs
- Live web search
- A database
- Autonomous agent workflows

Its responses are based on the information and functionality included in the source code.

## Tech Stack

- Python
- Python Standard Library
- Regular Expressions
- Dictionaries
- Sets
- setuptools
- pyproject.toml

The core application does not require external Python libraries at runtime.

## Contributing

Contributions and suggestions are welcome.

You can fork the repository, make changes, and submit a pull request.

Bug reports and feature requests can also be submitted through GitHub Issues.

## Open Source

Drico-Bot is released under the MIT License.

You can use, modify, and distribute the code according to the license terms.

## License

See the [LICENSE](LICENSE) file for the complete MIT License.
