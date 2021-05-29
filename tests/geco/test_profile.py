import pytest
from geco.profile import Profile


def test_init():
    profile = Profile("examples/x230")
    assert profile.path == "examples/x230"
    assert profile.efi_dir == "examples/x230/EFI"


def test_load_success():
    profile = Profile("examples/x230")
    profile.load()


def test_load_failure():
    profile = Profile("unexisting_profile")
    with pytest.raises(IOError):
        profile.load()
