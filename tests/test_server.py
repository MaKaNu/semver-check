import pytest

from semver_check.server import is_valid_semver


@pytest.mark.parametrize(
    "version, expected",
    [
        # Valid SemVer cases
        ("1.0.0", True),
        ("0.1.0", True),
        ("0.0.1", True),
        ("1.0.0-alpha", True),
        ("1.0.0-alpha.1", True),
        ("1.0.0-0.3.7", True),
        ("1.0.0-x.7.z.92", True),
        ("1.0.0-alpha+001", True),
        ("1.0.0+20130313144700", True),
        ("1.0.0-beta+exp.sha.5114f85", True),
        # Invalid SemVer cases
        ("1", False),  # Missing minor and patch
        ("1.0", False),  # Missing patch
        ("1.0.0-", False),  # Trailing dash
        ("1.0.0+", False),  # Trailing plus
        ("1.0.0-+", False),  # Empty pre-release and build
        ("1.0.0-alpha..1", False),  # Double dots
        ("1..0.0", False),  # Double dots in major
        ("-1.0.0", False),  # Negative major version
        ("1.0.0.0", False),  # Extra numeric field
        ("1.0.0-alpha!", False),  # Invalid character in pre-release
    ],
)
def test_is_valid_semver(version, expected):
    assert is_valid_semver(version) == expected
