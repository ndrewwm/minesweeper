from sys import exit
from rich.prompt import Prompt
from string import digits

prompt = Prompt()

def get_size() -> int:
    """Ask the user what size board they want to play."""

    choice = prompt.ask(
        prompt="What size board?",
        choices=["8x8", "9x9", "10x10", "15x15"],
        default="10x10",
    )
    n, _ = choice.split("x")
    return int(n)


def get_input(board_size: int) -> tuple[bool, tuple[int, int]]:
    """Get the user's input"""

    while True:
        flag = False
        resp = prompt.ask("Where next?")

        if resp == "exit":
            exit()

        if resp[0] not in digits:
            if resp[0].lower() != "f":
                continue
            flag = True
            resp = resp[1:]

        if resp[0] not in digits or resp[1] not in digits:
            continue

        i, j = int(resp[0]), int(resp[1])
        if i > board_size - 1 or j > board_size - 1:
            continue

        return flag, (i, j)
