# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing

def parse_line(line: str) -> str:
	"""Parses a line of input. By default, does nothing.
	Arguments:
	line -- the line of input
	"""
	return line

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	data = [parse_line(line.strip()) for line in input_file if line.strip()]

	food_dict = dict()
	all_ingredients = set()
	count_dict = collections.defaultdict(int)

	for line in data:
		match = regex.match(r"(.*) \(contains (.*)\)", line)
		ingredients = set(x for x in match.group(1).split(" "))
		allergens = set(x for x in match.group(2).split(", "))
		
		all_ingredients |= ingredients

		for a in allergens:
			if a not in food_dict:
				food_dict[a] = ingredients
			else:
				food_dict[a] = food_dict[a].intersection(ingredients)
		
		for i in ingredients:
			count_dict[i] += 1

	possible_allergens = []
	for x in food_dict.values():
		possible_allergens += x


	for key in food_dict:
		food_dict[key] = list(food_dict[key])
	
	len_sort = sorted([(i, x) for i, x in food_dict.items()], key=lambda x: len(x[1]))


	allergy_foods = dict()
	for i in range(len(len_sort)):
		ind = len_sort[i][0]
		food = len_sort[i][1][0]
		for j in range(i+1, len(len_sort)):
			if food in len_sort[j][1]:
				len_sort[j][1].remove(food)
		allergy_foods[ind] = food
	print(allergy_foods)
	print(",".join(allergy_foods[x] for x in sorted(allergy_foods)))

	yield sum(count_dict[i] for i in all_ingredients if i not in possible_allergens)
	yield str()

def main() -> None:
	"""Called when the script is run."""
	with open(f'input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()