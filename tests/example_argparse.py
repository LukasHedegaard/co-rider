# argparse_example.py
from argparse import ArgumentParser

from corider import Configs

parser = ArgumentParser(add_help=True)
parser.add_argument(
    "--defined_with_argparse",
    default=42,
    choices=(42, 1337),
    type=int,
    help="Nonsensical parameter defined for demo purposes.",
)

c2 = Configs.from_argument_parser(parser)

c2.add(
    name="defined_with_corider",
    type=int,
    default="lit",
    strategy="choice",
    description="Another parameter for demo purposes",
    choices=["lit", "woke"],
)

new_parser = c2.add_argparse_args(ArgumentParser(add_help=True))

new_parser.parse_args()
