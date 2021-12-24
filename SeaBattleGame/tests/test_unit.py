import unittest
import board
import player


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.player = player.Player()
        self.grid = [[1 if y == 0 else 0 for x in range(10)] for y in range(10)]

    def test_board_has_ten_rows(self):
        self.assertEqual(len(self.board.status), 10, "Error: incorrect board size")

    def test_board_all_ship_sunk(self):
        self.assertEqual(
            isinstance(self.board.all_ships_sunk(), bool),
            True,
            "Error: type of return value is invalid",
        )

    def test_board_add_ship(self):
        self.assertEqual(
            self.board.board_add_ship(0, 0, 2, 0, 3),
            (0, 2, 0, 0),
            "Error: some tuple values are incorrect",
        )

    def test_player_score(self):
        self.assertEqual(
            self.player.get_total_score(), 0, "Error: function returns wrong score"
        )

    def test_player_valid_location(self):
        self.assertEqual(
            self.player.valid_location(self.grid, 0, 0, 3, 0),
            0,
            "Error: ship placement is invalid",
        )


if __name__ == "__main__":
    unittest.main()
