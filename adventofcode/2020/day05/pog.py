import typing

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	data = [line.strip() for line in input_file if line]

	ids = [0] * 810

	for line in data:
		low = 0
		high = 127
		for i in range(7):
			# print(low,high)
			if line[i] == "F":
				high = low + (high - low) // 2
			elif line[i] == "B":
				low = low + (high - low) // 2 + 1
		# row = low
		# print(low, high)
		lo = 0
		hi = 7
		for i in range(7,10):
			if line[i] == "L":
				hi = lo + (hi - lo) // 2
			elif line[i] == "R":
				lo = lo + (hi-lo)//2 + 1

		ids[low * 8 + lo] = 1
	
	for i in range(1,len(ids)-1):
		if i < 8 or i >= 8 * 127:
			continue
		if ids[i] == 0 and ids[i-1] == 1 and ids[i+1] == 1:
			yield str(i)

	# yield "pog"

def main() -> None:
	with open('input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()