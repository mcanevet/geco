from geco import main, create_parser
import pytest
import unittest
from argparse import Namespace


def test_init_success():
    main()


def test_init_failure():
    with pytest.raises(TypeError):
        main("foo")


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def test_parse_args_without_args(self):
        args = self.parser.parse_args()
        assert(args == Namespace(verbose=False))

    def test_parse_args_with_verbose_short(self):
        args = self.parser.parse_args(["-v"])
        assert(args == Namespace(verbose=True))

    def test_parse_args_with_verbose_long(self):
        args = self.parser.parse_args(["--verbose"])
        assert(args == Namespace(verbose=True))
