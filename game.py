from random import randint
from ansitable import ANSITable, Column

class Square:
    """A square on the board, located at (i, j) in the grid."""

    def __init__(self, i: int, j: int):
        self.i = i  # row of the square in the grid
        self.j = j  # column of the square in the grid
        self.point = (i, j)
        self.flag = False  # is there a flag on the square?
        self.is_open = False  # has the square been revealed?
        self.mine = False  # does the square contain a mine?
        self.n = -1  # updated when opened --> how many mines in the square's neighbors?

    def open(self) -> None:
        """Reveal the tile."""
        self.is_open = True

    def __repr__(self) -> str:
        if self.flag:
            return "F"

        if self.is_open and self.mine:
            return "*"

        if self.is_open:
            return str(self.n) if self.n > 0 else " "

        return "+"

    def __str__(self) -> str:
        return self.__repr__()


class Board:
    """The game's board, sized N x N. Each entry (i, j) is a Square."""

    def __init__(self, N: int, mines: int):
        self.playing = True
        self.start = 0  # TODO: make this an intelligible time
        self.turns = 0
        self.N = N
        self.M = mines
        self.squares = [Square(i=i, j=j) for i in range(N) for j in range(N)]
        self.display()

    def get(self, i: int, j: int) -> Square:
        """Get a square at location (i, j) in the board."""

        if i < 0 or i > self.N - 1:
            raise ValueError(f"i must be between 0 and {self.N - 1}.")

        if j < 0 or j > self.N - 1:
            raise ValueError(f"j must be between 0 and {self.N - 1}.")

        for square in self.squares:
            if square.point == (i, j):
                return square

    def display(self) -> None:
        """Generate the display."""

        table = ANSITable(
            *[Column(str(i), colalign="^") for i in range(-1, self.N)],
            colsep=1,
            border="thin",
        )
        for i in range(self.N):
            table.row(i, *[str(self.get(i, j)) for j in range(self.N)])

        print(table)

    def upkeep(self) -> None:
        """Increment the turn counter by 1, checks to see if all mines are found."""
        self.turns += 1

        all_mines_flagged = all([square.flag for square in self.squares if square.mine])
        no_false_positives = all([not square.flag for square in self.squares if not square.mine])

        if all_mines_flagged and no_false_positives:
            self.playing = False
            print("You win!")

    def lay_mines(self, i: int, j: int) -> None:
        """Seed the board with mines. Called after the first guess."""

        while self.M > 0:
            square = self.get(randint(0, self.N - 1), randint(0, self.N - 1))
            if not square.mine and square.point != (i, j):
                square.mine = True
                self.M -= 1

    def neighbors(self, i: int, j: int) -> list[Square]:
        """Return a list containing the (ith, jth) square's neighbors."""

        K = [max(0, i - 1), min(self.N - 1, i + 1)]
        L = [max(0, j - 1), min(self.N - 1, j + 1)]

        m = []
        for k in range(K[0], K[1] + 1):
            for l in range(L[0], L[1] + 1):
                if (k, l) != (i, j):
                    m.append(self.get(k, l))
        return m

    def n(self, i: int, j: int) -> int:
        """Return the number of mines in a square's neighbors."""
        
        n = 0
        for neighbor in self.neighbors(i, j):
            n += int(neighbor.mine)
        return n

    def check(self, i: int, j: int) -> None:
        """Reveal a square."""

        if self.turns == 0:
            self.lay_mines(i, j)

        square = self.get(i, j)
        if square.is_open:
            return

        square.open()

        if square.mine:
            self.playing = False
            return

        square.n = self.n(i, j)
        if square.n != 0:
            return

        for neighbor in self.neighbors(i, j):
            self.check(neighbor.i, neighbor.j)

    def flag(self, i: int, j: int) -> None:
        """Add a flag to a square.""" 

        square = self.get(i, j)
        square.flag = not square.flag
