# Drico-Bot

Drico-Bot is a lightweight command-line tool written in Python that routes queries to useful AI tools, explains common development and AI concepts, provides basic programming references, and handles simple calculations directly from the terminal.

It is a keyword-based CLI program, not a large language model.

## Install

To make `drico-bot` available from anywhere in your terminal, install it with `pipx`.

```bash
pip install --user pipx
python -m pipx ensurepath
```

Close and reopen your terminal, then install Drico-Bot:

```bash
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

After installation, run:

```bash
drico-bot
```

## Commands

Type `show` inside Drico at any time to display the available commands.

| Input                                         | What Drico does                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `automation`, `agent`, `workflow`             | Shows automation tools such as CrewAI, LangChain, AutoGen, Zapier, Make.com, and n8n        |
| `research`, `find`, `found`, `search`         | Shows research tools such as Perplexity, NotebookLM, Grok, Elicit, and Consensus            |
| `create`, `image`, `video`, `design`          | Shows creative AI tools such as Midjourney, Runway, Gemini, ChatGPT, and Ideogram           |
| `build`, `website`, `app`, `code`, `develop`  | Shows development tools such as Claude, Cursor, GitHub Copilot, Base44, Lovable, and Replit |
| `git status`, `git push`, etc.                | Explains supported Git commands                                                             |
| `python lambda`, `python range`, etc.         | Explains supported Python references                                                        |
| `java class`, `c pointer`, `c++ vector`, etc. | Explains supported Java, C, and C++ references                                              |
| `what is ai`                                  | Explains a supported concept                                                                |
| `explain machine learning`                    | Explains a supported concept                                                                |
| `12+13`, `20 * 4`, `9 % 2`                    | Performs basic arithmetic                                                                   |
| `list`, `tools`, `links`                      | Displays the complete AI tool directory                                                     |
| `hi`, `hello`                                 | Greets the user                                                                             |
| `how are you`                                 | Returns a simple response                                                                   |
| `who are you`                                 | Explains what Drico is                                                                      |
| `exit`, `quit`, `bye`                         | Closes the program                                                                          |

## Supported Concepts

Drico currently includes explanations for:

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

Examples:

```text
what is ai
what is github
what is machine learning
explain deep learning
what is neural network
what is api
what is rag
```

## Programming References

Drico also contains a small built-in reference for common programming commands and concepts.

### Git

Supported examples include:

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

### Python

Supported topics include:

```text
python range
python len
python enumerate
python zip
python lambda
```

### Java

Supported topics include:

```text
java main
java system.out.println
java for loop
java arraylist
java class
```

### C

Supported topics include:

```text
c main
c printf
c scanf
c pointer
c malloc
```

### C++

Supported topics include:

```text
c++ main
c++ cout
c++ cin
c++ class
c++ vector
```

## Calculator

Drico supports basic arithmetic expressions containing two numbers.

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

Division and modulo by zero are handled safely instead of crashing the program.

## Example Session

```text
------------------------------------------------------------
        DRICO - AI TOOLS ROUTER
------------------------------------------------------------
Type 'show' to see the available commands.
Type 'exit' to close the program.

User  > what is ai
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

User  > build a website
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

Drico does not generate answers using an AI model.

Instead, it uses simple Python logic to:

1. Read input from the terminal.
2. Normalize the input.
3. Check for built-in commands.
4. Match supported concepts and programming references.
5. Detect basic mathematical expressions.
6. Match keywords to AI tool categories.
7. Return a predefined response or tool directory.

If Drico cannot understand a query, it responds without guessing:

```text
Drico > I don't understand that yet.
Drico > Type 'show' to see what I can do.
```

## Scope

Drico is intentionally small and predictable.

It currently provides:

* AI tool routing
* AI and development concept explanations
* Git command references
* Python references
* Java references
* C references
* C++ references
* basic arithmetic
* simple conversational commands

It does not use an LLM, external API, database, or internet search to generate answers.

Its responses come from the information stored directly in the program.

## Tech

* Python
* Python standard library
* Regular expressions
* Command-line interface
* Keyword matching
* Dictionary-based routing

The core program has no external runtime dependencies.

## Project Structure

```text
drico-terminal-bot/
├── drico.py
├── pyproject.toml
└── README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/YH189/drico-terminal-bot.git
cd drico-terminal-bot
```

Run Drico directly:

```bash
python drico.py
```

For development installation:

```bash
pip install -e .
```

Then:

```bash
drico-bot
```

## License

See the repository license for usage terms.
