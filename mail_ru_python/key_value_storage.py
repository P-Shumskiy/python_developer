import argparse

parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int)
parser.add_argument("-v", "--verbosity", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
answer = args.square**2
if args.verbosity:
    print(f"square of {args.square} equals {answer}")
else:
    print(answer)