
import re


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


math_pattern = re.compile(
    r"^(-?\d+\.?\d*)\s*([+\-*/%])\s*(-?\d+\.?\d*)$"
)


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
        if second == 0:
            return "Error: cannot divide by zero"

        return first / second

    if operator == "%":
        if second == 0:
            return "Error: cannot divide by zero"

        return first % second


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

        if user == "exit" or user == "quit" or user == "bye":
            print("Drico > Thanks for using Drico.")
            break

        if user == "show":
            show_commands()
            continue

        if is_math(user):
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

        topic = find_reference(user)
        if topic:
            command = find_command(user, references[topic])
            
            if command:
                print("Drico >", command + ":", references[topic][command])
            else:
                print("Drico > Try a specific command, like:", topic + " status" if topic == "git" else topic + " <keyword>")
                
            continue
        
        category = find_category(user)
        
        if category:
            show_tools(category)
        else:
            print("Drico > I don't understand that yet.")
            print("Drico > Type 'show' to see what I can do.")


run()
