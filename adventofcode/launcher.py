from argparse import ArgumentParser, FileType
from libtmux.server import Server
from libtmux.session import Session
from libtmux.window import Window
from pathlib import Path
from termcolor import colored
from typing import *

import datetime
import os
import shutil
import sys


class TmuxManager:
    """
    Manages all of the processes spawned by the AdventLauncher.
    """

    def __init__(self, pipe1_name: str, pipe2_name: str):
        """
        Initializes the tmux server.
        """
        self._server = Server()
        self.pipe1_name = pipe1_name
        self.pipe2_name = pipe2_name

    def start(self, day: int, year: int, input):
        """
        Splits the terminal into 3 panes.
        """
        sessions = self._server.sessions.filter(session_name="advent")
        if len(sessions) != 1:
            print(
                colored("ERROR", "red", attrs=["bold"]),
                f"Please run the launcher script instead of the python file directly.",
                file=sys.stderr,
            )
            exit(1)

        self._session: Session = sessions[0]
        self._window: Window = self._session.attached_window

        # Only pane
        self.console_pane = self._window.attached_pane
        if self.console_pane is None:
            exit()

        CMD = f"python3 run_solver.py --day {day} --year {year}"

        left_command = " ".join(
            [
                CMD,
                f"--mode {input or 'actual'}",
                f"--pipe {self.pipe1_name}",
            ]
        )
        right_command = " ".join(
            [
                CMD,
                f"--mode example",
                f"--pipe {self.pipe2_name}",
            ]
        )

        # console = top, left = bottom
        self.left_pane = self._window.split_window(
            attach=False, vertical=True, shell=left_command, percent=20
        )

        # console = top-left, left = bottom, right = top-right
        self.right_pane = self._window.split_window(
            attach=False, vertical=False, shell=right_command
        )

        window_index = self._window.index or "0"
        console_index = self.console_pane.index or "0"
        left_index = int(console_index) + 2  # self.left_pane.index is wrong...

        # Swap console & left pane -> console = bottom, left = left, right = right
        src = f"{window_index}.{console_index}"
        dst = f"{window_index}.{left_index}"
        self._window.cmd("swap-pane", "-s", src, "-t", dst)
        self._window.select_pane(self.console_pane.id)

    def quit(self):
        # Each time we delete a window, each of the indices goes down, so we can just keep removing
        # the 0 index.
        self._window.cmd(f"kill-pane", "-t", "0")
        self._window.cmd(f"kill-pane", "-t", "0")
        self._window.cmd(f"kill-pane", "-t", "0")


class AdventLauncher:
    tmux_manager: TmuxManager

    PIPE1_NAME: str = "advent-1"
    PIPE2_NAME: str = "advent-2"

    def __init__(self, args):
        # Setup pipes for runners to use
        self.setup_pipes()

        # Create and start the tmux manager
        self.tmux_manager = TmuxManager(self.PIPE1_NAME, self.PIPE2_NAME)
        self.tmux_manager.start(args.day, args.year, args.input)

    def setup_pipes(self):
        try:
            os.mkfifo(self.PIPE1_NAME)
        except:
            pass

        try:
            os.mkfifo(self.PIPE2_NAME)
        except:
            pass

        self.pipe1 = os.fdopen(os.open(self.PIPE1_NAME, os.O_RDWR), "w")
        self.pipe2 = os.fdopen(os.open(self.PIPE2_NAME, os.O_RDWR), "w")

    def start_repl(self, day: int, year: int):
        padded_day = str(day).rjust(2, "0")

        waiting_input = True

        print("> ", end="")

        while True:
            command = input().lower()
            os.system("clear")

            if command in ["quit", "q"]:
                self.quit()
            elif not waiting_input:
                if command in ["run", "r"]:
                    print(f"Running {padded_day}/{year}\n> ", end="")
                    print(command, file=self.pipe1, flush=True)
                    print(command, file=self.pipe2, flush=True)
                    waiting_input = True
                elif command == "get-date":
                    print(f"Selected date: {padded_day}-{year}")
                elif command.startswith("set-day"):
                    day = int(command[7:])
                    padded_day = str(day).rjust(2, "0")
                    print(command, file=self.pipe1, flush=True)
                    print(command, file=self.pipe2, flush=True)
                    print(f"Set date to {padded_day}/{year}\n$ ", end="")
                elif command.startswith("set-year"):
                    year = int(command[7:])
                    print(command, file=self.pipe1, flush=True)
                    print(command, file=self.pipe2, flush=True)
                    print(f"Set date to {padded_day}/{year}\n$ ", end="")
                else:
                    print("Unknown command.\n$ ", end="")
            else:
                waiting_input = False
                print(command, file=self.pipe1, flush=True)
                print(f"$ ", end="")

    def quit(self):
        # Cleanup the named pipes
        self.pipe1.close()
        self.pipe2.close()
        os.remove(self.PIPE1_NAME)
        os.remove(self.PIPE2_NAME)

        # Cleanup tmux
        self.tmux_manager.quit()


def copy_templates(year: int):
    template_path = Path(f"template.py")
    if not template_path.exists():
        print(
            colored("WARNING", "yellow", attrs=["bold"]),
            f"Cannot find template file",
            file=sys.stderr,
        )
        return

    for day in range(1, 26):
        padded_day = str(day).rjust(2, "0")
        solver_path = Path(f"solvers/year{year}/day{padded_day}/solver.py")

        if solver_path.exists():
            print(f"Solver already exists for day {day}. Skipping...")
            continue

        # Copy the template file to the solver path
        solver_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(template_path, solver_path)
        print(f"Copied template file to {solver_path}")


def perform_parsing():
    parser = ArgumentParser(description="Solves an Advent of Code puzzle.")
    parser.add_argument(
        "--day",
        "-d",
        default=datetime.date.today().day,
        help="which day the puzzle is from",
        type=int,
    )
    parser.add_argument(
        "--year",
        "-y",
        default=datetime.date.today().year,
        help="which year the puzzle is from",
        type=int,
    )

    # A user should not be able to do more than one of the following at the same
    # time:
    #
    # - Attempt to use the example puzzle input
    # - Manually provide the puzzle input
    # - Submit the actual answer to https://adventofcode.com
    input_group = parser.add_mutually_exclusive_group()
    # input_group.add_argument(
    #     "--example",
    #     "-e",
    #     action="store_true",
    #     default=False,
    #     help="attempts to use the example puzzle input",
    # )
    input_group.add_argument(
        "--input", "-i", help="path to the puzzle input", type=FileType("r")
    )
    input_group.add_argument(
        "--init",
        action="store_true",
        help="initializes the solver for the year",
    )

    parser.add_argument(
        "--part",
        "-p",
        action="append",
        choices=[1, 2],
        help="which part(s) to solve",
        type=int,
    )
    return parser.parse_args()


def main():
    args = perform_parsing()

    if args.init:
        copy_templates(int(args.year))
        return

    launcher = AdventLauncher(args)
    launcher.start_repl(args.day, args.year)


if __name__ == "__main__":
    main()
