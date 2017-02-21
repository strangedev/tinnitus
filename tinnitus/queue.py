import threading


class Queue(object):

    __lock = threading.Lock()
    __items = dict({})
    __queue = []
    __current = None

    def __init__(self): pass


    @property
    def current(self):
        id = None
        mrl = ""
        backend = ""
        with self.__lock:
            id = self.__current
            mrl = self.__items[id]["mrl"]
            backend = self.__items[id]["backend"]
        return id, mrl, backend


    def add(self, resource_id: int, mrl: str, backend: str) -> None:

        with self.__lock:
            self.__queue.append(resource_id)
            self.__items[resource_id] = {"mrl": mrl, "backend": backend}


    def remove(self, resource_id: int) -> None:

        with self.__lock:
            if resource_id in self.__items.keys():
                self.__queue.remove(resource_id)
                del self.__items[resource_id]


    def next(self):

        with self.__lock:
            if self.__current is not None:
                del self.__items[self.__current]

            if len(self.__queue) > 0:
                self.__current = self.__queue.pop(0)

            else:
                self.__current = None


    def put_back(self):

        with self.__lock:
            self.__queue.insert(0, self.__current)
            self.__current = None