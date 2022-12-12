# from ..util.inputs import *
import collections, functools, itertools, operator, os, regex, sys, typing
from math import sqrt

class Tile:
	def __init__(self, tile_id, data) -> None:
		self.id, self.data = tile_id, data

		self.edges = [
			"".join(row[-1] for row in data),
			self.data[-1],
			"".join(row[0] for row in data),
			self.data[0]
		]

	def left(self):
		return self.edges[2]

	def right(self):
		return self.edges[0]

	def top(self):
		return self.edges[3]

	def bottom(self):
		return self.edges[1]

	def rotate(self):
		return Tile(self.id, ["".join(r) for r in zip(*self.data[::-1])])

	def mirror_horizontal(self):
		return Tile(self.id, [r[::-1] for r in self.data])

	def mirror_vertical(self):
		return Tile(self.id, self.data[::-1])

	def image(self):
		return [row[1:-1] for row in self.data[1:-1]]

def parse_tiles(in_file):
	tiles = []

	tile_id = None
	tile_data = []

	for line in open(in_file):
		line = line.strip()

		if line == "":
			tiles.append(Tile(tile_id, tile_data))
			tile_id = None
			tile_data = []
		elif line.startswith("Tile "):
			tile_id = int(line[5:-1])
		else:
			tile_data.append(line)

	if tile_id is not None:
		tiles.append(Tile(tile_id, tile_data))

	return tiles

def form_image(tileset, length):
	possibilities = []

	for tile in tileset:
		for _ in range(2):
			possibilities.append(tile)
			possibilities.append(tile.mirror_horizontal())
			possibilities.append(tile.mirror_vertical())
			possibilities.append(possibilities[-1].mirror_horizontal())
			tile = tile.rotate()

	return backtrack(possibilities, [[None for _ in range(length)] for _ in range(length)], set())

def backtrack(tileset, grid, seen, curr=(0,0)):
	x,y = curr
	
	# base case
	if y == len(grid):
		return grid
	
	for tile in tileset:
		if tile.id in seen:
			continue
		
		if x > 0 and grid[y][x-1].right() != tile.left():
			continue
		
		if y > 0 and grid[y-1][x].bottom() != tile.top():
			continue
		
		grid[y][x] = tile
		newSeen = seen | {tile.id}
		
		newPos = curr
		if x < len(grid[y]) - 1:
			newPos = (x+1,y)
		else:
			newPos = (0,y+1)

		result = backtrack(tileset, grid, newSeen, newPos)
		if result:
			grid = result
			break
		# else this tile didnt match
		grid[y][x] = None
	else: # we didnt get a valid solution
		grid = None

	return grid

def crop_borders(grid):
	image = []
	sz = len(grid[0][0].left()) - 2 # 10 - 2 = 8
	for row in grid:
		new_row = [[] for _ in range(sz)]
		for tile in row:
			for i, image_row in enumerate(tile.image()):
				new_row[i] += [x for x in image_row]
		image += new_row
	return image

def find_and_remove(grid):

	def rotate(image):
		return [list(row) for row in zip(*image[::-1])]

	def mirror_horizontal(image):
		return [r[::-1] for r in image]

	def mirror_vertical(image):
		return image[::-1]


	image = crop_borders(grid)
	for _ in range(2):
		if remove_monsters(image):
			break

		image = mirror_horizontal(image)
		if remove_monsters(image):
			break

		image = mirror_vertical(image)
		if remove_monsters(image):
			break

		image = mirror_horizontal(image)
		if remove_monsters(image):
			break

		image = rotate(mirror_vertical(image))

	return image

def remove_monsters(image):
	x,y = 0,0
	num_monsters = 0

	rows, cols = len(image), len(image[0])
	offsets = [
		(1,0),
		(2,1),
		(2,4),
		(1,5),
		(1,6),
		(2,7),
		(2,10),
		(1,11),
		(1,12),
		(2,13),
		(2,16),
		(1,17),
		(0,18),
		(1,18),
		(1,19)
	]

	while y < rows - 3:
		while x < cols - 20:
			if all(image[y+i][x+j] == "#" for i,j in offsets):
				num_monsters += 1
				for i, j in offsets:
					image[y+i][x+j] = 'O'
				
				x += 19
			x += 1
		
		x,y = 0,y+1
	
	return num_monsters


def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	"""Generates solutions to the problem.
	Arguments:
	input_file -- the file containing the input
	"""
	
	tileset = parse_tiles(input_file)
	length = int(sqrt(len(tileset)))
	grid = form_image(tileset, length)
	
	# each corner
	yield functools.reduce(lambda x,y: x*y, [grid[i][j].id for i,j in itertools.product([0,-1], repeat=2)])
	yield sum(row.count('#') for row in find_and_remove(grid))


def main() -> None:
	"""Called when the script is run."""
	for solution in solve("input.txt"):
		print(solution)

if __name__ == '__main__':
	main()