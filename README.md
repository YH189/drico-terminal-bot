# Drico-Bot

Drico-Bot is a lightweight Python command-line chatbot and AI tools router.

It can recommend useful AI tools, explain selected AI and development concepts, provide small programming references, and perform basic arithmetic directly from the terminal.

Drico is intentionally simple and predictable. It does not use an LLM, external AI API, database, or live web search to generate its answers.

## Features

- AI tool recommendations
- AI and machine learning concept explanations
- Git command references
- Python references
- Java references
- C references
- C++ references
- Basic arithmetic
- Simple terminal conversations
- Case-insensitive concept matching
- Common concept aliases
- Basic punctuation handling
- No external runtime dependencies

## Requirements

Drico-Bot requires:

- Python 3.8 or newer
- pipx

Check your Python version:

```bash
python --version
```

On some macOS and Linux systems:

```bash
python3 --version
```

## Installation

The recommended way to install Drico-Bot is with `pipx`.

`pipx` installs Drico in an isolated Python environment and makes the `drico-bot` command available from your terminal.

### Windows

Install `pipx`:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Close PowerShell completely and open a new PowerShell window.

Install Drico-Bot:

```powershell
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```powershell
drico-bot
```

### macOS

Install `pipx`:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal.

Install Drico-Bot:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```bash
drico-bot
```

### Linux

Install `pipx`:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal.

Install Drico-Bot:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```bash
drico-bot
```

## Start Drico

After installation, start Drico with:

```bash
drico-bot
```

You should see:

```text
------------------------------------------------------------
        DRICO - AI TOOLS ROUTER
------------------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

User  >
```

Normal users do not need to manually run `main.py`.

## Update Drico-Bot

If Drico is already installed and you want the latest version:

```bash
pipx uninstall drico-bot
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Then run:

```bash
drico-bot
```

This replaces the previous isolated installation with the latest version from the repository.

## Upgrading From an Older Version

Older development versions of Drico used a different command-line entry point.

If you see an error similar to:

```text
ImportError: cannot import name 'run_bot' from 'drico_bot.main'
```

an older Drico launcher is still installed.

Remove the old pipx installation:

```bash
pipx uninstall drico-bot
```

Also remove any older pip installation:

```bash
python -m pip uninstall drico-bot
```

On macOS or Linux:

```bash
python3 -m pip uninstall drico-bot
```

Then install the current version:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```bash
drico-bot
```

The current CLI entry point is:

```toml
[project.scripts]
drico-bot = "drico_bot.main:run"
```

## Commands

Type:

```text
show
```

inside Drico at any time to display the available commands.

| Input | What Drico does |
|---|---|
| `automation`, `agent`, `workflow` | Shows automation tools |
| `research`, `find`, `found`, `search` | Shows research tools |
| `create`, `image`, `video`, `design` | Shows creative AI tools |
| `build`, `website`, `app`, `code`, `develop` | Shows development tools |
| `git status`, `git push`, etc. | Explains supported Git commands |
| `python lambda`, `python range`, etc. | Explains supported Python references |
| `java class`, `java arraylist`, etc. | Explains supported Java references |
| `c pointer`, `c malloc`, etc. | Explains supported C references |
| `c++ vector`, `c++ cout`, etc. | Explains supported C++ references |
| `what is ai` | Explains Artificial Intelligence |
| `what is ml` | Explains Machine Learning |
| `what is rag` | Explains Retrieval-Augmented Generation |
| `12+13`, `20 * 4`, `9 % 2` | Performs basic arithmetic |
| `list`, `tools`, `links` | Shows the complete tool directory |
| `hi`, `hello` | Greets the user |
| `how are you` | Returns a simple response |
| `who are you` | Explains what Drico is |
| `exit`, `quit`, `bye` | Closes Drico |

## AI Tool Categories

### Automation

Drico can suggest:

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

Drico can suggest:

- Perplexity
- NotebookLM
- Grok
- Elicit
- Consensus

Examples:

```text
User  > research
User  > find
User  > search
```

### Creative

Drico can suggest:

- Midjourney
- Runway
- Gemini
- ChatGPT
- Ideogram

Examples:

```text
User  > create
User  > image
User  > video
User  > design
```

### Development

Drico can suggest:

- Claude
- Cursor
- GitHub Copilot
- Base44
- Lovable
- Replit

Examples:

```text
User  > build
User  > website
User  > code
User  > develop
```

## Supported Concepts

Drico currently includes explanations for:

- Git
- GitHub
- Python
- Artificial Intelligence
- Machine Learning
- Large Language Models
- Deep Learning
- Neural Networks
- APIs
- Retrieval-Augmented Generation

Examples:

```text
what is ai
what is AI
what is AI?
what is artificial intelligence
what is ml
what is ML
what is machine learning
what is the use of AI
what is llm
what is large language model
what is deep learning
what is neural network
what is api
what is rag
explain RAG
tell me about neural networks
```

Drico handles capitalization differences such as:

```text
what is ai
what is AI
what is Ai
```

Basic trailing punctuation is also supported:

```text
what is AI?
what is ML?
explain RAG?
```

## Programming References

Drico includes small built-in references for several programming languages and development tools.

### Git

Supported Git commands include:

```text
git status
git add
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

Supported Python topics include:

```text
python range
python len
python enumerate
python zip
python lambda
```

### Java

Supported Java topics include:

```text
java main
java system.out.println
java for loop
java arraylist
java class
```

### C

Supported C topics include:

```text
c main
c printf
c scanf
c pointer
c malloc
```

### C++

Supported C++ topics include:

```text
c++ main
c++ cout
c++ cin
c++ class
c++ vector
```

## Calculator

Drico supports basic arithmetic using two numbers.

Supported operators:

```text
+
-
*
/
%
```

Examples:

```text
12+13
20 * 4
100 / 5
9 % 2
-5 + 10
```

Example:

```text
User  > 12+13
Drico > Calculating...
Drico > The result is: 25
```

Division by zero is handled safely:

```text
User  > 10/0
Drico > Calculating...
Drico > The result is: Error: cannot divide by 0
```

Modulo by zero is also handled without crashing the application.

## Example Session

```text
------------------------------------------------------------
        DRICO - AI TOOLS ROUTER
------------------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

User  > hi
Drico > Hello! How can I help you?

User  > what is AI
Drico > Searching...
Drico > Artificial Intelligence, or AI, is the field of computing focused on
building systems that can perform tasks that normally require forms
of human intelligence.

User  > what is ML
Drico > Searching...
Drico > Machine Learning, or ML, is a part of Artificial Intelligence where
models learn patterns from data and use those patterns to make
predictions or decisions.

User  > git status
Drico > Searching...
Drico > git status: Shows the current changes in the project.

User  > 12+13
Drico > Calculating...
Drico > The result is: 25

User  > build
Drico > Searching...

Drico > Development tools

Claude - https://claude.ai/
Cursor - https://www.cursor.com/
GitHub Copilot - https://github.com/features/copilot
Base44 - https://app.base44.com/
Lovable - https://lovable.dev/
Replit - https://replit.com/

User  > exit
Drico > Thanks for using Drico.
```

## How Drico Works

Drico uses straightforward Python routing rather than a language model.

When you enter a command, Drico:

1. Reads terminal input.
2. Normalizes the text.
3. Checks built-in commands.
4. Detects supported arithmetic expressions.
5. Matches supported concepts and aliases.
6. Checks programming references.
7. Matches keywords to AI-tool categories.
8. Returns a predefined response.

If Drico does not recognize an input, it does not invent an answer.

Example:

```text
Drico > I don't understand that yet.
Drico > Type 'show' to see what I can do.
```

## Project Structure

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

The terminal command is configured in `pyproject.toml`:

```toml
[project.scripts]
drico-bot = "drico_bot.main:run"
```

This connects:

```bash
drico-bot
```

to the `run()` function inside:

```text
drico_bot/main.py
```

Normal users do not need to manually locate or run `main.py`.

## Development

This section is for developers or contributors working directly with the source code.

Clone the repository:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
```

Enter the repository:

```bash
cd drico-terminal-bot
```

Run the source:

```bash
python -m drico_bot.main
```

On macOS or Linux:

```bash
python3 -m drico_bot.main
```

Run this command from inside the repository when testing source code.

Normal users should install Drico with `pipx` and start it with:

```bash
drico-bot
```

## Troubleshooting

### `drico-bot` is not recognized on Windows

Run:

```powershell
python -m pipx ensurepath
```

Then close PowerShell completely and open a new PowerShell window.

Try:

```powershell
drico-bot
```

If Drico has not been installed yet:

```powershell
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

### `drico-bot: command not found` on macOS or Linux

Run:

```bash
python3 -m pipx ensurepath
```

Close and reopen your terminal.

Then run:

```bash
drico-bot
```

### `run_bot` ImportError

If you see:

```text
ImportError: cannot import name 'run_bot' from 'drico_bot.main'
```

an older Drico launcher is still installed.

Remove old installations:

```bash
pipx uninstall drico-bot
```

Then:

```bash
python -m pip uninstall drico-bot
```

On macOS or Linux:

```bash
python3 -m pip uninstall drico-bot
```

Install the latest version:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Then run:

```bash
drico-bot
```

The current launcher uses:

```text
drico_bot.main:run
```

not:

```text
drico_bot.main:run_bot
```

### An old version of Drico starts

Remove both possible installations:

```bash
pipx uninstall drico-bot
python -m pip uninstall drico-bot
```

On macOS or Linux:

```bash
pipx uninstall drico-bot
python3 -m pip uninstall drico-bot
```

Then reinstall:

```bash
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Run:

```bash
drico-bot
```

### Windows has multiple Drico commands

In PowerShell, check:

```powershell
Get-Command drico-bot -All
```

Remove old installations:

```powershell
pipx uninstall drico-bot
python -m pip uninstall drico-bot
```

Reinstall Drico:

```powershell
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
```

Close PowerShell, open it again, and run:

```powershell
drico-bot
```

### Repository already exists

If you see:

```text
fatal: destination path 'drico-terminal-bot' already exists and is not an empty directory
```

do not clone it again.

Enter the existing repository:

```bash
cd drico-terminal-bot
```

Then update it:

```bash
git pull
```

## Clean Reinstall

If you are unsure which version of Drico is installed, perform a clean reinstall.

### Windows

```powershell
pipx uninstall drico-bot
python -m pip uninstall drico-bot
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
drico-bot
```

### macOS or Linux

```bash
pipx uninstall drico-bot
python3 -m pip uninstall drico-bot
pipx install https://github.com/YH189/drico-terminal-bot/archive/refs/heads/main.zip
drico-bot
```

## Scope

Drico is intentionally small and predictable.

It uses:

- predefined AI tool directories
- predefined concept explanations
- predefined programming references
- keyword matching
- concept aliases
- regular expressions
- simple arithmetic

Drico does not:

- use an LLM
- browse the internet
- call external AI APIs
- use a database
- generate unrestricted answers
- guess answers for unsupported queries

## Tech

Drico-Bot is built with:

- Python
- Python standard library
- Regular expressions
- Dictionaries
- Sets
- Command-line input/output
- setuptools
- pyproject.toml

The core application has no external runtime dependencies.

## Contributing

Contributions are welcome.

You can fork the repository, make changes in your own copy, and open a pull request.

Changes to the original repository are only made when they are reviewed and accepted.

## Open Source

Drico-Bot is an open-source project released under the MIT License.

You are free to use, study, modify, and distribute the code under the terms of the license.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
