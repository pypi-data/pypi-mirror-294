from socket import socket
from heapq import heappush, heappop
from typing import Callable, Dict, List, Optional, Tuple
from datetime import timedelta
import select
import time

class TimerEvent:
    __slots__ = ('time', 'interval', 'callback')

    def __init__(self, time: float, interval: float, callback: Callable[[], bool]) -> None:
        self.time = time
        self.interval = interval
        self.callback = callback

    def __lt__(self, other) -> bool:
        return self.time < other.time

class EventLoop:
    IN = getattr(select, 'EPOLLIN')
    OUT = getattr(select, 'EPOLLOUT')
    ERROR = getattr(select, 'EPOLLERR')
    HANGUP = getattr(select, 'EPOLLHUP')

    def __init__(self) -> None:
        self._fds : Dict[int, Callable[[], bool]] = {}
        self._poller = select.epoll()
        self._timers : List[Tuple[float, float, Callable[[], bool]]] = []

    def add_fd(self, fd: int, event_mask: int, callback: Callable[[int], bool]) -> None:
        self._fds[fd] = callback
        self._poller.register(fd, event_mask)

    def add_socket(self, s: socket, event_mask: int, callback: Callable[[int], bool]) -> None:
        self.add_fd(s.fileno(), event_mask, callback)

    def add_looping_timer(self, interval: timedelta, callback: Callable[[], bool]) -> None:
        heappush(self._timers, TimerEvent(time.monotonic() + interval.total_seconds(), interval.total_seconds(), callback))
    
    def defer(self, interval: timedelta, callback: Callable[[], None]) -> None:
        # "and False" forces the timer to deschedule
        self.add_looping_timer(interval, lambda callback=callback: callback() and False)

    def post(self, callback: Callable[[], None]) -> None:
        self.defer(timedelta(), callback)

    def poll(self, timeout: Optional[timedelta] = None) -> int:
        num_polled = 0
        #time_to_wait = (timeout.total_seconds() * 1000) if timeout is not None else None
        time_to_wait = timeout.total_seconds() if timeout is not None else None

        if self._timers:
            next_timer_time = self._timers[0].time
            now = time.monotonic()
            if next_timer_time <= now:
                time_to_wait = 0
            else:
                time_to_wait = (min(next_timer_time - now, timeout.total_seconds()) if timeout is not None else (next_timer_time - now))# * 1000

        for fd, evt in self._poller.poll(time_to_wait):
            callback = self._fds[fd]

            continue_running = callback(evt)
            num_polled += 1
            if not continue_running:
                self._poller.unregister(fd)
                del self._fds[fd]

        # Only process the events pertaining to this point in time,
        # otherwise we end up in an endless loop if we constantly check time
        now = time.monotonic()
        while self._timers and now >= self._timers[0].time:
            e = heappop(self._timers)

            continue_running = e.callback()
            if continue_running:
                e.time = time.monotonic() + e.interval
                heappush(self._timers, e)
            num_polled += 1

        return num_polled
