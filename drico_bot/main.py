import re
import sys
import time


# Tools grouped by what they are mainly used for
tools = {
    "automation": [
        ("CrewAI", "https://www.crewai.com/"),
        ("LangChain", "https://www.langchain.com/"),
        ("AutoGen", "https://microsoft.github.io/autogen/"),
        ("Make.com", "https://www.make.com/"),
        ("Zapier", "https://zapier.com/"),
        ("n8n", "https://n8n.io/")
    ],
    "research": [
        ("Perplexity", "https://www.perplexity.ai/"),
        ("NotebookLM", "https://notebooklm.google.com/"),
        ("Grok", "https://grok.com/"),
        ("Elicit", "https://elicit.com/"),
        ("Consensus", "https://consensus.app/")
    ],
    "creative": [
        ("Midjourney", "https://www.midjourney.com/"),
        ("Runway", "https://runwayml.com/"),
        ("Gemini", "https://gemini.google.com/"),
        ("ChatGPT", "https://chatgpt.com/"),
        ("Ideogram", "https://ideogram.ai/")
    ],
    "development": [
        ("Claude", "https://claude.ai/"),
        ("Cursor", "https://www.cursor.com/"),
        ("GitHub Copilot", "https://github.com/features/copilot"),
        ("Base44", "https://app.base44.com/"),
        ("Lovable", "https://lovable.dev/"),
        ("Replit", "https://replit.com/")
    ]
}


# Words used to decide which group of tools the user is asking about
keywords = {
    "automation": ["automation", "agent", "workflow"],
    "research": ["research", "found"],
    "creative": ["create", "image", "video"],
    "development": ["build", "website", "app", "code"]
}


git_commands = {
    "git status": "Shows the current changes in the project.",
    "git add": "Adds files to the staging area.",
    "git commit": "Saves the staged changes.",
    "git push": "Uploads your commits to GitHub.",
    "git pull": "Gets the latest changes from the remote repository.",
    "git branch": "Shows or creates branches.",
    "git checkout": "Switches between branches.",
    "git clone": "Copies a repository to your computer."
}

python_commands = {
    "range": "range(start, stop, step) creates a sequence of numbers.",
    "len": "len() gives the number of items in something.",
    "enumerate": "enumerate() gives both the index and the value while looping.",
    "zip": "zip() joins values from two or more lists together.",
    "lambda": "lambda is used to create a small function in one line."
}

java_commands = {
    "main": "public static void main(String[] args) is where a Java program starts.",
    "system.out.println": "Prints something to the console.",
    "for loop": "A for loop repeats code a certain number of times.",
    "arraylist": "ArrayList is a resizable list in Java.",
    "class": "A class is used as a blueprint for objects."
}

c_commands = {
    "main": "int main() is the starting point of a C program.",
    "printf": "printf() is used to print output.",
    "scanf": "scanf() is used to take input.",
    "pointer": "A pointer stores the memory address of another variable.",
    "malloc": "malloc() is used to allocate memory dynamically."
}

cpp_commands = {
    "main": "int main() is the starting point of a C++ program.",
    "cout": "std::cout is used to print output.",
    "cin": "std::cin is used to take input.",
    "class": "A class is a blueprint for creating objects.",
    "vector": "std::vector is a resizable container in C++."
}


references = {
    "git": git_commands,
    "python": python_commands,
    "java": java_commands,
    "c": c_commands,
    "c++": cpp_commands
}


# Basic explanations for common programming and AI topics
concepts = {
    "Git": """
Git is a distributed version control system used to track changes in
source code and other project files.

Git keeps a history of changes using commits. This makes it possible
to look at older versions, compare changes, and recover from mistakes.

Git also supports branches. A branch gives you a separate line of
development where you can work on a feature, bug fix, or experiment
without changing the main branch directly.

A normal Git workflow is to change files, check the changes, stage them
with git add, save them with git commit, and use git pull or git push
when working with a remote repository.

Git can be used without GitHub. A repository can stay completely
local or be hosted on another Git-compatible service.

Reference:
https://git-scm.com/docs
""",

    "Github": """
GitHub is an online platform for hosting Git repositories and
collaborating on software projects.

Git and GitHub are different. Git handles version control, while
GitHub provides an online place to store repositories and tools for
collaboration.

GitHub repositories can contain source code, documentation,
configuration files, releases, and the project's Git history.

Some common GitHub features are pull requests, issues, code reviews,
discussions, releases, permissions, and GitHub Actions.

A common workflow is:

1. Create or clone a repository.
2. Create a branch.
3. Make changes.
4. Commit the changes.
5. Push the branch to GitHub.
6. Open a pull request.
7. Review the changes.
8. Merge the branch.

Reference:
https://docs.github.com/en/repositories
""",

    "Python": """
Python is a high-level, general-purpose programming language known
for its readable syntax and large collection of libraries.

Python is used for web development, automation, scripting, data
analysis, scientific computing, testing, backend development,
cybersecurity, artificial intelligence, and machine learning.

One of Python's biggest advantages is its ecosystem. It has a large
standard library and many third-party packages available through PyPI.

Python is also widely used in AI and machine learning. Libraries such
as PyTorch, TensorFlow, scikit-learn, NumPy, and pandas all have strong
Python support.

Python uses indentation to organize blocks of code, which makes the
structure of a program easy to see.

Reference:
https://docs.python.org/3/
""",

    "AI": """
Artificial Intelligence, or AI, is the field of computing focused on
building systems that can perform tasks that normally require forms
of human intelligence.

AI includes areas such as rule-based systems, machine learning,
deep learning, reinforcement learning, computer vision, natural
language processing, speech systems, and generative AI.

Modern AI is heavily based on machine learning, where systems learn
patterns from data.

Generative AI can create content such as text, images, audio, video,
and code. Large language models are one type of generative AI system.

AI systems can also use tools, external information, memory, and
software actions to complete more complicated tasks.

AI development also has challenges such as reliability, privacy,
security, bias, evaluation, and data quality.

Reference:
https://www.nist.gov/artificial-intelligence
""",

    "Ml": """
Machine Learning, or ML, is a part of Artificial Intelligence where
models learn patterns from data and use those patterns to make
predictions or decisions.

A simple way to compare traditional programming and machine learning
is:

Traditional programming:
input + rules -> output

Machine learning:
data + learning algorithm -> trained model

The trained model can then be used on new data.

Common types of machine learning include supervised learning,
unsupervised learning, and reinforcement learning.

A typical ML project involves collecting data, cleaning it,
preparing it, choosing a model, training the model, testing it,
tuning it, and finally deploying it.

Important ideas include features, labels, parameters, loss functions,
gradient descent, overfitting, underfitting, regularization, and
evaluation metrics.

Reference:
https://developers.google.com/machine-learning
""",

    "Machine learning": """
Machine Learning is a subfield of Artificial Intelligence where
computer models learn patterns from data instead of depending only
on manually written rules.

During training, a model changes its parameters to improve its
performance on a chosen objective.

Common learning types include supervised learning, unsupervised
learning, self-supervised learning, semi-supervised learning, and
reinforcement learning.

Supervised learning is often used for classification and regression.
Unsupervised learning can be used to find patterns such as clusters.

Modern machine learning is used in recommendation systems, fraud
detection, search engines, computer vision, speech recognition,
language models, and generative AI.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "LLM": """
An LLM, or Large Language Model, is a machine learning model trained
on a large amount of data to understand and generate sequences of
tokens.

Many modern LLMs use Transformer architectures. Transformers use
self-attention to understand relationships between tokens.

During pretraining, a model learns statistical patterns in its
training data. One common training task is predicting the next token.

After pretraining, an LLM may go through additional training such as
instruction tuning, supervised fine-tuning, preference optimization,
or safety training.

LLMs can be used for writing, summarization, translation, question
answering, classification, coding, information extraction, and tool
use.

An LLM does not automatically have access to live information.
Applications can connect models to APIs, databases, search systems,
or other tools when current information is needed.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "Deep learning": """
Deep Learning is a part of machine learning that uses neural networks
with multiple layers.

The multiple layers allow the network to learn increasingly complex
representations of data.

Deep learning is widely used in computer vision, speech recognition,
natural language processing, recommendation systems, and generative AI.

Important neural network architectures include CNNs, RNNs, autoencoders,
GANs, and Transformers.

Training a neural network normally involves a forward pass, calculating
a loss, backpropagation, and updating the model parameters.

Large deep learning models often need substantial computing power,
with GPUs and other accelerators commonly used for training and
inference.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "neural network": """
A neural network is a machine learning model made from connected
computational units arranged into layers.

A simple neural network normally has an input layer, hidden layers,
and an output layer.

During a forward pass, the network produces a prediction. A loss
function measures how far the prediction is from the expected result.
Backpropagation is then used to calculate gradients so the parameters
can be updated.

Neural networks can learn complex relationships that are difficult
to describe using manually written rules.

A network with several hidden layers is generally called a deep
neural network.

Important concepts include neurons, weights, biases, activation
functions, layers, loss functions, gradients, and backpropagation.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "api": """
An API, or Application Programming Interface, is a defined way for
one software system to communicate with another.

An API describes how a program can request data or functionality and
what kind of response it should receive.

Web APIs commonly use HTTP methods such as GET, POST, PUT, PATCH,
and DELETE.

For example, a frontend application can send a GET request to a
backend API and receive information, often in JSON format.

APIs can use different approaches such as REST, GraphQL, RPC,
WebSockets, and webhooks.

Authentication, authorization, validation, rate limiting, error
handling, security, and versioning are common concerns when building
production APIs.

Reference:
https://developer.mozilla.org/en-US/docs/Glossary/API
""",

    "rag": """
RAG stands for Retrieval-Augmented Generation.

It is an AI architecture that combines information retrieval with
a generative language model.

Instead of asking a model to answer only from information stored in
its parameters, a RAG system first retrieves relevant information and
gives that information to the model as context.

A simple RAG process is:

1. Collect documents.
2. Split the documents into smaller pieces.
3. Index the pieces.
4. Receive a user question.
5. Find relevant information.
6. Give the retrieved information to the model.
7. Generate the answer.

RAG is useful for private documents, company knowledge bases,
research systems, customer support, and question answering.

RAG does not automatically make answers correct. If retrieval finds
bad or incomplete information, the final answer can still be wrong.

RAG is also different from fine-tuning. Fine-tuning changes model
parameters, while RAG normally supplies external information during
inference.

Reference:
https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/
"""
}

math_pattern = re.compile(
    r"^(-?\d+(?:\.\d+)?)\s*([+\-*/%])\s*(-?\d+(?:\.\d+)?)$"
)

THINKING_STAGES = ["Researching", "Analysing", "Finalising"]
CALC_STAGES = ["Thinking"]


def show_thinking(stages=None):
    """Show a small loading effect before an answer."""
    if stages is None:
        stages = THINKING_STAGES

    for stage in stages:
        print("Drico >", stage, end="", flush=True)

        for _ in range(3):
            time.sleep(0.25)
            print(".", end="", flush=True)

        print()
        time.sleep(0.15)


def banner():
    print("-" * 60)
    print("        DRICO - AI TOOLS ROUTER")
    print("-" * 60)
    print("Type 'show' to see the available commands.")
    print("Type 'exit' to close the program.\n")


def show_commands():
    print("\nDrico > Commands")
    print("automation / agent / workflow  - Automation tools")
    print("research / found               - Research tools")
    print("create / image / video         - Creative tools")
    print("build / website / app / code   - Development tools")
    print("git / python / java / c / c++  - Programming references")
    print("what is <topic>                - Concept explanations")
    print("5+5, 10*2, 20/4                - Calculator")
    print("list / tools / links            - Show all tools")
    print()


def show_tools(category):
    print("\nDrico > These tools may be useful:\n")

    for name, url in tools[category]:
        print(name, "-", url)

    print()


def show_all_tools():
    print("\nDrico > Full Tool Directory\n")

    for category, tool_list in tools.items():
        print("[" + category + "]")

        for name, url in tool_list:
            print(" ", name, "-", url)

        print()


def find_category(text):
    for category, words in keywords.items():
        for word in words:
            if word in text:
                return category

    return None


def find_reference(text):
    words = text.split()

    for topic in references:
        if topic in words:
            return topic

    return None


def find_concept(text):
    words = text.split()

    for topic in concepts:
        if topic in words or text.endswith(topic):
            return topic

    return None


def is_math(text):
    return math_pattern.fullmatch(text) is not None


def calculate(text):
    match = math_pattern.fullmatch(text)

    if match is None:
        return None

    first = float(match.group(1))
    operator = match.group(2)
    second = float(match.group(3))

    if operator == "+":
        return first + second

    if operator == "-":
        return first - second

    if operator == "*":
        return first * second

    if operator == "/":
        if second == 0:
            return "Error: cannot divide by 0"
        return first / second

    if operator == "%":
        if second == 0:
            return "Error: cannot divide by 0"
        return first % second

    return None


def find_command(text, reference):
    for command in reference:
        if command in text:
            return command

    return None


def run():
    banner()

    while True:
        user = input("User  > ").strip().lower()

        if not user:
            continue

        if user in ("exit", "quit", "bye"):
            print("Drico > Thanks for using Drico.")
            break

        if user == "show":
            show_commands()
            continue

        if is_math(user):
            show_thinking(CALC_STAGES)
            answer = calculate(user)
            print("Drico > The result is:", answer)
            continue

        if "how are you" in user:
            print("Drico > I am doing fine. What do you need?")
            continue

        if "who are you" in user:
            print("Drico > I am Drico, a simple Python chatbot.")
            continue

        if "hi" in user.split() or "hello" in user.split():
            print("Drico > Hello! How can I help you?")
            continue

        if "list" in user or "tools" in user or "links" in user:
            show_all_tools()
            continue

        if user.startswith("what is") or user.startswith("what are") or user.startswith("explain"):
            show_thinking()

            concept = find_concept(user)

            if concept:
                print("Drico >", concepts[concept])
            else:
                print("Drico > I don't have an explanation for that yet.")
                print("Drico > Type 'show' to see what I can answer.")

            continue

        topic = find_reference(user)

        if topic:
            show_thinking()

            command = find_command(user, references[topic])

            if command:
                print("Drico >", command + ":", references[topic][command])
            else:
                if topic == "git":
                    example = "git status"
                else:
                    example = topic + " <keyword>"

                print("Drico > Try a specific command, like:", example)

            continue

        category = find_category(user)

        if category:
            show_thinking()
            show_tools(category)
        else:
            print("Drico > I don't understand that yet.")
            print("Drico > Type 'show' to see what I can do.")


if __name__ == "__main__":
    run()
