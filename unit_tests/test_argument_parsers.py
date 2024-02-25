import unittest

from dataset_creator import argument_parsers


class ArgumentParserTest(unittest.TestCase):
    def test_parser_argument_choice__zero_subcommands__adds_choice(self):
        parser_info = (
            argument_parsers._ParserInfo(subparsers=dict(), arguments=dict()))
        @argument_parsers.parser_argument_choice(
            '--arg', 'choice',
            parser_info=parser_info)
        class MyClass:
            pass
        actual_cls = parser_info['arguments']['--arg']['choices']['choice']
        self.assertIs(MyClass, actual_cls)

    def test_parser_argument_choice__one_subcommand__adds_choice(self):
        parser_info = (
            argument_parsers._ParserInfo(subparsers=dict(), arguments=dict()))
        @argument_parsers.parser_argument_choice(
            '--arg', 'choice', 'subcommand',
            parser_info=parser_info)
        class MyClass:
            pass
        subparser_info = parser_info['subparsers']['subcommand']
        actual_cls = subparser_info['arguments']['--arg']['choices']['choice']
        self.assertIs(MyClass, actual_cls)

    def test_parser_argument_choice__two_subcommands__adds_choice(self):
        parser_info = (
            argument_parsers._ParserInfo(subparsers=dict(), arguments=dict()))
        @argument_parsers.parser_argument_choice(
            '--arg', 'choice', 'subcommand1', 'subcommand2',
            parser_info=parser_info)
        class MyClass:
            pass
        subparser1_info = parser_info['subparsers']['subcommand1']
        subparser2_info = subparser1_info['subparsers']['subcommand2']
        actual_cls = subparser2_info['arguments']['--arg']['choices']['choice']
        self.assertIs(MyClass, actual_cls)

    def test_create_parser__typical_case__creates_parser(self):
        parser_info = (
            argument_parsers._ParserInfo(subparsers=dict(), arguments=dict()))
        @argument_parsers.parser_argument_choice(
            '--arg', 'choice', 'subcommand',
            parser_info=parser_info)
        class MyClass:
            pass
        parser = argument_parsers.create_parser(parser_info=parser_info)
        namespace = parser.parse_args(['subcommand', '--arg', 'choice'])
        self.assertIs(MyClass, namespace.arg)
