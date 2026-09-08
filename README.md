# Drico-Bot

Drico-Bot is a lightweight command-line chatbot written in Python.

It routes simple queries to useful AI tools, explains selected AI and development concepts, provides small programming references, and performs basic arithmetic directly from the terminal.

Drico is intentionally simple and predictable. It does not use an LLM, external AI API, database, or web search to generate its answers.

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

On some macOS or Linux systems, use:

```bash
python3 --version
```

## Installation

The recommended installation method is `pipx`.

`pipx` installs Drico-Bot in its own isolated Python environment and makes the `drico-bot` command available from your terminal.

### Windows

Install pipx:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Close PowerShell or Command Prompt completely and open it again.

Then install Drico-Bot:

```powershell
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Run Drico:

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

Install Drico-Bot:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Run:

```bash
drico-bot
```

### Linux

Install pipx:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal.

Install Drico-Bot:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
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

Normal users should use this command to launch the program.

You should see:

```text
------------------------------------------------------------
        DRICO - AI TOOLS ROUTER
------------------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

User  >
```

## Update Drico-Bot

If you already have Drico installed and want the latest version from GitHub, remove the old installation first:

```bash
pipx uninstall drico-bot
```

Then install the newest version:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Start it again:

```bash
drico-bot
```

This prevents an older installed copy from being used after the project has been updated.

## Important for Previous Versions

If you previously installed an older version of Drico using `pip`, editable installation, or `pipx`, remove the old installation before installing the current version.

First try:

```bash
pipx uninstall drico-bot
```

Then remove any old pip installation:

```bash
python -m pip uninstall drico-bot
```

On macOS or Linux, if your system uses `python3`:

```bash
python3 -m pip uninstall drico-bot
```

Then install the latest release:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Run:

```bash
drico-bot
```

## Commands

Type:

```text
show
```

inside Drico at any time to display the command list.

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

Drico can suggest tools such as:

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

Drico normalizes capitalization before matching concepts.

For example:

```text
what is ai
what is AI
what is Ai
```

are treated as the same concept.

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

Example:

```text
User  > python lambda
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

1. Reads the terminal input.
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

Drico-Bot uses a command-line entry point defined in `pyproject.toml`:

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

This section is only for contributors or developers changing Drico's source code.

Clone the repository:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
```

Enter the repository:

```bash
cd drico-terminal-bot
```

Confirm that the project contains:

```text
drico_bot/
pyproject.toml
README.md
LICENSE
```

Then run the source:

```bash
python -m drico_bot.main
```

On systems where Python is available as `python3`:

```bash
python3 -m drico_bot.main
```

The module command should be run from inside the repository when testing source code.

Normal users should not use the module command. They should install Drico with `pipx` and run:

```bash
drico-bot
```

## Verify Which Source Is Running

This section is mainly useful for development or troubleshooting.

From inside the repository, run:

```bash
python -c "import drico_bot.main as m; print(m.__file__)"
```

The path should point to your current repository, for example:

```text
C:\Users\your-name\drico-terminal-bot\drico_bot\main.py
```

If it points to an older Python `site-packages` location, remove the old installation and reinstall Drico.

## Troubleshooting

### `drico-bot` command is not found

Close and reopen your terminal after running:

```bash
python -m pipx ensurepath
```

If necessary, run:

```bash
python -m pipx ensurepath
```

again and restart the terminal.

### An old version of Drico starts

Remove previous installations:

```bash
pipx uninstall drico-bot
```

Also check for an old pip installation:

```bash
python -m pip uninstall drico-bot
```

Then install the newest version:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Run:

```bash
drico-bot
```

### Windows shows multiple `drico-bot` commands

In PowerShell, run:

```powershell
Get-Command drico-bot -All
```

Remove old Drico installations, then reinstall using pipx:

```powershell
pipx uninstall drico-bot
python -m pip uninstall drico-bot
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

Then restart PowerShell and run:

```powershell
drico-bot
```

### macOS or Linux shows an old command

Check where the command is coming from:

```bash
which drico-bot
```

Remove the old installation:

```bash
pipx uninstall drico-bot
python3 -m pip uninstall drico-bot
```

Then reinstall:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
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

If you are unsure which Drico version is installed, use a clean reinstall.

Windows:

```powershell
pipx uninstall drico-bot
python -m pip uninstall drico-bot
pipx install git+https://github.com/YH189/drico-terminal-bot.git
drico-bot
```

macOS or Linux:

```bash
pipx uninstall drico-bot
python3 -m pip uninstall drico-bot
pipx install git+https://github.com/YH189/drico-terminal-bot.git
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

The core program has no external runtime dependencies.

## Contributing

If you want to modify Drico locally:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
cd drico-terminal-bot
```

Make your changes, then test:

```bash
python -m drico_bot.main
```

Check the repository:

```bash
git status
```

Commit changes:

```bash
git add .
git commit -m "your commit message"
git push
```

## License

See the `LICENSE` file in this repository for usage terms.
