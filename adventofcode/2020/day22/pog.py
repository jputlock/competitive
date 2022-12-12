# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def recursive_combat(d1, d2):

	rounds = []
	deck1 = d1.copy()
	deck2 = d2.copy()
	
	while min(len(deck1), len(deck2)) > 0:
		snapshot = (tuple(deck1), tuple(deck2))
		if snapshot in rounds:
			return (1, deck1, deck2)
		
		rounds.append(snapshot)
		play1, play2 = deck1.pop(0), deck2.pop(0)
		
		if play1 <= len(deck1) and play2 <= len(deck2):
			subround = recursive_combat(deck1[:play1], deck2[:play2])[0]
			if subround == 1:
				deck1.append(play1)
				deck1.append(play2)
			elif subround == 2:
				deck2.append(play2)
				deck2.append(play1)
		else:
			if play1 > play2:
				deck1.append(play1)
				deck1.append(play2)
			else:
				deck2.append(play2)
				deck2.append(play1)
		if len(deck1) == 0:
			return (2, deck1, deck2)
		elif len(deck2) == 0:
			return (1, deck1, deck2)

	return (1 if len(deck2) == 0 else 2, deck1, deck2)
	

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]
	
	player = 0
	deck1, deck2 = [],[]

	for line in data:
		if line.startswith("Player"):
			player += 1
		else:
			if player == 1:
				deck1.append(int(line))
			else:
				deck2.append(int(line))

	# while min(len(deck1), len(deck2)) > 0:
	# 	play1, play2 = deck1.pop(0), deck2.pop(0)
	# 	if play1 > play2:
	# 		deck1.append(play1)
	# 		deck1.append(play2)
	# 	else:
	# 		deck2.append(play2)
	# 		deck2.append(play1)

	ans = recursive_combat(deck1, deck2)
	print(ans)

	total = 0
	win_deck = ans[1] if ans[0] == 1 else ans[2]
	for i, num in enumerate(reversed(win_deck), 1):
		total += num * i
	
	yield total

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()

def recursive_combat(deck1, deck2):
	previous_games = set() # will be tuple(player1, player2)
 
	player1 = deck1.copy()
	player2 = deck2.copy()
 
	winner = None
	while not winner:
		if (tuple(player1), tuple(player2)) in previous_games:
			winner = "p1"
		else:
			previous_games.add((tuple(player1), tuple(player2)))
 
			card1 = player1.pop(0)
			card2 = player2.pop(0)
 
			if card1 <= len(player1) and card2 <= len(player2):
				result = recursive_combat(player1[:card1], player2[:card2])[0]
 
				if result == "p1":
					player1.append(card1)
					player1.append(card2)
				else:
					player2.append(card2)
					player2.append(card1)
			else:
				if card1 > card2:
					player1.append(card1)
					player1.append(card2)
				else:
					player2.append(card2)
					player2.append(card1)
 
			if len(player1) == 0:
				winner = "p2"
			elif len(player2) == 0:
				winner = "p1"
 
	return winner, player1, player2
 
def part2(player1, player2):
	result = recursive_combat(player1, player2)
	if result[0] == "p1":
		winner = result[1]
	else:
		winner = result[2]
 
	t = 0
 
	for i, j in enumerate(winner):
		t += (50 - i) * int(j)
 
	print(t)