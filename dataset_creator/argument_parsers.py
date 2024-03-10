import argparse
from typing import Any
from typing import Callable
from typing import Self
from typing import Sequence
from typing import TypedDict


class _ConvertChoiceAction(argparse.Action):
    _dest_choice_objects: dict[str, dict[str, Any]] = dict()

    @classmethod
    def add_dest_choice_object(
        cls: type[Self],
        argument: str,
        choice: str,
        choice_object: Any,
    ) -> None:
        if argument not in cls._dest_choice_objects:
            cls._dest_choice_objects[argument] = dict()
        cls._dest_choice_objects[argument][choice] = choice_object

    def __call__(
        self: Self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        choice_object = (
            self.__class__._dest_choice_objects[option_string][values])
        setattr(namespace, self.dest, choice_object)


class _ArgumentInfo(TypedDict, total=False):
    choices: dict[str, Any]


class _ParserInfo(TypedDict):
    subparsers: dict[str, '_ParserInfo']
    arguments: dict[str, _ArgumentInfo]


_parser_info: _ParserInfo = _ParserInfo(subparsers=dict(), arguments=dict())
_parser_info['arguments']['--config_path'] = _ArgumentInfo()
_parser_info['arguments']['--loglevel'] = _ArgumentInfo()


def parser_argument_choice(
    argument: str,
    choice: str,
    *subcommand_names: str,
    parser_info: _ParserInfo = _parser_info,
) -> Callable[[type], type]:
    p_info = parser_info
    def parser_argument_choice_decorator(cls: type) -> type:
        parser_info = p_info
        for subcommand_name in subcommand_names:
            subparser_infos = parser_info['subparsers']
            if subcommand_name not in subparser_infos:
                subparser_infos[subcommand_name] = (
                    _ParserInfo(subparsers=dict(), arguments=dict()))
            parser_info = subparser_infos[subcommand_name]
        argument_infos = parser_info['arguments']
        if argument not in argument_infos:
            argument_infos[argument] = _ArgumentInfo(choices=dict())
        argument_info = argument_infos[argument]
        choices = argument_info['choices']
        choices[choice] = cls
        _ConvertChoiceAction.add_dest_choice_object(argument, choice, cls)
        return cls
    return parser_argument_choice_decorator


def create_parser(
    parser: argparse.ArgumentParser = None,
    parser_info: _ParserInfo = _parser_info,
) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser()
    for name, argument_info in parser_info['arguments'].items():
        extra_info = dict()
        if 'choices' in argument_info:
            extra_info['action'] = _ConvertChoiceAction
        parser.add_argument(name, **argument_info, **extra_info)
    subparsers = parser.add_subparsers()
    for name, subparser_info in parser_info['subparsers'].items():
        subparser = subparsers.add_parser(name)
        create_parser(parser=subparser, parser_info=subparser_info)
    return parser
