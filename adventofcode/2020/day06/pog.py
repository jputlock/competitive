import typing

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	data = [line.strip() for line in input_file] + [""]

	total = 0
	questions = set()
	lst = []
	for line in data:
		if not line:
			questions = lst[0].intersection(*lst)
			total += len(questions)
			lst = []
			continue

		lst.append(
			set(c for c in line)
		)

	yield total

def main() -> None:
	with open('input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()