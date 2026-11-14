import pytest

from app import llm_guard


@pytest.fixture(autouse=True)
def _reset_llm_guard():
    """Each test starts with a fresh Nemotron quota (the guard is per-IP, and every test is 'testclient')."""
    llm_guard.reset()
    yield
    llm_guard.reset()
