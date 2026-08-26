import re
import time
import sys


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

concepts = {
    "git": "Git is a version control system that tracks changes to your code over time and lets you collaborate without overwriting each other's work.",
    "github": "GitHub is a website that hosts Git repositories online, so you can back up, share, and collaborate on code.",
    "python": "Python is a general-purpose programming language known for readable syntax, widely used in web development, automation, and AI/ML.",
    "ai": "AI (Artificial Intelligence) is the broad field of building systems that perform tasks normally requiring human intelligence, like understanding language or recognizing images.",
    "ml": "ML (Machine Learning) is a subset of AI where systems learn patterns from data instead of being explicitly programmed with rules.",
    "machine learning": "Machine Learning is a subset of AI where systems learn patterns from data instead of being explicitly programmed with rules.",
    "llm": "An LLM (Large Language Model) is a machine learning model trained on huge amounts of text to understand and generate human-like language.",
    "deep learning": "Deep learning is a type of machine learning using multi-layered neural networks to learn complex patterns from large amounts of data.",
    "neural network": "A neural network is a machine learning model loosely inspired by the brain, made of layers of connected nodes that learn to map inputs to outputs.",
    "api": "An API (Application Programming Interface) is a defined way for two programs to talk to each other, usually by sending requests and getting responses.",
    "rag": "RAG (Retrieval-Augmented Generation) is a technique where an AI model looks up relevant information from a data source before generating its answer.",
}

math_pattern = re.compile(
    r"^(-?\d+\.?\d*)\s*([+\-*/%])\s*(-?\d+\.?\d*)$"
)

THINKING_STAGES = ["Researching", "Analysing", "Finalising"]


def show_thinking():
    for stage in THINKING_STAGES:
        sys.stdout.write("Drico > " + stage)
        sys.stdout.flush()
        for _ in range(3):
            time.sleep(0.25)
            sys.stdout.write(".")
            sys.stdout.flush()
        print()
        time.sleep(0.15)


def banner():
    print("-" * 60)
    print("        DRICO v2 - AI TOOLS ROUTER")
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
    print("what is <topic>                - Concept explanations (git, ai, ml, llm, api, rag...)")
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
    for category in tools:
        print("[" + category + "]")
        for name, url in tools[category]:
            print(" ", name, "-", url)
        print()


def find_category(text):
    for category in keywords:
        for word in keywords[category]:
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
    for topic in concepts:
        if topic in text.split() or topic + " " in text or text.endswith(topic):
            return topic
    return None


def is_math(text):
    return math_pattern.match(text) is not None


def calculate(text):
    match = math_pattern.match(text)
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
        return "Error: cannot divide by zero" if second == 0 else first / second
    if operator == "%":
        return "Error: cannot divide by zero" if second == 0 else first % second


def find_command(text, reference):
    for command in reference:
        if command in text:
            return command
    return None


def run():
    banner()

    while True:
        user = input("User  > ").strip().lower()

        if user == "":
            continue

        if user in ("exit", "quit", "bye"):
            print("Drico > Thanks for using Drico.")
            break

        if user == "show":
            show_commands()
            continue

        if is_math(user):
            show_thinking()
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
                print("Drico > I don't have an explanation for that yet. Type 'show' to see what I can answer.")
            continue

        topic = find_reference(user)
        if topic:
            show_thinking()
            command = find_command(user, references[topic])
            if command:
                print("Drico >", command + ":", references[topic][command])
            else:
                print("Drico > Try a specific command, like:", topic + " status" if topic == "git" else topic + " <keyword>")
            continue

        category = find_category(user)
        if category:
            show_thinking()
            show_tools(category)
        else:
            print("Drico > I don't understand that yet.")
            print("Drico > Type 'show' to see what I can do.")


run()