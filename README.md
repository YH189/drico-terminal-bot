# Drico-Bot

A command-line chatbot that routes your queries to the right AI tools, does quick math, and answers basic dev-reference questions — right from your terminal.

## Install

```
git clone https://github.com/YH189/drico-terminal-bot.git
cd drico-terminal-bot
pip install -e .
```

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
| `git status`, `what is git`, etc. | Explains a git command |
| `python lambda`, `what is enumerate`, etc. | Explains a Python keyword |
| `java main`, `c pointer`, `c++ vector`, etc. | Explains a Java / C / C++ keyword |
| `12+13`, `20 * 4`, `9 % 2` | Calculates the result — no spacing required |
| `list`, `tools`, `links` | Shows the full tool directory |
| `hi`, `hello` | Says hello |
| `who are you` | Explains what Drico is |
| `bye`, `exit`, `quit` | Closes the bot |


## Tech

Pure Python, no external dependencies. Packaged with `pyproject.toml` for `pip install -e .`.

