from __future__ import annotations


class DummyContextManager:
    def __init__(self: DummyContextManager) -> None:
        pass

    def __enter__(self: DummyContextManager) -> None:
        pass

    def __exit__(self: DummyContextManager, exc_type, exc_value, exc_tb) -> None:
        pass
