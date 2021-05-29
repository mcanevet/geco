from geco import main, create_parser
import pathlib
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
        with pytest.raises(SystemExit):
            self.parser.parse_args()

    def test_parse_args_with_verbose_short(self):
        args = self.parser.parse_args(["-v", "-p", "examples/x230"])
        assert(args == Namespace(verbose=True,
                                 profile=pathlib.PosixPath("examples/x230")))

    def test_parse_args_with_verbose_long(self):
        args = self.parser.parse_args(["--verbose",
                                       "--profile", "examples/x230"])
        assert(args == Namespace(verbose=True,
                                 profile=pathlib.PosixPath("examples/x230")))

    def test_parse_args_with_profile_short(self):
        args = self.parser.parse_args(["-p", "examples/x230"])
        assert(args == Namespace(verbose=False,
                                 profile=pathlib.PosixPath("examples/x230")))

    def test_parse_args_with_profile_long(self):
        args = self.parser.parse_args(["--profile", "examples/x230"])
        assert(args == Namespace(verbose=False,
                                 profile=pathlib.PosixPath("examples/x230")))
