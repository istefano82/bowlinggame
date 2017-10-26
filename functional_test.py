from selenium import webdriver
import unittest


class TestBowlingGame(unittest.TestCase):
      
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_bowlgame(self):
        self.browser.get('http://localhost:8000')
        self.assertEqual('Bowling Game', self.browser.title)

# Application should have 2 methods:

# add_roll - it rolls the ball and returns at least pins down and some additional information if needed. Method should be callble as URL and should return JSON response (it can be made as basic REST app)

# get_total_score - get current game state, where required information at least "Total Score"
if __name__ == "__main__":
    unittest.main(warnings='ignore')

