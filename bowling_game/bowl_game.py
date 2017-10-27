author__ = 'Ivaylo'
import random
import copy

"""Stand alone module encapsulating the bowling game and its attributes.
Can be used to simulate single player bowling game.

Usage:

# Create intance of the game
new_game = BowlGameSimulator()

# roll the bowling ball and get pins down
new_game.add_roll()

# Get the total game score and current game state
new_gameget_total_score()

"""


class BowlGameSimulator(object):
    """Simulate single player bowling game."""

    def __init__(self):
        self.reset_game()

    def add_roll(self):
        """Roll the ball and return at least pins down
        and some additional information if needed"""
        pins_down = random.randint(0, self.pins_remaining)
        self._update_game_state(pins_down)
        return pins_down

    def get_total_score(self):
        """Get the current game state, where required information is at least

        'Total Score'.
        """
        total_score = sum([frame_state['frame_score'] for frame, frame_state in
                           self.game_state.items() if
                           frame_state['frame_score']])
        return total_score

    def reset_game(self):
        """Initialize  game attributes to starting state"""
        self.game_state = {"Frame_" + str(i):
                           {"roll_1": 0, "roll_2": 0, "frame_score": 0}
                           for i in range(1, 11)}
        self.current_frame = 1
        self.current_roll = 1
        self.pins_remaining = 10
        self.finished = False

    def present_game_state(self):
        """Prepare game state for visual presentation.

        Returns new game state where
        strikes and spares are replaced with 'X' and '/'
        """
        new_game_state = copy.deepcopy(self.game_state)
        for frame in new_game_state:
            if new_game_state[frame]['roll_1'] == 10:
                new_game_state[frame]['roll_1'] = 'X'
            elif (new_game_state[frame]['roll_1'] +
                    new_game_state[frame]['roll_2']) == 10:
                new_game_state[frame]['roll_2'] = '/'
        return new_game_state

    def _recalculate_frame_scores(self):
        """Adjust frame score based on spares and strikes rolled.
        
        In the last frame spares and strikes scored do not require frame score
        update.
        """
        for frame_num in range(1, len(self.game_state) + 1):
            if frame_num < len(self.game_state):
                if self.game_state['Frame_{}'.format(frame_num)][
                    'frame_score'] == 10:
                    if self.game_state['Frame_{}'.format(frame_num)][
                        'roll_1'] == 10:
                        # Strike rolled
                        if self.game_state['Frame_{}'.format(frame_num + 1)][
                            'roll_1'] == 10:
                            if frame_num + 2 <= len(self.game_state):
                                self.game_state['Frame_{}'.format(frame_num)][
                                    'frame_score'] += \
                                    self.game_state[
                                        'Frame_{}'.format(frame_num + 1)][
                                        'roll_1'] + \
                                    self.game_state[
                                        'Frame_{}'.format(frame_num + 2)][
                                        'roll_1']
                            else:
                                self.game_state['Frame_{}'.format(frame_num)][
                                    'frame_score'] += \
                                    self.game_state[
                                        'Frame_{}'.format(frame_num + 1)][
                                        'roll_1'] + \
                                    self.game_state[
                                        'Frame_{}'.format(frame_num + 1)][
                                        'roll_2']
                        else:
                            self.game_state['Frame_{}'.format(frame_num)][
                                'frame_score'] += \
                                self.game_state[
                                    'Frame_{}'.format(frame_num + 1)][
                                    'roll_1'] + \
                                self.game_state[
                                    'Frame_{}'.format(frame_num + 1)]['roll_2']
                    else:
                        # Spare rolled
                        self.game_state['Frame_{}'.format(frame_num)][
                            'frame_score'] += \
                            self.game_state['Frame_{}'.format(frame_num + 1)][
                                "roll_1"]

    def _update_game_state(self, pins_down):
        """Updates game state - current frame, roll, frame_score.

        Contains the business logic to recalculate scores when strikes
        and/or spare is scored.
        """
        self.game_state['Frame_{}'.format(self.current_frame)][
            'roll_{}'.format(self.current_roll)] = pins_down
        self.game_state['Frame_{}'.format(self.current_frame)][
            'frame_score'] += pins_down
        if pins_down == 10 or self.current_roll == 2:
            self.current_frame += 1
            self.current_roll = 1
            self.pins_remaining = 10
            self._recalculate_frame_scores()
            if self.current_frame > 10:
                # Game Over! Open the result page and reset the game.
                self.finished = True
        else:
            self.current_roll += 1
            self.pins_remaining -= pins_down

