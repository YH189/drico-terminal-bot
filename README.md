# Drico-Bot

Drico-Bot is a lightweight command-line chatbot written in Python.

It can route queries to useful AI tools, explain common AI and development concepts, provide small programming references, and perform basic calculations directly from the terminal.

Drico is a keyword-based CLI tool. It does not use an LLM or external AI API to generate responses.

## Features

Drico currently supports:

* AI tool recommendations
* AI and machine learning concept explanations
* Git command references
* Python references
* Java references
* C references
* C++ references
* Basic arithmetic
* Simple conversational commands
* Case-insensitive concept matching
* Common question variations
* Basic punctuation handling

## Installation

The recommended way to install Drico-Bot is with `pipx`.

Install pipx:

```bash
pip install --user pipx
python -m pipx ensurepath
```

Close and reopen your terminal after running `ensurepath`.

Then install Drico-Bot directly from GitHub:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

After installation, run:

```bash
drico-bot
```

## Install From a Local Clone

Clone the repository:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
cd drico-terminal-bot
```

Install the package normally with pipx:

```bash
pipx install .
```

Then run:

```bash
drico-bot
```

This installs Drico as a normal package.

It does not use editable installation mode.

## Run Without Installing

If you are developing or testing Drico locally, you can run it directly from the repository:

```bash
python -m drico_bot.main
```

You do not need to run:

```bash
pip install -e .
```

for normal development testing.

## Commands

Type:

```text
show
```

inside Drico at any time to display the command list.

| Input                                        | What Drico does                         |
| -------------------------------------------- | --------------------------------------- |
| `automation`, `agent`, `workflow`            | Shows automation tools                  |
| `research`, `find`, `found`, `search`        | Shows research tools                    |
| `create`, `image`, `video`, `design`         | Shows creative AI tools                 |
| `build`, `website`, `app`, `code`, `develop` | Shows development tools                 |
| `git status`, `git push`, etc.               | Explains supported Git commands         |
| `python lambda`, `python range`, etc.        | Explains supported Python references    |
| `java class`, `java arraylist`, etc.         | Explains supported Java references      |
| `c pointer`, `c malloc`, etc.                | Explains supported C references         |
| `c++ vector`, `c++ cout`, etc.               | Explains supported C++ references       |
| `what is ai`                                 | Explains Artificial Intelligence        |
| `what is ml`                                 | Explains Machine Learning               |
| `what is rag`                                | Explains Retrieval-Augmented Generation |
| `12+13`, `20 * 4`, `9 % 2`                   | Performs basic arithmetic               |
| `list`, `tools`, `links`                     | Shows the complete AI tool directory    |
| `hi`, `hello`                                | Greets the user                         |
| `how are you`                                | Returns a simple response               |
| `who are you`                                | Explains what Drico is                  |
| `exit`, `quit`, `bye`                        | Closes the program                      |

## AI Tool Categories

### Automation

Drico can recommend:

* CrewAI
* LangChain
* AutoGen
* Make.com
* Zapier
* n8n

Example:

```text
User  > automation
```

### Research

Drico can recommend:

* Perplexity
* NotebookLM
* Grok
* Elicit
* Consensus

Examples:

```text
User  > research
User  > search
User  > find
```

### Creative

Drico can recommend:

* Midjourney
* Runway
* Gemini
* ChatGPT
* Ideogram

Examples:

```text
User  > create
User  > image
User  > video
User  > design
```

### Development

Drico can recommend:

* Claude
* Cursor
* GitHub Copilot
* Base44
* Lovable
* Replit

Examples:

```text
User  > build
User  > website
User  > code
User  > develop
```

## Supported Concepts

Drico currently understands explanations for:

* Git
* GitHub
* Python
* Artificial Intelligence
* Machine Learning
* Large Language Models
* Deep Learning
* Neural Networks
* APIs
* Retrieval-Augmented Generation

### Examples

```text
what is ai
what is ml
what is machine learning
what is the use of ai
what is github
what is python
what is llm
what is deep learning
what is neural network
what is api
what is rag
```

Drico also accepts other supported question styles:

```text
explain rag
tell me about neural networks
what is the use of ai
what are the uses of machine learning
```

Concept matching is case-insensitive, so these are treated the same:

```text
what is AI
what is ai
what is Ai
```

Basic punctuation is also handled:

```text
what is AI?
what is ML?
explain RAG?
```

## Programming References

Drico includes a small built-in development reference.

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

Drico includes a small arithmetic calculator.

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

Example output:

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

Modulo by zero is also handled safely.

## Example Session

```text
------------------------------------------------------------
        DRICO - AI TOOLS ROUTER
------------------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

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

User  > what is the use of AI
Drico > Searching...
Drico > Artificial Intelligence, or AI, is the field of computing focused on
building systems that can perform tasks that normally require forms
of human intelligence.

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

User  > who are you
Drico > I am Drico, a simple Python AI tools router.

User  > exit
Drico > Thanks for using Drico.
```

## How It Works

Drico uses straightforward Python logic instead of an AI model.

The program:

1. Reads input from the terminal.
2. Normalizes the text to lowercase.
3. Removes simple trailing punctuation.
4. Checks built-in commands.
5. Detects arithmetic expressions.
6. Matches supported concept names and aliases.
7. Looks for programming references.
8. Matches keywords to AI tool categories.
9. Returns a predefined response.

For unsupported input, Drico does not guess.

It responds with:

```text
Drico > I don't understand that yet.
Drico > Type 'show' to see what I can do.
```

## Concept Matching

Drico uses aliases to recognize different ways of referring to supported concepts.

Examples include:

```text
AI
Artificial Intelligence

ML
Machine Learning

LLM
Large Language Model

API
Application Programming Interface

RAG
Retrieval-Augmented Generation
```

This allows queries such as:

```text
what is AI
what is artificial intelligence
what is ML
what is machine learning
what is LLM
what is large language model
what is API
what is application programming interface
what is RAG
```

## Project Structure

```text
drico-terminal-bot/
│
├── drico_bot/
│   ├── __init__.py
│   └── main.py
│
├── pyproject.toml
├── README.md
└── LICENSE
```

## Package Entry Point

The command-line executable is configured in `pyproject.toml`:

```toml
[project.scripts]
drico-bot = "drico_bot.main:run"
```

This connects the terminal command:

```bash
drico-bot
```

to the `run()` function inside:

```text
drico_bot/main.py
```

## Updating a Local Clone

If the repository is already cloned, do not clone it again.

Open the existing repository:

```powershell
cd C:\Users\your-name\drico-terminal-bot
```

Then pull the latest changes:

```bash
git pull
```

Run the latest source directly:

```bash
python -m drico_bot.main
```

## Reinstalling the CLI

If Drico was installed previously and you want the terminal command to use the newest code:

```bash
pipx uninstall drico-bot
pipx install .
```

Then run:

```bash
drico-bot
```

For the GitHub version:

```bash
pipx uninstall drico-bot
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

## Scope

Drico is intentionally small and predictable.

It is not intended to behave like ChatGPT or another large language model.

Drico only answers using:

* predefined AI tool directories
* predefined concept explanations
* predefined programming references
* keyword matching
* concept aliases
* simple arithmetic

It does not:

* generate new AI responses
* browse the internet
* call external AI APIs
* use a database
* use an LLM
* guess answers for unknown queries

## Tech

Drico is built with:

* Python
* Python standard library
* Regular expressions
* Dictionaries
* Sets
* Command-line input/output
* Keyword matching
* Alias-based concept matching
* `setuptools`
* `pyproject.toml`

The core program has no external runtime dependencies.

## Requirements

* Python 3.8 or newer
* pipx recommended for global CLI installation

## Development

Run directly:

```bash
python -m drico_bot.main
```

Check repository status:

```bash
git status
```

After making changes:

```bash
git add .
git commit -m "your commit message"
git push
```

## License

See the `LICENSE` file in this repository for usage terms.
