import typing
import re

def solve(input_file: typing.IO) -> typing.Generator[str, None, None]:
	data = [line.strip() for line in input_file]

	total = 0
	fields = dict()

	for line in data:
		if not line:
			valid = len(fields) == 8 or (len(fields) == 7 and "cid" not in fields)
			if not valid:
				fields = dict()
				continue
			valid &= re.match(r"\d{4}", fields["byr"]) is not None
			valid &= 1920 <= int(fields["byr"]) <= 2002
			valid &= 2010 <= int(fields["iyr"]) <= 2020 and len(fields["iyr"]) == 4 and all(c in "0123456789" for c in fields["iyr"])
			valid &= 2020 <= int(fields["eyr"]) <= 2030 and len(fields["eyr"]) == 4 and all(c in "0123456789" for c in fields["eyr"])
			if fields["hgt"][-2:] == "cm":
				valid &= 150 <= int(fields["hgt"][:-2]) <= 193
			elif fields["hgt"][-2:] == "in":
				valid &= 59 <= int(fields["hgt"][:-2]) <= 76
			else:
				valid = False
			valid &= fields["hcl"][0] == "#" and all(c in "0123456789abcdef" for c in fields["hcl"][1:]) and len(fields["hcl"]) == 7
			valid &= fields["ecl"] in ["amb","blu","brn","gry","grn","hzl","oth"]
			valid &= len(fields["pid"]) == 9 and all(c in "0123456789" for c in fields["pid"])
			if valid:
				total += 1
			fields = dict()
			continue
		for pair in line.split(" "):
			key, val = pair.split(":")
			fields[key] = val

	valid = len(fields) == 8 or (len(fields) == 7 and "cid" not in fields)
	if valid:
		valid &= 1920 <= int(fields["byr"]) <= 2002 and len(fields["byr"]) == 4 and all(c in "0123456789" for c in fields["byr"])
		valid &= 2010 <= int(fields["iyr"]) <= 2020 and len(fields["iyr"]) == 4 and all(c in "0123456789" for c in fields["iyr"])
		valid &= 2020 <= int(fields["eyr"]) <= 2030 and len(fields["eyr"]) == 4 and all(c in "0123456789" for c in fields["eyr"])
		if fields["hgt"][-2:] == "cm":
			valid &= 150 <= int(fields["hgt"][:-2]) <= 193
		elif fields["hgt"][-2:] == "in":
			valid &= 59 <= int(fields["hgt"][:-2]) <= 76
		valid &= fields["hcl"][0] == "#" and all(c in "0123456789abcdef" for c in fields["hcl"][1:]) and len(fields["hcl"]) == 7
		valid &= fields["ecl"] in ["amb","blu","brn","gry","grn","hzl","oth"]
		valid &= len(fields["pid"]) == 9 and all(c in "0123456789" for c in fields["pid"])
		if valid:
			total += 1
	yield str(total)


def get_match(regex, text):
	return re.match(regex, text).groups()

def get_all_matches(regex, text):
	return re.search(regex, text).groups()

def main() -> None:
	with open('input.txt', 'r') as input_file:
		for solution in solve(input_file):
			print(solution)

if __name__ == '__main__':
	main()