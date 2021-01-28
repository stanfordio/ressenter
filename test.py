import ressenter
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Process command line options in conflicting_module.py."
)
parser.add_argument("--conflicting", "-c")
parser.parse_args(sys.argv)
