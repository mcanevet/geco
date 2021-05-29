from geco.profile import Profile


def test_init():
    profile = Profile("examples/x230")
    assert profile.path == "examples/x230"
    assert profile.efi_dir == "examples/x230/EFI"
