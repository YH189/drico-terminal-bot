# ChatBot Router

A command-line chatbot built in Python that responds to user input using keyword matching — no machine learning or LLMs involved, purely conditional logic.

## What it does

- Recognizes basic greetings and simple questions
- Detects intent based on keywords (e.g. automation, research, image/video creation, coding) and recommends relevant AI tools with links based on the query
- Performs basic math operations
- Exits gracefully on "bye" or "exit"

## How it works

The bot checks the user's input against a series of keyword conditions (`if`/`elif`) and prints a matching response. If no keyword matches, it returns a fallback message.

## Example

---------Rule Based ChatBot---------
User > hello
Bot > How can I assist you today?
User > I want to build a website
Bot > By analyzing your query, it appears to be software development:

Claude: https://claude.ai/
Cursor: https://www.cursor.com/
GitHub Copilot: https://github.com/features/copilot
User > bye
Bot > Thank you for utilizing the system. Goodbye.
