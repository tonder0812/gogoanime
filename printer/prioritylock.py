import queue
import threading
from types import TracebackType

from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


"""
Sligtly modified PriorityLock from
https://gist.github.com/timofurrer/db44ad05ffffd74f73384e2eb0bfb682
"""


class PriorityLock:
    """Lock object which prioritizes each acquire
    >>> import random
    >>> thread_exec_order = []
    >>> lock = PriorityLock()
    >>> def worker(priority):
    ...     with lock(priority):
    ...         time.sleep(0.2)
    ...         thread_exec_order.append(priority)
    >>> threads = [
    ...     threading.Thread(target=worker, args=(p,))
    ...     for p in range(10)
    ... ]
    >>> random.shuffle(threads)
    >>> for thread in threads:
    ...     thread.start()
    >>> for thread in threads:
    ...     thread.join()
    >>> # the first thread to be executed is non-deterministic
    >>> assert thread_exec_order[1:] == list(sorted(thread_exec_order[1:]))
    """

    class _Context:
        def __init__(self, lock: "PriorityLock", priority: int):
            self._lock = lock
            self._priority = priority

        def __enter__(self):
            self._lock.acquire(self._priority)

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ):
            self._lock.release()

    def __init__(self):
        self._lock = threading.Lock()
        self._acquire_queue: queue.PriorityQueue[
            PrioritizedItem
        ] = queue.PriorityQueue()
        self._need_to_wait = False

    def acquire(self, priority: int):
        with self._lock:
            if not self._need_to_wait:
                self._need_to_wait = True
                return True
            event = threading.Event()
            self._acquire_queue.put(PrioritizedItem(priority, event))
        event.wait()
        return True

    def release(self):
        with self._lock:
            try:
                event = self._acquire_queue.get_nowait().item
            except queue.Empty:
                self._need_to_wait = False
            else:
                event.set()

    def __call__(self, priority: int):
        return self._Context(self, priority)


class PriorityRLock:
    class _Context:
        def __init__(self, lock: "PriorityRLock", priority: int):
            self._lock = lock
            self._priority = priority

        def __enter__(self):
            self._lock.acquire(self._priority)

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ):
            self._lock.release()

    def __init__(self) -> None:
        self._lock = PriorityLock()
        self._owner = None
        self._count = 0

    def acquire(self, priority: int = 0):
        me = threading.get_ident()
        if self._owner == me:
            self._count += 1
            return 1
        rc = self._lock.acquire(priority)
        if rc:
            self._owner = me
            self._count = 1
        return rc

    __enter__ = acquire

    def release(self):
        if self._owner != threading.get_ident():
            raise RuntimeError("cannot release un-acquired lock")
        self._count = count = self._count - 1
        if not count:
            self._owner = None
            self._lock.release()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self.release()

    def __call__(self, priority: int):
        return self._Context(self, priority)
