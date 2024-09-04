import pytest


def test_import():

    try:
        import pythonlemmy
    except ModuleNotFoundError as ex:
        pytest.fail(f"{ex}")
