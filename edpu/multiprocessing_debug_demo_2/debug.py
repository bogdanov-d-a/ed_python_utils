from __future__ import annotations
from . import mp_global as MPG
from enum import Enum, auto
from typing import Any, Optional


class Thread(Enum):
    MAIN = auto()
    WORKER1 = auto()
    WORKER2_A = auto()
    WORKER2_B = auto()


class Location(Enum):
    START = auto()
    END = auto()


_Mode = Optional[tuple[Thread, Location]]


_mode: _Mode = None

def _key_check(key: Any) -> bool:
    return False


def no_thread_wait() -> bool:
    return _mode is None or _mode == (Thread.MAIN, Location.END)


class ThreadNode:
    def __init__(self: ThreadNode, value: Thread, children: list[ThreadNode]=[]) -> None:
        self.value = value
        self.parent: Optional[ThreadNode] = None

        for child in children:
            child.parent = self

        self.children = children

    def _find_down(self: ThreadNode, value: Thread) -> Optional[ThreadNode]:
        if self.value == value:
            return self

        for child in self.children:
            result = child._find_down(value)
            if result:
                return result

        return None

    def find_down(self: ThreadNode, value: Thread) -> ThreadNode:
        result = self._find_down(value)
        if result is None:
            raise Exception()
        return result

    def find_all_children(self: ThreadNode) -> set[Thread]:
        result: set[Thread] = set([self.value])

        for child in self.children:
            result |= child.find_all_children()

        return result

    def find_all_parents(self: ThreadNode) -> set[Thread]:
        node = self
        result: set[Thread] = set()

        while True:
            if node.parent is None:
                return result

            node = node.parent
            result.add(node.value)


_tree =  ThreadNode(
    Thread.MAIN,
    [
        ThreadNode(Thread.WORKER1, [
            ThreadNode(Thread.WORKER2_A),
            ThreadNode(Thread.WORKER2_B),
        ]),
    ]
)


def thread(thread: Thread, location: Location, key: Any) -> None:
    if thread == Thread.MAIN:
        raise Exception()

    if _mode is None:
        return

    if no_thread_wait():
        return

    if thread in _tree.find_down(_mode[0]).find_all_parents():
        return

    if _mode[1] == Location.END:
        if _mode[0] == thread and location == Location.START:
            return

        children = _tree.find_down(_mode[0]).find_all_children()
        children.remove(_mode[0])

        if thread in children:
            return

    MPG.introduce_and_pop_pass(
        MPG.PmKey.DEBUG if (_mode == (thread, location) and _key_check(key)) else MPG.PmKey.WAIT,
        str((thread, location, key))
    )


def main(location: Location) -> None:
    if _mode is None:
        return

    if _mode == (Thread.MAIN, location):
        from ..concurrency_debug.utils import wait_for_input
        wait_for_input(str((Thread.MAIN, location)))


def before_fork(thread: Thread) -> None:
    if _mode is None:
        return

    if _mode == (thread, Location.START):
        raise Exception('before_fork')


def before_results_main() -> None:
    if not no_thread_wait():
        CALLER = 'before_results_main'
        MPG.user_interaction_control(MPG.PmKey.DEBUG, CALLER)
        MPG.release(MPG.PmKey.WAIT, CALLER)
