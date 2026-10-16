"""Built-in dictionaries moved from the original main module."""

import re

TOOLS = {
    "automation": [
        ("CrewAI", "https://www.crewai.com/"),
        ("LangChain", "https://www.langchain.com/"),
        ("AutoGen", "https://microsoft.github.io/autogen/"),
        ("Make.com", "https://www.make.com/"),
        ("Zapier", "https://zapier.com/"),
        ("n8n", "https://n8n.io/"),
    ],
    "research": [
        ("Perplexity", "https://www.perplexity.ai/"),
        ("NotebookLM", "https://notebooklm.google.com/"),
        ("Grok", "https://grok.com/"),
        ("Elicit", "https://elicit.com/"),
        ("Consensus", "https://consensus.app/"),
    ],
    "creative": [
        ("Midjourney", "https://www.midjourney.com/"),
        ("Runway", "https://runwayml.com/"),
        ("Gemini", "https://gemini.google.com/"),
        ("ChatGPT", "https://chatgpt.com/"),
        ("Ideogram", "https://ideogram.ai/"),
    ],
        "security": [
        ("OWASP", "https://owasp.org/"),
        ("PortSwigger Academy", "https://portswigger.net/web-security"),
        ("CyberChef", "https://gchq.github.io/CyberChef/"),
    ],
        "productivity": [
        ("Notion", "https://www.notion.so/"),
        ("Obsidian", "https://obsidian.md/"),
        ("Trello", "https://trello.com/"),
    ],
    "development": [
        ("Claude", "https://claude.ai/"),
        ("Cursor", "https://www.cursor.com/"),
        ("GitHub Copilot", "https://github.com/features/copilot"),
        ("Base44", "https://app.base44.com/"),
        ("Lovable", "https://lovable.dev/"),
        ("Replit", "https://replit.com/"),
    ],
}


CATEGORY_KEYWORDS = {
    "automation": {"automation", "agent", "workflow"},
    "research": {"research", "find", "found", "search"},
    "creative": {"create", "image", "video", "design"},
    "development": {"build", "website", "app", "code", "develop"},
    "security": {"security", "cybersecurity", "pentest", "privacy"},
    "productivity": {"productivity", "notes", "planning"},
}


GIT_COMMANDS = {
    "git status": "Shows the current changes in the project.",
    "git add .": "Adds files to the staging area.",
    "git commit": "Saves the staged changes as a commit.",
    "git push": "Uploads local commits to a remote repository such as GitHub.",
    "git pull": "Downloads and integrates the latest remote changes.",
    "git branch": "Shows branches or creates a new branch.",
    "git checkout": "Switches between branches.",
    "git clone": "Copies a remote repository to your computer.",
}


PYTHON_COMMANDS = {
    "range": "range(start, stop, step) creates a sequence of numbers.",
    "len": "len() returns the number of items in an object.",
    "enumerate": "enumerate() gives both the index and value while looping.",
    "zip": "zip() combines values from two or more iterables.",
    "lambda": "lambda creates a small anonymous function in one expression.",
}


JAVA_COMMANDS = {
    "main": "public static void main(String[] args) is the usual entry point of a Java program.",
    "system.out.println": "System.out.println() prints output to the console.",
    "for loop": "A for loop repeats a block of code.",
    "arraylist": "ArrayList is a resizable list implementation in Java.",
    "class": "A class is a blueprint for creating objects.",
}


C_COMMANDS = {
    "main": "int main() is the usual starting point of a C program.",
    "printf": "printf() prints formatted output.",
    "scanf": "scanf() reads formatted input.",
    "pointer": "A pointer stores the memory address of another value.",
    "malloc": "malloc() dynamically allocates memory.",
}

BASH_COMMANDS = {
    "pwd": "Prints the current working directory.",
    "ls": "Lists files and directories.",
    "cd": "Changes the current directory.",
    "mkdir": "Creates a new directory.",
    "grep": "Searches lines for a pattern.",
}

SQL_COMMANDS = {
    "select": "Retrieves rows or columns from a database.",
    "where": "Filters rows that match a condition.",
    "join": "Combines related rows from multiple tables.",
    "group by": "Groups rows for aggregation.",
    "order by": "Sorts the result set.",
}


CPP_COMMANDS = {
    "main": "int main() is the usual starting point of a C++ program.",
    "cout": "std::cout writes output to the console.",
    "cin": "std::cin reads input from the console.",
    "class": "A class is a blueprint for creating objects.",
    "vector": "std::vector is a resizable sequence container.",
}


REFERENCES = {
    "git": GIT_COMMANDS,
    "python": PYTHON_COMMANDS,
    "java": JAVA_COMMANDS,
    "c": C_COMMANDS,
    "c++": CPP_COMMANDS,
    "bash": BASH_COMMANDS,
    "sql": SQL_COMMANDS,
}


CONCEPTS = {
    "git": """
Git is a distributed version control system used to track changes in
source code and other project files.

Git stores project history through commits. This makes it possible to
compare versions, recover older work, and collaborate safely.

Git also supports branches. A branch lets you work on a feature, bug
fix, or experiment without directly changing the main branch.

A common Git workflow is:

1. Change files.
2. Check the changes with git status.
3. Stage changes with git add.
4. Save them with git commit.
5. Share them with git push.

Git can be used without GitHub. GitHub is one platform that can host
Git repositories.

Reference:
https://git-scm.com/docs
""",
    "github": """
GitHub is an online platform for hosting Git repositories and
collaborating on software projects.

Git and GitHub are different. Git is the version control system, while
GitHub is a service that stores Git repositories online and adds
collaboration features.

Common GitHub features include repositories, pull requests, issues,
code reviews, discussions, releases, and GitHub Actions.

Reference:
https://docs.github.com/en/repositories
""",
    "python": """
Python is a high-level, general-purpose programming language known for
its readable syntax and large ecosystem.

Python is used for automation, web development, scripting, data
analysis, scientific computing, backend development, artificial
intelligence, and machine learning.

Popular Python libraries include NumPy, pandas, scikit-learn,
TensorFlow, and PyTorch.

Reference:
https://docs.python.org/3/
""",
    "ai": """
Artificial Intelligence, or AI, is the field of computing focused on
building systems that can perform tasks that normally require forms
of human intelligence.

AI includes areas such as rule-based systems, machine learning, deep
learning, reinforcement learning, computer vision, natural language
processing, speech systems, and generative AI.

Modern AI is heavily based on machine learning, where systems learn
patterns from data.

Generative AI can create text, images, audio, video, and code. Large
language models are one type of generative AI system.

Reference:
https://www.nist.gov/artificial-intelligence
""",
    "ml": """
Machine Learning, or ML, is a part of Artificial Intelligence where
models learn patterns from data and use those patterns to make
predictions or decisions.

Traditional programming:
input + rules -> output

Machine learning:
data + learning algorithm -> trained model

Common types of machine learning include supervised learning,
unsupervised learning, and reinforcement learning.

Reference:
https://developers.google.com/machine-learning
""",
    "machine learning": """
Machine Learning is a subfield of Artificial Intelligence where
computer models learn patterns from data instead of depending only on
manually written rules.

During training, a model changes its parameters to improve performance
on a chosen objective.

Common learning approaches include supervised learning, unsupervised
learning, self-supervised learning, semi-supervised learning, and
reinforcement learning.

Reference:
https://developers.google.com/machine-learning/glossary
""",
    "llm": """
An LLM, or Large Language Model, is a machine learning model trained
on large amounts of data to understand and generate sequences of
tokens.

Many modern LLMs use Transformer architectures. Transformers use
self-attention to model relationships between tokens.

LLMs can be used for writing, summarization, translation, question
answering, classification, coding, information extraction, and tool use.

Reference:
https://developers.google.com/machine-learning/glossary
""",
    "deep learning": """
Deep Learning is a part of machine learning that uses neural networks
with multiple layers.

Those layers allow a model to learn increasingly complex
representations from data.

Deep learning is widely used in computer vision, speech recognition,
natural language processing, recommendation systems, and generative AI.

Reference:
https://developers.google.com/machine-learning/glossary
""",
    "neural network": """
A neural network is a machine learning model made from connected
computational units arranged into layers.

A simple neural network normally contains an input layer, one or more
hidden layers, and an output layer.

During a forward pass, the network produces a prediction. A loss
function measures how far the prediction is from the expected result.

Backpropagation calculates gradients so that model parameters can be
updated.

Reference:
https://developers.google.com/machine-learning/glossary
""",
    "api": """
An API, or Application Programming Interface, is a defined way for one
software system to communicate with another.

An API describes how software can request data or functionality and
what kind of response it should receive.

Web APIs commonly use HTTP methods such as GET, POST, PUT, PATCH, and
DELETE.

Reference:
https://developer.mozilla.org/en-US/docs/Glossary/API
""",
    "prompt engineering": """
Prompt engineering is the process of writing and improving
instructions given to an AI model.

A good prompt explains the task clearly, provides useful context,
and defines the expected output.

Common techniques:
- Clear instructions
- Few-shot examples
- Role prompting
- Output formatting
- Prompt testing and refinement

Prompt engineering is useful when building chatbots,
AI assistants, and LLM-powered applications.
""",
       "embeddings": """
Embeddings are numerical representations of text,
images, or other data.

They help computers compare information based on
meaning rather than exact words.

For example, two sentences with similar meanings
can have similar embedding vectors.

Common uses:
- Semantic search
- Recommendation systems
- Document retrieval
- RAG applications
- Similarity matching
""",
    "rag": """
RAG stands for Retrieval-Augmented Generation.

It is an AI architecture that combines information retrieval with a
generative language model.

A simple RAG pipeline collects documents, splits them into smaller
chunks, indexes them, retrieves relevant information for a question,
and gives that information to a model before generating an answer.

RAG is different from fine-tuning. Fine-tuning changes model
parameters, while RAG supplies external information during inference.

Reference:
https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/
""",
}


CONCEPT_ALIASES = {
    "artificial intelligence": "ai",
    "machine learning": "machine learning",
    "large language model": "llm",
    "large language models": "llm",
    "deep learning": "deep learning",
    "neural network": "neural network",
    "neural networks": "neural network",
    "application programming interface": "api",
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",
    "github": "github",
    "python": "python",
    "git": "git",
    "ai": "ai",
    "ml": "ml",
    "llm": "llm",
    "embedding": "embeddings",
    "embeddings": "embeddings",
    "api": "api",
    "rag": "rag",
}


MATH_PATTERN = re.compile(
    r"^(-?\d+(?:\.\d+)?)\s*([+\-*/%])\s*(-?\d+(?:\.\d+)?)$"
)
