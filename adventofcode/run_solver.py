from argparse import FileType
from io import TextIOWrapper
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from importlib import import_module
from functools import partial
from os import getenv
from pathlib import Path
from tap import Tap
from termcolor import colored
from types import ModuleType
from typing import *

import os
import re
import requests
import select
import sys
import time
import traceback

# Types
PartAnswerPair = Tuple[int, str]
AnswerCallback = Callable[[List[PartAnswerPair]], None]
SolverMap = Dict[Tuple[int, int], ModuleType]


def evaluate(
    solver: ModuleType,
    puzzle_input: str,
    parts: set[int],
    answer_callback: AnswerCallback,
):
    part_answer_pairs: List[PartAnswerPair] = []
    for part, answer in enumerate(solver.solve(puzzle_input), 1):
        part_answer_pairs.append((part, str(answer)))

    answer_callback(part_answer_pairs)


def to_path(string: str) -> Literal["actual", "example"] | Path:
    if string == "actual":
        return "actual"
    elif string == "example":
        return "example"

    path = Path(string)
    if not path.exists() or not path.is_file():
        print("Given path does not exist or is not a file. Exiting...")
        exit(1)
    return path


class ArgParser(Tap):
    """
    Runs a solver for an Advent of Code puzzle.
    """

    day: int  # the day for the solver
    year: int  # the year for the solver
    mode: Literal["actual", "example"] | Path  # the type of puzzle input
    pipe: str  # the name of the pipe to listen for commands from the Advent Console

    def configure(self) -> None:
        self.add_argument("--mode", type=to_path)


class WebsiteManager:
    """
    Manages all interactions with https://adventofcode.com/

    Args:
        session_token: The session token associated with an AoC account.
    """

    USER_AGENT: str = "AoC @ github.com/jputlock/competitive/"
    SESSION: str

    def __init__(self, session_token: str):
        """
        Constructs a WebsiteManager.

        Args:
            session_token: The session token associated with an AoC account.
        """
        self.SESSION = session_token

    def get_example_input(self, day: int, year: int) -> Optional[str]:
        """
        Retrieves the example input for a puzzle.

        Args:
            day: Which day the puzzle is from.
            year: Which year the puzzle is from.

        Returns:
            The example puzzle input, or None if it failed to scrape an example input.
        """
        problem_document = self.__retrieve_page(day, year)
        if problem_document is None:
            return None
        return self.__scrape_example_input(problem_document)

    def get_actual_input(self, day: int, year: int) -> Optional[str]:
        """
        Retrieves the actual input for a puzzle.

        Args:
            day: Which day the puzzle is from.
            year: Which year the puzzle is from.

        Returns:
            The puzzle input, or None if it could not be retrieved.
        """
        # If the puzzle input has previously been retrieved, then read it from the
        # file
        input_path = Path(f"inputs/year{year}/day{str(day).rjust(2, '0')}/input.txt")
        if input_path.exists():
            with open(input_path, "r") as input_file:
                return input_file.read()

        # Retrieve the puzzle input
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        response = requests.get(
            url,
            headers={"User-Agent": self.USER_AGENT},
            cookies={"session": self.SESSION},
        )
        if response.status_code != 200:
            print(
                colored("WARNING", "yellow", attrs=["bold"]),
                f"Cannot retrieve input from {url}",
                file=sys.stderr,
            )
            return None
        input = response.text.strip("\r\n")

        # Save the puzzle input to a file
        input_path.parent.mkdir(parents=True, exist_ok=True)
        with open(input_path, "w") as input_file:
            input_file.write(input)

        return input

    def submit(self, day: int, year: int, part: int, answer: any):  # type: ignore
        """
        Submits an answer for a specified puzzle.

        Args:
            day: Which day the puzzle is from.
            year: Which year the puzzle is from.
            part: Which part was solved.
            answer: The answer to the puzzle.
        """
        url = f"https://adventofcode.com/{year}/day/{day}/answer"
        response = requests.post(
            url,
            headers={"User-Agent": self.USER_AGENT},
            cookies={"session": self.SESSION},
            data={"level": part, "answer": str(answer)},
        )

        doc = BeautifulSoup(response.text, "html.parser")
        for paragraph in doc.find("article").find_all("p"):
            print()
            print(paragraph.text)

    # Answer callbacks

    def submission_prompt(
        self, day: int, year: int, part_answer_pairs: List[Tuple[int, str]]
    ):
        for index, (part, answer) in enumerate(part_answer_pairs):
            sep = "\n" if "\n" in answer else " "
            print(f"Part {part} answer:{sep}{answer}")

            if index == len(part_answer_pairs) - 1:
                response = input("Would you like to submit? ")
                if response.lower() in ["y", "yes"]:
                    print(colored("yes", "green"))
                    self.submit(day, year, part, answer)
                else:
                    print(colored("no", "red"))

    def verify_example_answer(
        self, day: int, year: int, part_answer_pairs: List[Tuple[int, str]]
    ):
        """
        Verifies that the given answer matches the answer given on the page for the example input.

        Args:
            day: Which day the puzzle is from.
            year: Which year the puzzle is from.
            part_answer_pairs: A list of pairs denoting answers for a puzzle and which parts they
            correspond to.
        """
        document = self.__retrieve_page(day, year)
        if document is None:
            return None

        match = document.find("main")

        for part, answer in part_answer_pairs:
            part_counter = 1
            for content in match.contents:
                if content.text.startswith("---"):
                    if part_counter != part:
                        part_counter += 1
                        continue

                    separator = "\n" if "\n" in str(answer) else " "
                    text = (
                        colored("[EXAMPLE]", "cyan", attrs=["bold"])
                        + f" Part {part} answer:{separator}{answer}"
                    )

                    next_text = ""

                    if content.text.find(answer) != -1:
                        emphasized = [x.text.strip() for x in content.find_all("em")]

                        next_text = (
                            colored("FOUND", "green", attrs=["bold"])
                            + " "
                            + (
                                colored("(emphasized too!)", "green", attrs=["bold"])
                                if answer in emphasized
                                else colored("(not emphasized)", "red", attrs=["bold"])
                            )
                        )
                    else:
                        next_text = colored("NOT FOUND", "red", attrs=["bold"])

                    print(f"{text}{separator}{next_text}")
                    break

    # Private methods

    def __scrape_example_input(self, document: BeautifulSoup) -> Optional[str]:
        """
        Attempts to get an example input from a problem statement page using observed patterns in
        how they have been historically written.

        Args:
            doc: The BeautifulSoup object

        Returns:
            The example input, or None if an example input could not be determined from the
            document.
        """
        keywords = ["for example", "example", "suppose"]
        example: Optional[str] = None
        for keyword in keywords:
            match = document.find(string=re.compile(keyword))
            if match is not None:
                code = match.parent.find_next("code")
                if code is not None:
                    example = code.text.strip("\r\n")
                    break

        if example is None:
            print(
                colored("ERROR", "red", attrs=["bold"]),
                "Cannot find example puzzle input",
                file=sys.stderr,
            )
            return None

        return example

    def __retrieve_page(self, day: int, year: int) -> Optional[BeautifulSoup]:
        """
        Retrieves the problem statement page for a puzzle.

        Args:
            day: Which day the puzzle is from.
            year: Which year the puzzle is from.

        Returns:
            The problem page as a BeautifulSoup object, or None if it could not be retrieved.
        """
        # If the problem page has previously been retrieved, then read the cached copy
        problem_statement_path = Path(
            f"inputs/year{year}/day{str(day).rjust(2, '0')}/problem_statement.txt"
        )
        if problem_statement_path.exists():
            with open(problem_statement_path, "r") as file:
                return BeautifulSoup(file.read(), "html.parser")

        # Retrieve the example puzzle input
        url = f"https://adventofcode.com/{year}/day/{day}"
        response = requests.get(
            url,
            headers={"User-Agent": self.USER_AGENT},
            cookies={"session": self.SESSION},
        )
        if response.status_code != 200:
            print(
                colored("WARNING", "yellow", attrs=["bold"]),
                f"Cannot retrieve problem page from {url}",
                file=sys.stderr,
            )
            return None
        input = response.text.strip("\r\n")

        # Save the puzzle input to a file
        problem_statement_path.parent.mkdir(parents=True, exist_ok=True)
        with open(problem_statement_path, "w") as input_file:
            input_file.write(input)

        return BeautifulSoup(response.text, "html.parser")


def noop(_unused: List[PartAnswerPair]):
    pass


def run_day(
    website_manager: WebsiteManager,
    args: ArgParser,
    solver_map: SolverMap,
):
    # Get the puzzle input and answer callback
    puzzle_input = None
    answer_callback: AnswerCallback = noop
    if args.mode == "actual":
        puzzle_input = website_manager.get_actual_input(args.day, args.year)
        answer_callback = partial(
            WebsiteManager.submission_prompt, website_manager, args.day, args.year
        )
    elif args.mode == "example":
        puzzle_input = website_manager.get_example_input(args.day, args.year)
        print(puzzle_input)
        answer_callback = partial(
            WebsiteManager.verify_example_answer, website_manager, args.day, args.year
        )
    else:
        with open(args.mode, "r") as input_file:
            puzzle_input = input_file.read()

    if puzzle_input is None:
        print("No puzzle input. Exiting...")
        return

    # Get the solver
    padded_day = str(args.day).rjust(2, "0")
    solver = solver_map.get(
        (args.day, args.year),
        import_module(f"solvers.year{args.year}.day{padded_day}.solver"),
    )

    print(f"{padded_day}/{args.year}: {args.mode}\n")
    evaluate(solver, puzzle_input, set(), answer_callback)


def main(SESSION_TOKEN: str, args: ArgParser):
    # Connect to the Launcher
    pipe = os.open(args.pipe, os.O_RDWR)
    os.dup2(
        pipe,
        sys.stdin.fileno(),
    )

    website_manager = WebsiteManager(SESSION_TOKEN)

    solver_map = {}
    run_day(website_manager, args, solver_map)

    run_count = 1
    # Now start the event loop
    running = True
    while running:
        command = input()
        if command in ["run", "r"]:
            os.system("clear")
            print(f"Run count: {run_count}")
            run_count += 1
            run_day(website_manager, args, solver_map)
        elif command.startswith("set-day"):
            args.day = int(command[7:])
        elif command.startswith("set-year"):
            args.year = int(command[7:])


if __name__ == "__main__":
    load_dotenv()
    SESSION_TOKEN = getenv("ADVENT_OF_CODE_SESSION")
    if SESSION_TOKEN is None:
        print("ERROR: 'ADVENT_OF_CODE_SESSION' env variable is not set.")
        exit(1)

    args = ArgParser().parse_args()

    try:
        main(SESSION_TOKEN, args)
    except Exception:
        traceback.print_exc()
        if args.mode == "actual":
            input()
        else:
            print("Crashed, closing...")
            time.sleep(2)
