import threading

import rpyc
import sys

from tinnitus import Status
from tinnitus.pluggable import Pluggable
from tinnitus.queue import Queue


_status = Status.STOPPED
_queue = Queue()
_pluggable = Pluggable()
_lock = threading.Lock()


def _play_next():
    global _queue
    global _status

    _queue.next()
    id, mrl, backend = _queue.current

    if id < 1:
        _pluggable.backend.stop()

    _pluggable.use_backend(backend)
    _pluggable.backend.set_mrl(mrl)
    _pluggable.backend.play()

    with _lock:
        _status = Status.PLAYING


_pluggable.set_callback(_play_next)


class PlayerService(rpyc.Service):


    def on_connect(self): pass


    def on_disconnect(self): pass


    def exposed_play(self) -> None:
        global _status
        global _lock

        if _status != Status.PLAYING:
            _play_next()

            with _lock:
                _status = Status.PLAYING


    def exposed_pause(self) -> None:
        global _pluggable
        global _status
        global _lock

        if _status != Status.PAUSED:
            _pluggable.backend.pause()

            with _lock:
                _status = Status.PAUSED


    def exposed_stop(self) -> None:
        global _queue
        global _pluggable
        global _status
        global _lock

        if _status != Status.STOPPED:
            _pluggable.backend.stop()
            _queue.put_back()

            with _lock:
                _status = Status.STOPPED


    def exposed_play_next(self) -> None:
        global _status
        global _lock

        if _status != Status.STOPPED:
            _play_next()

            with _lock:
                _status = Status.PLAYING


    def exposed_status(self) -> Status:
        global _status
        global _lock

        status = Status.STOPPED

        with _lock:
            status = _status

        return status


def run_command():

    argc = len(sys.argv)
    port = 18861

    if argc > 2:
        print("Usage...")

    if argc > 1:
        port = sys.argv[1]

    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(PlayerService, port=port)
    t.start()

