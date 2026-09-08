Drico-Bot

Drico-Bot is a lightweight command-line chatbot written in Python.

It routes queries to useful AI tools, explains a small set of AI and development concepts, provides programming references, and performs basic arithmetic directly from the terminal.

Drico is a keyword-based CLI tool. It does not use an LLM, external AI API, database, or internet search to generate answers.

Features

AI tool routing

AI and machine learning concept explanations

Git command references

Python references

Java references

C references

C++ references

Basic arithmetic

Simple terminal conversations

Case-insensitive concept matching

Concept aliases

Basic punctuation handling

No external runtime dependencies

Requirements

Python 3.8 or newer

pipx

Install

Install pipx if it is not already available:

python -m pip install --user pipx
python -m pipx ensurepath

Close and reopen your terminal after running ensurepath.

Install Drico-Bot directly from GitHub:

pipx install git+https://github.com/YH189/drico-terminal-bot.git

Run Drico:

drico-bot

After installation, drico-bot is the normal command you should use to start the program.

Update

If Drico-Bot is already installed and you want to install the latest version from GitHub:

pipx uninstall drico-bot
pipx install git+https://github.com/YH189/drico-terminal-bot.git

Then run:

drico-bot

Reinstalling ensures that an older installed copy is replaced by the current repository version.

Commands

Type show inside Drico to display the available commands.

Input

What Drico does

automation, agent, workflow

Shows automation tools

research, find, found, search

Shows research tools

create, image, video, design

Shows creative AI tools

build, website, app, code, develop

Shows development tools

git status, git push, etc.

Explains supported Git commands

python lambda, python range, etc.

Explains supported Python references

java class, java arraylist, etc.

Explains supported Java references

c pointer, c malloc, etc.

Explains supported C references

c++ vector, c++ cout, etc.

Explains supported C++ references

what is ai

Explains Artificial Intelligence

what is ml

Explains Machine Learning

what is rag

Explains Retrieval-Augmented Generation

12+13, 20 * 4, 9 % 2

Performs basic arithmetic

list, tools, links

Shows the complete tool directory

hi, hello

Greets the user

how are you

Returns a simple response

who are you

Explains what Drico is

exit, quit, bye

Closes Drico

AI Tool Categories

Automation

Drico can suggest:

CrewAI

LangChain

AutoGen

Make.com

Zapier

n8n

Example:

User  > automation

Research

Drico can suggest:

Perplexity

NotebookLM

Grok

Elicit

Consensus

Examples:

User  > research
User  > search
User  > find

Creative

Drico can suggest:

Midjourney

Runway

Gemini

ChatGPT

Ideogram

Examples:

User  > image
User  > video
User  > design

Development

Drico can suggest:

Claude

Cursor

GitHub Copilot

Base44

Lovable

Replit

Examples:

User  > build
User  > website
User  > code

Supported Concepts

Drico currently includes explanations for:

Git

GitHub

Python

Artificial Intelligence

Machine Learning

Large Language Models

Deep Learning

Neural Networks

APIs

Retrieval-Augmented Generation

Examples:

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

Drico normalizes capitalization and basic trailing punctuation before matching supported concepts.

Programming References

Git

Supported commands include:

git status
git add
git commit
git push
git pull
git branch
git checkout
git clone

Example:

User  > git status
Drico > Searching...
Drico > git status: Shows the current changes in the project.

Python

Supported topics include:

python range
python len
python enumerate
python zip
python lambda

Java

Supported topics include:

java main
java system.out.println
java for loop
java arraylist
java class

C

Supported topics include:

c main
c printf
c scanf
c pointer
c malloc

C++

Supported topics include:

c++ main
c++ cout
c++ cin
c++ class
c++ vector

Calculator

Drico supports basic arithmetic with two numbers.

Supported operators:

+
-
*
/
%

Examples:

12+13
20 * 4
100 / 5
9 % 2
-5 + 10

Example:

User  > 12+13
Drico > Calculating...
Drico > The result is: 25

Division by zero is handled without crashing:

User  > 10/0
Drico > Calculating...
Drico > The result is: Error: cannot divide by 0

Example Session

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

How It Works

Drico uses straightforward Python routing rather than an AI model.

The program:

Reads terminal input.

Normalizes the text.

Checks built-in commands.

Detects supported arithmetic expressions.

Matches supported concept aliases.

Checks programming references.

Matches AI-tool category keywords.

Returns a predefined response.

If Drico does not recognize an input, it does not invent an answer:

Drico > I don't understand that yet.
Drico > Type 'show' to see what I can do.

Project Structure

drico-terminal-bot/
├── drico_bot/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── README.md
└── LICENSE

Package Entry Point

The command-line executable is configured in pyproject.toml:

[project.scripts]
drico-bot = "drico_bot.main:run"

This makes:

drico-bot

run the run() function from drico_bot/main.py.

Development

This section is only for contributors working on the source code.

Clone the repository:

git clone https://github.com/YH189/drico-terminal-bot.git

Enter the repository before running the source:

cd drico-terminal-bot

Run the current source directly:

python -m drico_bot.main

Do not run the module command from an unrelated directory because Python may find a separately installed copy of the package instead of the repository source.

Normal users should install Drico with pipx and start it with:

drico-bot

Scope

Drico is intentionally small and predictable.

It uses:

predefined AI tool directories

predefined concept explanations

predefined programming references

keyword matching

concept aliases

regular expressions

simple arithmetic

It does not:

use an LLM

browse the web

call external AI APIs

generate unrestricted answers

use a database

guess unknown answers

Tech

Python

Python standard library

Regular expressions

Dictionaries

Sets

Command-line input/output

setuptools

pyproject.toml

The core application has no external runtime dependencies.
