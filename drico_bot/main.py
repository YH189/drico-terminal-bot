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
    "automation": {"automation", "agent", "workflow"},
    "research": {"research", "find", "found", "search"},
    "creative": {"create", "image", "video", "design"},
    "development": {"build", "website", "app", "code", "develop"},
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
    "api": "api",
    "rag": "rag",
}


MATH_PATTERN = re.compile(
    r"^(-?\d+(?:\.\d+)?)\s*([+\-*/%])\s*(-?\d+(?:\.\d+)?)$"
)


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[?!.,;:]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def calculate(expression):
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
    words = set(normalize_text(text).split())

    for category, keywords in CATEGORY_KEYWORDS.items():
        if words.intersection(keywords):
            return category

    return None


def find_reference(text):
    text = normalize_text(text)
    words = set(text.split())

    if "c++" in text:
        return "c++"

    for topic in REFERENCES:
        if topic in words:
            return topic

    return None


def find_reference_command(text, reference):
    text = normalize_text(text)

    for command in reference:
        if command in text:
            return command

    return None


def find_concept(text):
    text = normalize_text(text)

    for alias in sorted(CONCEPT_ALIASES, key=len, reverse=True):
        if re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", text):
            return CONCEPT_ALIASES[alias]

    return None


def is_concept_question(text):
    text = normalize_text(text)

    starters = (
        "what is ",
        "what are ",
        "what's ",
        "whats ",
        "explain ",
        "tell me about ",
        "what is the use of ",
        "what are the uses of ",
        "what is use of ",
    )

    return text.startswith(starters)


def is_math(text):
    return MATH_PATTERN.fullmatch(text.strip()) is not None


def show_loading(message="Searching"):
    print(f"Drico > {message}", end="", flush=True)

    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)

    print()


def show_banner():
    print("-" * 50)
    print("        DRICO - AI TOOLS ROUTER")
    print("-" * 50)
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
    concept = find_concept(user)

    show_loading()

    if concept:
        print(f"Drico > {CONCEPTS[concept].strip()}\n")
    else:
        print("Drico > I don't have an explanation for that yet.")
        print("Drico > Type 'show' to see what I can answer.\n")


def handle_reference_question(user):
    topic = find_reference(user)

    if not topic:
        return False

    reference = REFERENCES[topic]
    command = find_reference_command(user, reference)

    if not command:
        return False

    show_loading()
    print(f"Drico > {command}: {reference[command]}\n")
    return True


def run():
    show_banner()

    while True:
        raw_user = input("User  > ").strip()

        if not raw_user:
            continue

        user = normalize_text(raw_user)

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

        if is_concept_question(user):
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
