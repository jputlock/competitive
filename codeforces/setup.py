
import argparse


def main():
    parser = argparse.ArgumentParser(description="Set up a new CodeForces competition folder.")
    parser.add_argument(
        "name",
        help="The round name or number"
    )

    parser.parse_args()

if __name__ == "__main__":
    main()