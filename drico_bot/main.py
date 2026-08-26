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
    "git status": {
        "description": "Shows the current state of your working directory and staging area. It tells you which files are modified, staged, untracked, or ready to commit.",
        "syntax": "git status",
        "example": "git status",
        "output": """On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   concepts.py

Untracked files:
  git_commands.py

no changes added to commit"""
    },

    "git add": {
        "description": "Moves changes from the working directory into the staging area so they can be included in the next commit.",
        "syntax": "git add <file>",
        "example": "git add concepts.py",
        "output": """$ git add concepts.py

$ git status
Changes to be committed:
  modified:   concepts.py"""
    },

    "git add .": {
        "description": "Stages all new, modified, and deleted files in the current directory and its subdirectories.",
        "syntax": "git add .",
        "example": "git add .",
        "output": """$ git add .

$ git status
Changes to be committed:
  modified:   concepts.py
  modified:   git_commands.py
  new file:   README.md"""
    },

    "git commit": {
        "description": "Creates a permanent snapshot of the staged changes in the Git repository. Each commit receives a unique commit hash.",
        "syntax": 'git commit -m "<message>"',
        "example": 'git commit -m "docs: expand Git concepts"',
        "output": """[main 7f3a21c] docs: expand Git concepts
 2 files changed, 86 insertions(+), 14 deletions(-)"""
    },

    "git log": {
        "description": "Displays the commit history of the repository, including commit hashes, authors, dates, and commit messages.",
        "syntax": "git log",
        "example": "git log --oneline",
        "output": """7f3a21c (HEAD -> main) docs: expand Git concepts
91c4e82 feat: add Python concepts
4a12d76 fix: update README
2b8f431 Initial commit"""
    },

    "git diff": {
        "description": "Shows the differences between your current working files and the last committed version. It is useful for reviewing changes before staging them.",
        "syntax": "git diff",
        "example": "git diff concepts.py",
        "output": """diff --git a/concepts.py b/concepts.py
@@ -10,7 +10,10 @@

-    "git": "Git tracks changes..."
+    "git": "Git is a distributed version control system..."
+
+    "rag": "RAG combines retrieval with generation..."
"""
    },

    "git diff --staged": {
        "description": "Shows the changes that have already been staged and will be included in the next commit.",
        "syntax": "git diff --staged",
        "example": "git diff --staged",
        "output": """diff --git a/concepts.py b/concepts.py
index 81a2f4c..9b42d17 100644
--- a/concepts.py
+++ b/concepts.py
@@ -1,5 +1,8 @@
 concepts = {
+    "git": "...",
+    "github": "...",
+    "python": "..."
 }"""
    },

    "git push": {
        "description": "Uploads local commits to a remote repository such as GitHub. The remote branch must usually be configured before pushing.",
        "syntax": "git push <remote> <branch>",
        "example": "git push origin main",
        "output": """Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (3/3), 2.41 KiB | 2.41 MiB/s, done.
To https://github.com/YH189/project.git
   91c4e82..7f3a21c  main -> main"""
    },

    "git pull": {
        "description": "Downloads changes from a remote repository and integrates them into your current local branch. Conceptually, it performs a fetch followed by an integration step.",
        "syntax": "git pull <remote> <branch>",
        "example": "git pull origin main",
        "output": """From https://github.com/YH189/project
 * branch            main       -> FETCH_HEAD
Updating 91c4e82..7f3a21c
Fast-forward
 concepts.py | 24 +++++++++++++++++++++++-
 README.md   |  5 +++++
 2 files changed, 28 insertions(+), 1 deletion(-)"""
    },

    "git fetch": {
        "description": "Downloads the latest commits and references from a remote repository without automatically merging those changes into your current branch.",
        "syntax": "git fetch <remote>",
        "example": "git fetch origin",
        "output": """From https://github.com/YH189/project
   91c4e82..7f3a21c  main       -> origin/main
   4a12d76..82b91de  dev        -> origin/dev"""
    },

    "git branch": {
        "description": "Lists existing branches, creates new branches, or deletes branches.",
        "syntax": "git branch <branch-name>",
        "example": "git branch feature/rag",
        "output": """$ git branch

* main
  dev
  feature/rag"""
    },

    "git switch": {
        "description": "Switches between branches. It is the modern Git command specifically designed for branch switching.",
        "syntax": "git switch <branch-name>",
        "example": "git switch feature/rag",
        "output": """Switched to branch 'feature/rag'"""
    },

    "git checkout": {
        "description": "An older, multi-purpose Git command historically used for switching branches, creating branches, and restoring files. For modern workflows, `git switch` and `git restore` are usually clearer alternatives.",
        "syntax": "git checkout <branch-name>",
        "example": "git checkout dev",
        "output": """Switched to branch 'dev'
Your branch is up to date with 'origin/dev'."""
    },

    "git switch -c": {
        "description": "Creates a new branch and immediately switches to it.",
        "syntax": "git switch -c <branch-name>",
        "example": "git switch -c feature/ai-search",
        "output": """Switched to a new branch 'feature/ai-search'"""
    },

    "git merge": {
        "description": "Combines the changes from one branch into the currently checked-out branch.",
        "syntax": "git merge <branch-name>",
        "example": "git merge feature/rag",
        "output": """Updating 7f3a21c..b91d442
Fast-forward
 rag.py | 42 ++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 42 insertions(+)"""
    },

    "git rebase": {
        "description": "Reapplies commits from one branch on top of another commit or branch. Rebase can create a cleaner, more linear project history but rewrites commit history.",
        "syntax": "git rebase <branch-name>",
        "example": "git rebase main",
        "output": """Successfully rebased and updated refs/heads/feature/rag."""
    },

    "git remote -v": {
        "description": "Displays the remote repositories configured for the current Git repository, including their fetch and push URLs.",
        "syntax": "git remote -v",
        "example": "git remote -v",
        "output": """origin  https://github.com/YH189/project.git (fetch)
origin  https://github.com/YH189/project.git (push)"""
    },

    "git clone": {
        "description": "Creates a local copy of a remote Git repository, including its files, branches, commits, and repository history.",
        "syntax": "git clone <repository-url>",
        "example": "git clone https://github.com/YH189/project.git",
        "output": """Cloning into 'project'...
remote: Enumerating objects: 42, done.
remote: Counting objects: 100% (42/42), done.
Receiving objects: 100% (42/42), done.
Resolving deltas: 100% (18/18), done."""
    },

    "git stash": {
        "description": "Temporarily stores uncommitted changes so you can switch branches or perform another Git operation without committing unfinished work.",
        "syntax": "git stash",
        "example": "git stash",
        "output": """Saved working directory and index state
WIP on feature/rag: b91d442 add retrieval pipeline"""
    },

    "git stash pop": {
        "description": "Restores the most recently stashed changes and removes that stash from the stash list.",
        "syntax": "git stash pop",
        "example": "git stash pop",
        "output": """On branch feature/rag
Changes not staged for commit:
  modified:   rag.py

Dropped refs/stash@{0} (a42f19d...)"""
    },

    "git restore": {
        "description": "Restores files to a previous state. It is commonly used to discard working-directory changes or remove files from the staging area.",
        "syntax": "git restore <file>",
        "example": "git restore concepts.py",
        "output": """$ git status
On branch main
nothing to commit, working tree clean"""
    },

    "git reset": {
        "description": "Moves the current branch reference to another commit and can modify the staging area or working directory depending on the selected mode. Use carefully because some reset modes can discard work.",
        "syntax": "git reset <mode> <commit>",
        "example": "git reset --soft HEAD~1",
        "output": """$ git reset --soft HEAD~1

$ git status
Changes to be committed:
  modified:   concepts.py"""
    },

    "git cherry-pick": {
        "description": "Applies the changes introduced by a specific commit onto the current branch. It is useful when you need one particular change without merging an entire branch.",
        "syntax": "git cherry-pick <commit-hash>",
        "example": "git cherry-pick 7f3a21c",
        "output": """[main 4d92bc1] docs: expand Git concepts
 Date: Wed Aug 26 19:10:00 2026
 1 file changed, 38 insertions(+), 4 deletions(-)"""
    },

    "git tag": {
        "description": "Creates or lists tags used to mark important points in repository history, commonly release versions.",
        "syntax": "git tag <tag-name>",
        "example": "git tag v1.0.0",
        "output": """$ git tag

v1.0.0"""
    },

    "git show": {
        "description": "Displays information about a specific Git object, commonly a commit, including its metadata and changes.",
        "syntax": "git show <commit>",
        "example": "git show 7f3a21c",
        "output": """commit 7f3a21c
Author: YH
Date:   Wed Aug 26 19:10:00 2026

    docs: expand Git concepts

diff --git a/concepts.py b/concepts.py
...
"""
    },

    "git log --oneline --graph": {
        "description": "Displays a compact visual representation of the commit history, including branches and merges.",
        "syntax": "git log --oneline --graph --all",
        "example": "git log --oneline --graph --all",
        "output": """*   b91d442 Merge branch 'feature/rag'
|\\
| * 82c31a4 add RAG pipeline
| * 71a91bc add vector search
|/
* 7f3a21c docs: expand Git concepts
* 91c4e82 feat: add Python concepts
* 4a12d76 Initial commit"""
    },

    "git rm": {
        "description": "Removes a tracked file from the working directory and stages the deletion for the next commit.",
        "syntax": "git rm <file>",
        "example": "git rm old_notes.txt",
        "output": """rm 'old_notes.txt'

$ git status
Changes to be committed:
  deleted:    old_notes.txt"""
    },

    "git config": {
        "description": "Reads or changes Git configuration settings, such as your username, email, default branch, and editor.",
        "syntax": "git config <option> <value>",
        "example": 'git config --global user.name "YH"',
        "output": """$ git config --global user.name "YH"

$ git config --global user.name
YH"""
    }
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
    "git": """
Git is a distributed version control system (DVCS) used to track changes to source code and other files throughout the development of a project. 
Instead of storing only the latest version of a project, Git records a history of commits, allowing developers to inspect previous states, compare changes, revert mistakes, and work on multiple versions of a project independently.

Git works locally, so most operations such as creating commits, viewing history, creating branches, and comparing changes do not require an internet connection. 
A Git repository contains the project's files together with its version history and metadata.

One of Git's most important features is branching. A branch provides an independent line of development, allowing developers to work on features, bug fixes, experiments, or releases without directly modifying the main development line. 
Branches can later be merged, and Git provides mechanisms for handling conflicts when different branches modify the same parts of a file.

The normal Git workflow involves modifying files, inspecting changes with commands such as `git diff`, staging changes with `git add`, creating a snapshot with `git commit`, and synchronizing with remote repositories using commands such as `git fetch`, `git pull`, and `git push`.

Important Git concepts include repositories, commits, branches, remotes, staging, merging, rebasing, tags, cherry-picking, stashing, and conflict resolution.

Git itself does not require GitHub. A Git repository can exist entirely on a local machine or be hosted on many different Git-compatible services.

In modern software development, Git is a foundational tool for source-code management, collaborative development, release management, open-source projects, and CI/CD workflows.

Reference:
https://git-scm.com/docs
""",

    "github": """
GitHub is a web-based software development and collaboration platform that hosts Git repositories and provides tools for working with software projects.

Git and GitHub are not the same thing. Git is the version control system that manages project history, while GitHub provides an online platform where Git repositories can be stored, shared, reviewed, and collaboratively developed.

A GitHub repository can contain source code, documentation, configuration files, datasets, releases, and the complete Git history of the project. Repositories can be public or private.

GitHub adds collaboration features around Git, including pull requests, issues, code review, discussions, project management, releases, permissions, repository security features, and automation through GitHub Actions.

A typical GitHub workflow is:
1. Create or clone a repository.
2. Create a branch for a change.
3. Modify the project locally.
4. Commit the changes using Git.
5. Push the branch to GitHub.
6. Open a pull request.
7. Review and discuss the changes.
8. Merge the approved changes into the target branch.

GitHub also supports CI/CD and developer automation through GitHub Actions, dependency and security tooling, code ownership, release management, and other repository-level features.

GitHub repositories are therefore more than simple online storage. They function as collaborative development environments where code, history, reviews, issues, automation, and project documentation can be managed together.

Reference:
https://docs.github.com/en/repositories
https://docs.github.com/en/get-started/onboarding/getting-started-with-your-github-account
""",

    "python": """
Python is a high-level, general-purpose programming language designed around readable syntax, dynamic typing, and a large standard library.

Python is interpreted through implementations such as CPython and supports multiple programming paradigms, including procedural, object-oriented, and functional programming.

Python is widely used in web development, automation, scripting, data analysis, scientific computing, cybersecurity, DevOps, artificial intelligence, machine learning, testing, and backend development.

One of Python's major strengths is its ecosystem. Developers can use built-in modules from the standard library as well as third-party packages distributed through the Python Package Index (PyPI).

Python is particularly important in AI and ML because major frameworks and libraries such as PyTorch, TensorFlow, scikit-learn, NumPy, pandas, and many modern AI tooling ecosystems provide Python interfaces.

Python code is generally designed to prioritize readability and developer productivity. Its indentation-based block structure makes the organization of code visually explicit.

Modern Python also includes features such as type annotations, asynchronous programming with `asyncio`, structural pattern matching, dataclasses, improved typing support, and increasingly capable concurrency features.

As of August 2026, the current stable major series is Python 3.14. Python 3.14.7 was released on August 5, 2026. The Python 3.14 series introduced major changes including officially supported free-threaded Python, deferred evaluation of annotations, template string literals, multiple interpreters in the standard library, and the `compression.zstd` module.

Python is therefore not simply an introductory programming language. It is a major production language used across software engineering, scientific computing, data engineering, and modern AI systems.

Reference:
https://docs.python.org/3/
https://www.python.org/downloads/release/python-3147/
""",

    "ai": """
Artificial Intelligence (AI) is the broad field of computing concerned with building systems capable of producing outputs such as predictions, recommendations, decisions, or generated content that would traditionally require forms of human intelligence.

AI is an umbrella term rather than a single algorithm or technology. It includes multiple approaches such as rule-based systems, search and planning, machine learning, deep learning, reinforcement learning, computer vision, natural language processing, speech systems, generative AI, and increasingly multimodal and agentic systems.

Traditional AI systems can use explicitly designed rules and symbolic reasoning. Modern AI is heavily dominated by machine learning, where models learn patterns from data.

Generative AI is a major modern branch of AI capable of generating new content such as text, images, audio, video, and code. Large language models are one important class of generative AI systems.

Modern AI systems can also combine multiple capabilities. For example, a multimodal model may process text and images, while an AI agent may use a model together with tools, external data, memory, and software actions to accomplish a task.

AI systems are not automatically intelligent in the human sense. Their capabilities depend on their architecture, training data, objectives, evaluation methods, available tools, and deployment environment.

AI also introduces engineering and governance challenges including reliability, hallucination, bias, privacy, security, explainability, robustness, data quality, evaluation, and misuse.

The modern AI engineering lifecycle therefore involves more than training a model. It can include data preparation, model selection, training or inference, evaluation, deployment, monitoring, security, and continuous improvement.

Reference:
https://www.nist.gov/artificial-intelligence
https://airc.nist.gov/airmf-resources/airmf/
""",

    "ml": """
Machine Learning (ML) is a subfield of Artificial Intelligence in which computational models learn patterns or relationships from data and use those learned patterns to make predictions, classifications, decisions, or other outputs.

Traditional programming generally follows the pattern:

input + manually written rules -> output

Machine learning instead often follows:

data + learning algorithm -> trained model

The trained model can then process new inputs and produce predictions.

Machine learning includes several major learning paradigms. Supervised learning uses labeled examples to learn tasks such as classification and regression. Unsupervised learning searches for structure in data, such as clusters or lower-dimensional representations. Reinforcement learning involves an agent learning through interactions with an environment and feedback in the form of rewards or penalties.

A typical ML workflow includes collecting data, cleaning and preprocessing it, selecting useful features or representations, splitting data into training/validation/test sets, choosing a model, training it, evaluating it, tuning hyperparameters, and deploying it.

Important ML concepts include features, labels, parameters, hyperparameters, loss functions, optimization, gradient descent, overfitting, underfitting, regularization, generalization, inference, and evaluation metrics.

Modern machine learning increasingly includes deep learning, foundation models, generative models, multimodal models, and large-scale pretrained models.

An important distinction is that a machine learning model does not simply "memorize intelligence." It learns statistical patterns from its training process, and its ability to generalize to unseen data is a central part of evaluating the model.

Reference:
https://developers.google.com/machine-learning
https://developers.google.com/machine-learning/glossary
""",

    "machine learning": """
Machine Learning (ML) is a subfield of Artificial Intelligence in which computational models learn patterns from data rather than relying entirely on manually written rules.

A machine learning system typically receives examples during training and adjusts its internal parameters to reduce an objective such as a loss function. After training, the resulting model can process previously unseen inputs during inference.

The major learning paradigms include supervised learning, unsupervised learning, semi-supervised learning, self-supervised learning, and reinforcement learning.

Supervised learning commonly solves classification and regression problems. Unsupervised learning can discover structure in data through techniques such as clustering. Self-supervised learning has become particularly important for modern foundation models because models can learn representations from large quantities of unlabeled data by creating learning signals from the data itself.

The quality of an ML system depends not only on the algorithm but also on data quality, representation, model architecture, training procedure, evaluation methodology, and deployment conditions.

Modern ML systems range from relatively simple linear regression and decision trees to very large neural networks containing billions or more parameters.

Machine learning is the foundation behind many modern systems including recommendation engines, fraud detection, search ranking, computer vision, speech recognition, language models, autonomous systems, and generative AI.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "llm": """
An LLM (Large Language Model) is a machine learning model trained on large-scale text or multimodal data to model language and generate or transform sequences of tokens.

Modern LLMs are commonly based on Transformer architectures. Instead of treating language purely as a sequence of isolated words, Transformer-based systems use mechanisms such as self-attention to model relationships between tokens across a context window.

During pretraining, a language model learns statistical relationships in large datasets. A common objective is next-token prediction, where the model learns to predict likely subsequent tokens from preceding context.

After pretraining, many LLMs undergo additional stages such as supervised fine-tuning, instruction tuning, preference optimization, safety training, or other post-training techniques to make them more useful for interactive tasks.

LLMs can perform tasks such as text generation, summarization, translation, question answering, classification, reasoning-oriented workflows, code generation, information extraction, and tool interaction.

Modern language models can also be multimodal, meaning they may process combinations of text, images, audio, or video rather than text alone.

An LLM does not inherently contain a live database of facts. Its knowledge is determined by its training and subsequent system components. For current or private information, systems can use retrieval, tools, APIs, databases, or other external sources.

Important LLM concepts include tokens, context windows, embeddings, attention, Transformers, pretraining, fine-tuning, instruction tuning, inference, temperature, sampling, quantization, model weights, and alignment.

LLMs are a subset of machine learning and deep learning, not a separate category of intelligence.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "deep learning": """
Deep Learning is a subfield of machine learning that uses neural networks with multiple layers to learn increasingly complex representations of data.

The term "deep" generally refers to the presence of multiple computational layers between the input and output. These layers allow the model to transform raw inputs into progressively more abstract representations.

For example, in computer vision, early layers of a neural network may learn low-level visual patterns, while deeper layers can represent increasingly complex structures. In language models, deep neural networks learn representations of tokens and their relationships across multiple layers.

Deep learning has been highly successful in computer vision, speech recognition, natural language processing, recommendation systems, scientific computing, and generative AI.

Important deep learning architectures include convolutional neural networks (CNNs), recurrent neural networks (RNNs), autoencoders, generative adversarial networks (GANs), and Transformer architectures.

Training deep neural networks generally involves forward propagation, calculating a loss, backpropagation, and parameter optimization using methods related to gradient descent.

Deep learning typically benefits from large datasets and substantial computational resources, particularly for large-scale foundation models. GPUs, TPUs, and other accelerators are commonly used to perform the large number of matrix and tensor operations required during training and inference.

Modern deep learning has evolved from task-specific neural networks toward large pretrained foundation models that can be adapted to many downstream applications.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "neural network": """
A neural network is a machine learning model composed of interconnected computational units organized into layers. It learns parameters that transform input data into useful predictions or representations.

A basic neural network contains an input layer, one or more hidden layers, and an output layer. Each neuron generally computes a weighted combination of inputs, applies a bias, and passes the result through an activation function.

During training, the network produces predictions through a forward pass. A loss function measures the difference between predictions and desired outcomes. Backpropagation then calculates how model parameters contributed to the error, and an optimization algorithm updates those parameters.

Neural networks can represent highly nonlinear relationships, which allows them to solve problems that are difficult to express using manually written rules.

A neural network with multiple hidden layers is generally referred to as a deep neural network.

Different architectures are suited to different problems. CNNs have historically been important in image processing, RNNs were widely used for sequential data, and Transformers are now central to many state-of-the-art language and multimodal systems.

Modern neural networks can contain millions, billions, or even substantially more parameters. Larger parameter counts alone do not guarantee better performance; architecture, data quality, training methodology, compute, and evaluation all matter.

Important concepts include neurons, weights, biases, activation functions, layers, loss functions, gradients, backpropagation, optimization, embeddings, attention, and parameters.

Reference:
https://developers.google.com/machine-learning/glossary
""",

    "api": """
An API (Application Programming Interface) is a defined interface through which one software component can interact with another software component.

An API specifies how a caller can request functionality or data and what form the response will take. APIs allow systems to communicate without requiring the caller to know how the underlying implementation works.

In web development, APIs commonly use HTTP and expose endpoints that clients can call using methods such as GET, POST, PUT, PATCH, and DELETE.

For example, a frontend application might send a GET request to an API endpoint to retrieve user information. The backend processes the request and returns a response, often in JSON format.

Modern APIs can use different architectural and communication approaches, including REST, GraphQL, RPC, WebSockets, Webhooks, and event-driven interfaces.

APIs commonly use authentication and authorization mechanisms such as API keys, OAuth 2.0, JSON Web Tokens, or other identity systems. Production APIs also need to consider rate limiting, validation, error handling, versioning, observability, caching, and security.

APIs are fundamental to modern software architecture because they allow frontend applications, backend services, databases, third-party platforms, AI models, payment systems, cloud services, and other systems to interact.

In AI development, APIs are frequently used to connect applications to model inference services, vector databases, retrieval systems, external tools, and other software components.

Reference:
https://developer.mozilla.org/en-US/docs/Glossary/API
""",

    "rag": """
RAG (Retrieval-Augmented Generation) is an AI architecture that combines information retrieval with generative models.

Instead of requiring a language model to answer entirely from information encoded in its parameters, a RAG system retrieves relevant external information and supplies that information as context to the model before generation.

A typical RAG pipeline works approximately like this:

1. Documents are collected from sources such as PDFs, websites, databases, or internal knowledge bases.
2. Documents are cleaned and divided into smaller chunks.
3. The chunks are converted into embeddings or indexed using another retrieval mechanism.
4. A user submits a query.
5. The system retrieves the most relevant pieces of information.
6. Retrieved content is provided to the language model as context.
7. The model generates an answer based on the supplied context.

This architecture allows an application to use private, domain-specific, or frequently changing information without necessarily retraining the underlying language model.

RAG is particularly useful for enterprise knowledge bases, document question answering, customer support, research systems, internal documentation, and applications where answers should be grounded in an external source.

Modern RAG systems can use vector search, keyword search, hybrid retrieval, reranking, metadata filtering, query rewriting, multi-step retrieval, citation generation, and agentic retrieval workflows.

RAG is not a guarantee of factual accuracy. Poor retrieval can provide the model with irrelevant or incomplete information, and the model can still generate incorrect conclusions. Therefore, retrieval quality, context construction, evaluation, and source attribution are important parts of a production RAG system.

RAG is also different from fine-tuning. Fine-tuning changes model parameters to adapt behavior or capabilities, whereas RAG generally leaves the model parameters unchanged and supplies relevant external information at inference time.

Reference:
https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/
"""
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