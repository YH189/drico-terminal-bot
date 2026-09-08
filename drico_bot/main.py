import re
import time

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
    "automation": ["automation", "agent", "workflow"],
    "research": ["research", "find", "found", "search"],
    "creative": ["create", "image", "video", "design"],
    "development": ["build", "website", "app", "code", "develop"],
}

GIT_COMMANDS = {
    "git status": "Shows the current changes in the project.",
    "git add": "Adds files to the staging area.",
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

Git can be used without GitHub. GitHub is only one platform that can
host Git repositories.

Reference:
https://git-scm.com/docs
""",

    "github": """
GitHub is an online platform for hosting Git repositories and
collaborating on software projects.

Git and GitHub are different. Git is the version control system, while
GitHub is a service that stores Git repositories online and adds
collaboration features.

Common GitHub features include:

- repositories
- pull requests
- issues
- code reviews
- discussions
- releases
- GitHub Actions

A common workflow is:

1. Create or clone a repository.
2. Create a branch.
3. Make changes.
4. Commit the changes.
5. Push the branch.
6. Open a pull request.
7. Review and merge the changes.

Reference:
https://docs.github.com/en/repositories
""",

    "python": """
Python is a high-level, general-purpose programming language known for
its readable syntax and large ecosystem.

Python is used for:

- automation
- web development
- scripting
- data analysis
- scientific computing
- testing
- backend development
- artificial intelligence
- machine learning

Popular Python libraries include NumPy, pandas, scikit-learn,
TensorFlow, and PyTorch.

Reference:
https://docs.python.org/3/
""",

    "ai": """
Artificial Intelligence, or AI, is the field of computing focused on
building systems that can perform tasks that normally require forms
of human intelligence.

AI includes areas such as:

- rule-based systems
- machine learning
- deep learning
- reinforcement learning
- computer vision
- natural language processing
- speech systems
- generative AI

Modern AI is heavily based on machine learning, where systems learn
patterns from data.

Generative AI can create text, images, audio, video, and code. Large
language models are one type of generative AI system.

AI systems can also use tools, external information, memory, and
software actions to complete more complex tasks.

Important AI challenges include reliability, privacy, security, bias,
evaluation, and data quality.

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

The trained model can then be used on new data.

Common types of machine learning include supervised learning,
unsupervised learning, and reinforcement learning.

A typical ML project involves collecting data, cleaning it, preparing
features, choosing a model, training it, evaluating it, tuning it, and
deploying it.

Reference:
https://developers.google.com/machine-learning
""",

    "machine learning": """
Machine Learning is a subfield of Artificial Intelligence where
computer models learn patterns from data instead of depending only on
manually written rules.

During training, a model changes its parameters to improve performance
on a chosen objective.

Common learning approaches include:

- supervised learning
- unsupervised learning
- self-supervised learning
- semi-supervised learning
- reinforcement learning

Machine learning is widely used in recommendation systems, fraud
detection, search engines, computer vision, speech recognition, and
language models.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "llm": """
An LLM, or Large Language Model, is a machine learning model trained
on large amounts of data to understand and generate sequences of
tokens.

Many modern LLMs use Transformer architectures. Transformers use
self-attention to model relationships between tokens.

During pretraining, a model learns statistical patterns in its training
data. A common objective is next-token prediction.

After pretraining, an LLM may go through instruction tuning, supervised
fine-tuning, preference optimization, or safety training.

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

Deep learning is widely used in:

- computer vision
- speech recognition
- natural language processing
- recommendation systems
- generative AI

Important architectures include CNNs, RNNs, autoencoders, GANs, and
Transformers.

Training usually involves a forward pass, loss calculation,
backpropagation, and parameter updates.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "neural network": """
A neural network is a machine learning model made from connected
computational units arranged into layers.

A simple neural network normally contains:

- an input layer
- one or more hidden layers
- an output layer

During a forward pass, the network produces a prediction. A loss
function measures how far the prediction is from the expected result.

Backpropagation calculates gradients so that the model parameters can
be updated.

Important concepts include neurons, weights, biases, activation
functions, layers, loss functions, gradients, and backpropagation.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "api": """
An API, or Application Programming Interface, is a defined way for one
software system to communicate with another.

An API describes how software can request data or functionality and
what kind of response it should receive.

Web APIs commonly use HTTP methods such as:

- GET
- POST
- PUT
- PATCH
- DELETE

APIs can use approaches such as REST, GraphQL, RPC, WebSockets, and
webhooks.

Important API concerns include authentication, authorization,
validation, rate limiting, error handling, security, and versioning.

Reference:
https://developer.mozilla.org/en-US/docs/Glossary/API
""",

    "rag": """
RAG stands for Retrieval-Augmented Generation.

It is an AI architecture that combines information retrieval with a
generative language model.

A simple RAG pipeline works like this:

1. Collect documents.
2. Split them into smaller chunks.
3. Index those chunks.
4. Receive a user question.
5. Retrieve relevant information.
6. Give that information to the model.
7. Generate an answer.

RAG is useful for private documents, company knowledge bases, research
systems, customer support, and question-answering applications.

RAG is different from fine-tuning. Fine-tuning changes model
parameters, while RAG supplies external information during inference.

Reference:
https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/
""",
}

MATH_PATTERN = re.compile(
    r"^(-?\d+(?:\.\d+)?)\s*([+\-*/%])\s*(-?\d+(?:\.\d+)?)$"
)


def calculate(expression):
    """Calculate a basic two-number arithmetic expression."""
    match = MATH_PATTERN.fullmatch(expression)

    if not match:
        return None

    first = float(match.group(1))
    operator = match.group(2)
    second = float(match.group(3))

    if operator == "+":
        result = first + second
    elif operator == "-":
        result = first - second
    elif operator == "*":
        result = first * second
    elif operator == "/":
        if second == 0:
            return "Error: cannot divide by 0"
        result = first / second
    elif operator == "%":
        if second == 0:
            return "Error: cannot divide by 0"
        result = first % second
    else:
        return None

    if result.is_integer():
        return int(result)

    return result

def find_category(text):
    """Return the first matching AI-tool category."""
    words = set(text.split())

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in words or keyword in text:
                return category

    return None


def find_reference(text):
    """Find a programming reference topic in the user's message."""
    words = set(text.split())

    if "c++" in text:
        return "c++"

    for topic in REFERENCES:
        if topic in words:
            return topic

    return None


def find_reference_command(text, reference):
    """Find a supported command or keyword for a programming topic."""
    for command in reference:
        if command in text:
            return command

    return None


def find_concept(text):
    """
    Match a concept without depending on capitalization.

    The user's input is normalized to lowercase, so concept keys are
    also stored and compared in lowercase.
    """
    text = text.lower().strip()

    for topic in sorted(CONCEPTS, key=len, reverse=True):
        if text.endswith(topic):
            return topic

    return None


def is_math(text):
    """Return True if the input is a supported arithmetic expression."""
    return MATH_PATTERN.fullmatch(text) is not None


def show_loading(message="Searching"):
    """Show a small console loading animation."""
    print(f"Drico > {message}", end="", flush=True)

    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)

    print()


def show_banner():
    print("-" * 60)
    print("        DRICO - AI TOOLS ROUTER")
    print("-" * 60)
    print("Type 'show' to see the available commands.")
    print("Type 'exit' to close the program.\n")


def show_commands():
    print("\nDrico > Commands")
    print("automation / agent / workflow   - Automation tools")
    print("research / find / search        - Research tools")
    print("create / image / video          - Creative tools")
    print("build / website / app / code    - Development tools")
    print("git / python / java / c / c++   - Programming references")
    print("what is <topic>                 - Concept explanations")
    print("5+5, 10*2, 20/4                - Calculator")
    print("list / tools / links            - Show all tools")
    print("exit                            - Close Drico")
    print()


def show_tools(category):
    print(f"\nDrico > {category.title()} tools\n")

    for name, url in TOOLS[category]:
        print(f"{name} - {url}")

    print()


def show_all_tools():
    print("\nDrico > Full Tool Directory\n")

    for category, tool_list in TOOLS.items():
        print(f"[{category.title()}]")

        for name, url in tool_list:
            print(f"  {name} - {url}")

        print()

def handle_concept_question(user):
    """Handle questions such as 'what is AI' or 'explain RAG'."""
    concept = find_concept(user)

    if concept:
        show_loading()
        print(f"Drico > {CONCEPTS[concept].strip()}\n")
    else:
        show_loading()
        print("Drico > I don't have an explanation for that yet.")
        print("Drico > Type 'show' to see what I can answer.\n")


def handle_reference_question(user):
    """Handle programming reference requests."""
    topic = find_reference(user)

    if not topic:
        return False

    show_loading()

    reference = REFERENCES[topic]
    command = find_reference_command(user, reference)

    if command:
        print(f"Drico > {command}: {reference[command]}\n")
    else:
        if topic == "git":
            example = "git status"
        elif topic == "c++":
            example = "c++ vector"
        else:
            example = f"{topic} <keyword>"

        print(f"Drico > Try a specific command, like: {example}\n")

    return True


def run():
    show_banner()

    while True:
        user = input("User  > ").strip().lower()

        if not user:
            continue

        if user in {"exit", "quit", "bye"}:
            print("Drico > Thanks for using Drico.")
            break

        if user == "show":
            show_commands()
            continue

        if user in {"list", "tools", "links"}:
            show_all_tools()
            continue

        if is_math(user):
            show_loading("Calculating")
            answer = calculate(user)
            print(f"Drico > The result is: {answer}\n")
            continue

        if "how are you" in user:
            print("Drico > I am doing fine. How can I help you?\n")
            continue

        if "who are you" in user:
            print("Drico > I am Drico, a simple Python AI tools router.\n")
            continue

        if "hi" in user.split() or "hello" in user.split():
            print("Drico > Hello! How can I help you?\n")
            continue

        if user.startswith(("what is ", "what are ", "explain ")):
            handle_concept_question(user)
            continue

        if handle_reference_question(user):
            continue

        category = find_category(user)

        if category:
            show_loading()
            show_tools(category)
            continue

        print("Drico > I don't understand that yet.")
        print("Drico > Type 'show' to see what I can do.\n")


if __name__ == "__main__":
    run()
