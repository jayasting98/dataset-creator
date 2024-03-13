import argparse
import json
import logging

import dotenv

from dataset_creator import argument_parsers
from dataset_creator import creator_factories


def main(args: argparse.Namespace) -> None:
    dotenv.load_dotenv()
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=args.loglevel.upper(),
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    config_file_pathname: str = args.config_path
    with open(config_file_pathname) as config_file:
        config = json.load(config_file)
    creator_factory_cls: type[creator_factories.CreatorFactory] = args.creator
    creator_factory = creator_factory_cls(config, args)
    loader = creator_factory.create_loader()
    saver = creator_factory.create_saver()
    processor = creator_factory.create_processor(loader, saver)
    processor.process()


if __name__ == '__main__':
    parser = argument_parsers.create_parser()
    args = parser.parse_args()
    main(args)
