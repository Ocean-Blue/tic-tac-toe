"""Unit tests for the tic-tac-toe game logic."""

import unittest
from unittest.mock import patch

import tictactoe as game


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        game.init()
        game.playerPiece = "x"
        game.gamePiece = "o"

    def test_init_creates_empty_board_and_eight_lines(self):
        self.assertEqual(game.gameBoard, [["-"] * 3 for _ in range(3)])
        self.assertEqual(len(game.gameBoardValues), 9)
        self.assertTrue(all(value == 0 for value in game.gameBoardValues.values()))
        self.assertEqual(len(game.gameCounts), 8)
        self.assertEqual(
            [line.positions for line in game.gameCounts[:3]],
            [[(row, col) for col in range(3)] for row in range(3)],
        )

    def test_get_slot_value_maps_pieces_to_points(self):
        game.gameBoard[0] = ["o", "x", "-"]

        self.assertEqual(game.getSlotValue(0, 0), game.GAME_POINT)
        self.assertEqual(game.getSlotValue(0, 1), game.PLAYER_POINT)
        self.assertEqual(game.getSlotValue(0, 2), 0)

    def test_play_move_updates_board_values_and_crossing_lines(self):
        game.playMove((1, 1), "x", game.PLAYER_POINT)

        self.assertEqual(game.gameBoard[1][1], "x")
        self.assertEqual(game.gameBoardValues[(1, 1)], game.PLAYER_POINT)
        self.assertEqual(
            [line.count for line in game.gameCounts], [0, -5, 0, 0, -5, 0, -5, -5]
        )

    def test_find_move_takes_center_when_available(self):
        self.assertEqual(game.findMove(), (1, 1))

    def test_find_move_takes_immediate_winning_spot(self):
        # The game has two pieces in the top row and can finish at (0, 2).
        game.playMove((0, 0), "o", game.GAME_POINT)
        game.playMove((0, 1), "o", game.GAME_POINT)
        # Occupy the center so move selection evaluates line scores.
        game.playMove((1, 1), "x", game.PLAYER_POINT)

        self.assertEqual(game.findMove(), (0, 2))

    def test_update_game_state_detects_player_loss(self):
        for column in range(3):
            game.playMove((2, column), "x", game.PLAYER_POINT)

        game.updateGameState()

        self.assertEqual(game.gameState, "lost")

    def test_update_game_state_detects_game_win(self):
        for column in range(3):
            game.playMove((0, column), "o", game.GAME_POINT)

        game.updateGameState()

        self.assertEqual(game.gameState, "won")

    def test_player_move_skips_occupied_coordinate(self):
        game.playMove((0, 0), "o", game.GAME_POINT)

        with patch("builtins.input", side_effect=["0,0", "2,1"]):
            self.assertEqual(game.getPlayerMove(), (2, 1))


if __name__ == "__main__":
    unittest.main()
