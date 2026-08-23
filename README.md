# Drico-Bot

A command-line chatbot that routes your queries to the right AI tools, does quick math, and answers basic questions — right from your terminal.

## Install

```bash
git clone https://github.com/YH189/Drico-Bot.git
cd Drico-Bot
pip install -e .
```

## Run

```bash
drico-bot
```

That's it. Once installed, `drico-bot` works from any folder, any terminal.

## Example

```text
--------------- ChatBot Router ---------------
User > hello
Bot > How can I assist you today?
User > I want to build a website
Bot > By analyzing your query, it appears to be software development:
- Claude: https://claude.ai/
- Cursor: https://www.cursor.com/
- GitHub Copilot: https://github.com/features/copilot
User > 12 / 3
Bot > The result is: 4.0
User > bye
Bot > Thank you for utilizing the system. Goodbye.
```

## What it can do

- Route your query to relevant AI tools (automation, research, creative, dev)
- Basic math (`12 / 3`, with spaces between numbers and the operator)
- Greetings and small talk
- Exit anytime with `bye` or `exit`

