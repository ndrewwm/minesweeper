"""Test behavior of the game-related classes."""

import pytest
from ..game import Board

class TestBoard:
    """Tests dedicated to checking the results from the Board class."""

    board = Board(N=8, mines=10)

    def test_get__improper_location(self):
        """Invalid locations should be handled."""

        with pytest.raises(ValueError):
            self.board.get(-1, -1)

        with pytest.raises(ValueError):
            self.board.get(20, 20)

    def test_neighbors__corner(self):
        """Verify that we find a corner square's neighbors correctly."""

        neighbors = self.board.neighbors(7, 7)
        points = {neighbor.point for neighbor in neighbors}
        expected = {(6, 6), (6, 7), (7, 6)}
        assert points == expected, "We should have 3 specific neighbors."

    def test_neighbors__left_side(self):
        """Verify that we can find a square's neighors if it's located on the left-edge."""

        neighbors = self.board.neighbors(1, 0)
        points = {neighbor.point for neighbor in neighbors}
        expected = {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)}
        assert points == expected, "We should have 5 specific neighbors."

    def test_neighbors__middle(self):
        """Verify that we can find a middle square's neighbors as expected."""

        neighbors = self.board.neighbors(4, 4)
        points = {neighbor.point for neighbor in neighbors}
        expected = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}
        assert points == expected, "We should have 8 specific neighbors."
