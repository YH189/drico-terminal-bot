import time


def show_loading(message="Searching"):
    print("Drico > {0}".format(message), end="", flush=True)

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
