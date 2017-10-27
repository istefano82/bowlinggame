import bowling_game.bowl_game as bowlgame
import random # used in mock object
import unittest
from unittest import mock


class TestBowlGame(unittest.TestCase):
    def setUp(self):
        self.new_game = bowlgame.BowlGameSimulator()

    def test_initial_game_state(self):
        """Test initial game state is properly set."""
        self.assertEqual(self.new_game.game_state, {
        'Frame_4': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_1': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_6': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_8': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_9': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_2': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_5': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_7': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_10': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_3': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0}}
                         )
        self.assertEqual(self.new_game.current_frame, 1)
        self.assertEqual(self.new_game.current_roll, 1)
        self.assertEqual(self.new_game.pins_remaining, 10)
        self.assertEqual(self.new_game.finished, False)

    def test_add_roll(self):
        """Test add_roll returns random integer between 0 and pins remaining.

        """
        pins_remaining = 10
        with mock.patch.object(bowlgame.BowlGameSimulator,
                               '_update_game_state') as mocked_simulator:
            self.new_game = bowlgame.BowlGameSimulator()
            with mock.patch('random.randint') as mock_randint:
                mock_randint.return_value = 5
                pins_down = self.new_game.add_roll()
                mock_randint.assert_called_with(0, pins_remaining)
                self.assertEqual(pins_down, 5)
                mocked_simulator.assert_called_once_with(5)

    def test_get_total_score(self):
        """Test get_total_score method returns correctly computed game state
        total score.

        Calculation shell be computed from the sum of all
        Frames frame_score attribute.
        """
        fake_game_state = {'Frame_1': {'frame_score': 7},
                           'Frame_2': {'frame_score': 5}}
        self.new_game.game_state = fake_game_state
        total_score = self.new_game.get_total_score()

        self.assertEqual(total_score, 12)

    def test_update_game_state_frame_first_roll(self):
        """Test current frame rolls and pins remaining are properly updated when
        
         _update_game_state is called for the first roll in the frame.
         """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 3, 'frame_score': 3}}
        self.new_game._update_game_state(pins_down=3)

        self.assertEqual(self.new_game.current_frame, 1)
        self.assertEqual(self.new_game.current_roll, 2)
        self.assertEqual(self.new_game.pins_remaining, 7)
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_update_game_state_frame_second_roll(self):
        """Test current frame rolls and pins remaining are properly updated when
         _update_game_state is called for the second roll in the frame.
         """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 3, 'frame_score': 3}}
        expected_state = {
        'Frame_1': {'roll_2': 4, 'roll_1': 3, 'frame_score': 7}}
        self.new_game.current_frame = 1
        self.new_game.current_roll = 2
        self.new_game.pins_remaining = 7
        with mock.patch.object(bowlgame.BowlGameSimulator,
                               '_recalculate_frame_scores') as mocked_simulator:
            self.new_game._update_game_state(pins_down=4)

            self.assertEqual(self.new_game.current_frame, 2)
            self.assertEqual(self.new_game.current_roll, 1)
            self.assertEqual(self.new_game.pins_remaining, 10)
            self.assertEqual(self.new_game.game_state, expected_state)
            mocked_simulator.assert_called_once_with()

    def test_update_game_state_frame_last_frame_last_roll(self):
        """Test game finishes when the last roll is performed and it is reinitilized to start state"""
        self.new_game.game_state = {
        'Frame_10': {'roll_2': 4, 'roll_1': 3, 'frame_score': 7}}
        expected_state = {
        'Frame_4': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_1': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_6': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_8': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_9': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_2': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_5': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_7': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_10': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0},
        'Frame_3': {'roll_2': 0, 'roll_1': 0, 'frame_score': 0}}

        self.new_game.current_frame = 10
        self.new_game.current_roll = 2
        self.new_game.pins_remaining = 10
        with mock.patch.object(bowlgame.BowlGameSimulator,
                               '_recalculate_frame_scores') as mocked_simulator:
            self.new_game._update_game_state(pins_down=4)
            # simulate reseting the game called from the views methods
            self.new_game.reset_game()
            self.assertEqual(self.new_game.current_frame, 1)
            self.assertEqual(self.new_game.current_roll, 1)
            self.assertEqual(self.new_game.pins_remaining, 10)
            self.assertEqual(self.new_game.finished, False)
            self.assertEqual(self.new_game.game_state, expected_state)
            mocked_simulator.assert_called_once_with()


    def test_recalculate_frame_scores_spare_scored(self):
        """Test frame scores are properly updated when spare is scored
        
        in a frame.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': '7', 'roll_1': 3, 'frame_score': 10},
        'Frame_2': {'roll_2': '6', 'roll_1': 4, 'frame_score': 10}}
        expected_state = {
        'Frame_1': {'roll_2': '7', 'roll_1': 3, 'frame_score': 14},
        'Frame_2': {'roll_2': '6', 'roll_1': 4, 'frame_score': 10}}
        self.new_game._recalculate_frame_scores()
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_recalculate_frame_scores_strike_scored(self):
        """Test frame scores are properly updated when strike is scored 
        
        in a frame.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_2': {'roll_2': 3, 'roll_1': 5, 'frame_score': 8}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 18},
        'Frame_2': {'roll_2': 3, 'roll_1': 5, 'frame_score': 8}}
        self.new_game._recalculate_frame_scores()
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_recalculate_frame_scores_mutiple_strikes_scored(self):
        """Test frame scores are properly updated when mutiple 
        
        strikes one after another are scored.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 30},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 20},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        self.new_game._recalculate_frame_scores()
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_recalculate_frame_scores_strike_last_frame(self):
        """Test frame scores are properly updated when strike
        
        is scored in the last frame.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 30},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 20},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        self.new_game._recalculate_frame_scores()
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_recalculate_frame_scores_spare_last_frame(self):
        """Test frame scores are properly updated when spare
        
        is scored in the last frame.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 30},
        'Frame_2': {'roll_2': 0, 'roll_1': 10, 'frame_score': 20},
        'Frame_3': {'roll_2': 0, 'roll_1': 10, 'frame_score': 10}}
        self.new_game._recalculate_frame_scores()
        self.assertEqual(self.new_game.game_state, expected_state)

    def test_present_game_state(self):
        """Replace strike and spare rolls with 'X' and '/' before 
        
        showing result to the user.
        """
        self.new_game.game_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 10, 'frame_score': 17},
        'Frame_2': {'roll_2': 3, 'roll_1': 7, 'frame_score': 10}}
        expected_state = {
        'Frame_1': {'roll_2': 0, 'roll_1': 'X', 'frame_score': 17},
        'Frame_2': {'roll_2': '/', 'roll_1': 7, 'frame_score': 10}}
        game_state = self.new_game.present_game_state()
        self.assertEqual(game_state, expected_state)


if __name__ == '__main__':
    unittest.main()

