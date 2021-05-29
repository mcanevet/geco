from geco import main
import pytest


def test_init_success():
    main()


def test_init_failure():
    with pytest.raises(TypeError):
        main("foo")
