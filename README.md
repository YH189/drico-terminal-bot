# Drico-Bot

A command-line chatbot that routes your queries to the right AI tools, does quick math, explains dev concepts, and answers basic dev-reference questions — right from your terminal.

## Install

Want `drico-bot` available anytime, just by typing it?

```bash
pip install --user pipx
pipx install git+https://github.com/YH189/drico-terminal-bot.git
```

> Restart your terminal after installing, then run:
> ```bash
> drico-bot
> ```

## Run

```
drico-bot
```

## What it can do

Type `show` inside the bot at any time to see this list again.

| You type | What happens |
|---|---|
| `automation`, `agent`, `workflow` | Shows automation tool links (CrewAI, LangChain, n8n, etc.) |
| `research`, `found` | Shows research tool links (Perplexity, NotebookLM, etc.) |
| `create`, `image`, `video` | Shows creative tool links (Midjourney, Runway, etc.) |
| `build`, `website`, `app`, `code` | Shows dev tool links (Claude, Cursor, Copilot, etc.) |
| `git status`, `python lambda`, etc. | Explains a specific git / Python / Java / C / C++ command |
| `what is git`, `what is the use of python`, etc. | Explains a broader concept — git, github, python, ai, ml, llm, deep learning, neural network, api, rag |
| `12+13`, `20 * 4`, `9 % 2` | Calculates the result — no spacing required |
| `list`, `tools`, `links` | Shows the full tool directory |
| `hi`, `hello` | Says hello |
| `who are you` | Explains what Drico is |
| `bye`, `exit`, `quit` | Closes the bot |

Before answering most queries, Drico shows a short "Researching... Analysing... Finalising..." sequence to make the terminal feel more alive.

## Example session

```
User  > what is the use of git
Drico > Researching...
Drico > Analysing...
Drico > Finalising...
Drico > Git is a version control system that tracks changes to your code over time and lets you collaborate without overwriting each other's work.

User  > git status
Drico > Researching...
Drico > Analysing...
Drico > Finalising...
Drico > git status: Shows the current changes in the project.

User  > 12+13
Drico > Researching...
Drico > Analysing...
Drico > Finalising...
Drico > The result is: 25.0

User  > build a website
Drico > Researching...
Drico > Analysing...
Drico > Finalising...
Drico > These tools may be useful:

Claude - https://claude.ai/
Cursor - https://www.cursor.com/
...

User  > exit
Drico > Thanks for using Drico.
```

## Scope

Drico is a keyword-matching CLI tool, not an LLM. It answers what's in its dictionaries — git/Python/Java/C/C++ command references, a small set of AI/ML concept explanations, tool links, and basic math. For anything outside that, it says so plainly instead of guessing.

## Tech

Pure Python, no external dependencies. Packaged with `pyproject.toml` for `pip install -e .`.

