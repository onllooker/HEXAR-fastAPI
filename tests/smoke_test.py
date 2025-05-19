# import pytest


def test_import_app() -> None:
    from app.api.api import app

    assert app is not None
