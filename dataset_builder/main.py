import argparse


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace) -> None:
    pass


if __name__ == '__main__':
    args = _parse_args()
    main(args)
