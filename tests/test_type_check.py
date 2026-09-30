"""
Type check validation for jsonport using mypy API.
"""

from mypy import api


def test_mypy_typecheck():
    """Verify that jsonport passes mypy typecheck with strict settings."""
    stdout, stderr, exit_status = api.run(
        ["jsonport", "tests", "--config-file", "pyproject.toml"]
    )
    assert exit_status == 0, f"Mypy typecheck failed:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
