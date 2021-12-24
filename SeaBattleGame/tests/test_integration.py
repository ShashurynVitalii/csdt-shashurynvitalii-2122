import unittest
import player
import board
from pygame import display
from visible_board import VisibleBoard
from visible_board import Rectangle
from person_player import PersonPlayer


class IntegrationTests(unittest.TestCase):

    """This class is created for integration testing, basically for testing
    program modules which work depends on each other."""

    def setUp(self):
        self.display = display.set_mode((1000, 500))
        self.person_player = PersonPlayer()
        self.visible_board = VisibleBoard(0, 0, self.display)

    def test_visible_board_rectangles(self):
        self.assertEqual(
            isinstance(self.visible_board.rectangles[0][0], Rectangle),
            True,
            "Error: incorrect object type",
        )

    def test_visible_board_viewable_move(self):
        self.assertEqual(
            self.visible_board.viewable_move(0, 0), [], "Error: wrong list value"
        )

    def test_person_player_set_battleship(self):
        self.assertEqual(
            self.person_player.set_battleship(5, 5, 3),
            [(5, 5, 7, 5, 3)],
            "Error: wrong list value",
        )


if __name__ == "__main__":
    unittest.main()
