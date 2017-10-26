author__ = 'Ivaylo Stefanov'

import copy
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from bowling_game.bowl_game import BowlGameSimulator
# Create your views here.

BOWL_GAME = None

def home_page(request):
    return render(request, 'home.html')
    
def add_roll(request):
	global BOWL_GAME
	if not BOWL_GAME:
		BOWL_GAME = BowlGameSimulator()
		pins_down = BOWL_GAME.add_roll()
	else:
		if not BOWL_GAME.finished:
			pins_down = BOWL_GAME.add_roll()
		else:
			return redirect('http://localhost:8000/game_over')
	return JsonResponse({'Pins Down': pins_down})
	
def get_total_score(request):
	try:
		total_score = BOWL_GAME.get_total_score()
		game_state = (BOWL_GAME._present_game_state())
	except AttributeError:
		return render(request, 'game_not_started_yet.html')
	return JsonResponse({"Total Score": total_score, "Game State": game_state}, safe=False)
	
def game_over(request):
	total_score = BOWL_GAME.get_total_score()
	game_state = (BOWL_GAME._present_game_state())
	BOWL_GAME._reset_game()
	return render(request, 'game_over.html', {'total_score': total_score, 'game_state': game_state})

def _present_game_state(original_state):
    """Prepare game state for visual presentation.
    
    Takes the original game state and returns new game state where
    strikes and spares are replaced with 'X' and '/'
    """
    new_game_state = copy.deepcopy(original_state)
    for _dummy, frame_state in new_game_state.items():
    	if frame_state['roll_1'] == 10:
    		frame_state['roll_1'] = 'X'
    	if (frame_state['roll_1'] + frame_state['roll_2'])== 10:
    		frame_state['roll_2'] = '/'
    return new_game_state

