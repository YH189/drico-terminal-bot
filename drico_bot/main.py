from unicodedata import category


TOOL_LINKS = {
    'automation': [
        ('CrewAI', 'https://www.crewai.com/'),
        ('LangChain', 'https://www.langchain.com/'),
        ('AutoGen', 'https://microsoft.github.io/autogen/'),
        ('Make.com', 'https://www.make.com/'),
        ('Zapier', 'https://zapier.com/'),
        ('n8n', 'https://n8n.io/'),
    ],
    'research': [
        ('Perplexity', 'https://www.perplexity.ai/'),
        ('NotebookLM', 'https://notebooklm.google.com/'),
        ('Grok', 'https://grok.com/'),
        ('Elicit', 'https://elicit.com/'),
        ('Consensus', 'https://consensus.app/'),
    ],
    'creative': [
        ('Midjourney', 'https://www.midjourney.com/'),
        ('Runway', 'https://runwayml.com/'),
        ('Gemini', 'https://gemini.google.com/'),
        ('ChatGPT', 'https://chatgpt.com/'),
        ('Ideogram', 'https://ideogram.ai/'),
    ],
    'development': [
        ('Claude', 'https://claude.ai/'),
        ('Cursor', 'https://www.cursor.com/'),
        ('GitHub Copilot', 'https://github.com/features/copilot'),
        ('Base44', 'https://app.base44.com/'),
        ('Lovable', 'https://lovable.dev/'),
        ('Replit', 'https://replit.com/'),
    ],
}
CATEGORY_KEYWORDS = {
    'automation': ['automation', 'agent', 'workflow'],
    'research': ['research', 'found'],
    'creative': ['create', 'image', 'video'],
    'development': ['build', 'website', 'app', 'code'],
}
GIT_COMMANDS = {
    'git status': 'Shows changed/staged/untracked files in the working directory.',
    'git add': 'Stages changes for the next commit. Use "git add ." for all files.',
    'git commit': 'Saves staged changes. Use "git commit -m \'message\'".',
    'git push': 'Uploads local commits to the remote repository.',
    'git pull': 'Downloads and merges changes from the remote repository.',
    'git branch': 'Lists branches, or creates one if given a name.',
    'git checkout': 'Switches branches, or restores files.',
    'git clone': 'Copies a remote repository to your local machine.',
}
PYTHON_SYNTAX = {
    'range': 'range(start, stop, step) generates a sequence of numbers.',
    'len': 'len(x) returns the number of items in a list, string, or dict.',
    'enumerate': 'enumerate(x) pairs each item with its index while looping.',
    'zip': 'zip(a, b) pairs up items from two iterables position by position.',
    'lambda': 'lambda x: x + 1 defines a small unnamed function inline.',
}

VALID_OPERATORS = ['+', '-', '*', '/', '%']

def print_banne():
    print('-'* 60)
    print('  AI TOOLS ROUTER + DEV REFERENCE - DRICO v2')
    print('-'*60)
    print("Type 'show' for commands, or 'exit' to quit.\n ")

def print_show():
    print('Bot  > Available commands:')
    print('  automation / agent / workflow   -> automation tool links')
    print('  research / found                -> research tool links')
    print('  create / image / video          -> creative tool links')
    print('  build / website / app / code    -> dev tool links')
    print('  git <command>                   -> git command reference')
    print('  python <keyword>                -> python syntax reference')
    print('  <number> <operator> <number>    -> calculates result, e.g. 5 + 3')
    print('  list / tools / links            -> full tool directory')

def print_tools(category):
    print(f'This looks like {category}-realated, so try:')
    for name,url in TOOL_LINKS[category]:
        print(f' {name:<16}:{url}')

def print_full_directory():
    print('You have requested full directory:')
    for category,tools in TOOL_LINKS.items():
        print(f'[{category}]')
        for name,url in tools:
            print(f'{name}:{url}')


