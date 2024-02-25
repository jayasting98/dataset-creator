import argparse

from dataset_creator import argument_parsers


def main(args: argparse.Namespace) -> None:
    pass


if __name__ == '__main__':
    parser = argument_parsers.create_parser()
    args = parser.parse_args()
    main(args)
