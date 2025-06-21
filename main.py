"""The game's entrypoint."""

from game import Board
from prompt import get_size, get_input

def main():
    """Main game loop."""

    n = get_size()
    board = Board(N=n, mines=10)

    while board.playing:
        flag, loc = get_input(board_size=board.N)

        if flag:
            if board.turns == 0:
                print("Pick a square first.")
                continue

            board.flag(*loc)
        else:
            board.check(*loc)

        board.upkeep()
        board.display()


if __name__ == "__main__":
    main()
