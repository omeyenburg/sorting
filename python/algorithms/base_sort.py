from threading import Thread
import resource
import random
import time


STATE_IDLE = 0
STATE_PAUSED = 1
STATE_RUNNING = 2
STATE_SORTED = 3
STATE_RECURSIONERROR = 4


class BaseSort:
    def __init__(self):
        self.connection = None
        self.array = None
        self.delay = None
        self.variant = None
        self.update = False

        self.time = 0
        self.memory = 0
        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0
        self.state = STATE_RUNNING

        self.highlight_index = ()
        self.highlight_group = ()

        self.thread = Thread(
            target=self._thread_update,
            daemon=True,
        )

        self.time_last = time.monotonic()

    def wait(self):
        self.update = True

        if self.state == STATE_PAUSED:
            self.time += time.monotonic() - self.time_last

            while self.state == STATE_PAUSED:
                time.sleep(0.01)

            self.time_last = time.monotonic()
            return

        time_current = time.monotonic()
        delta_time = time_current - self.time_last
        self.time += delta_time
        self.time_last = time_current

        time.sleep(max(0, self.delay - delta_time))

    def _thread_update(self):
        while True:
            while self.connection.poll():
                data_recv = self.connection.recv()
                for key, value in data_recv.items():
                    self.__dict__[key] = value

            while not self.update:
                time.sleep(0.01)
            
            if self.state == STATE_PAUSED:
                continue

            self.memory = self._get_memory()
            self._thread_send(self.time + time.monotonic() - self.time_last)

            if self.state in (STATE_SORTED, STATE_RECURSIONERROR):
                break
        
        self.memory = self._get_memory()
        self._thread_send(self.time)

    def _thread_send(self, time):
        data_send = {
            "array": self.array,
            "time": time,
            "memory": self.memory,
            "iterations": self.iterations,
            "comparisons": self.comparisons,
            "reads": self.reads,
            "writes": self.writes,
            "highlight_index": self.highlight_index,
            "highlight_group": self.highlight_group,
        }
        if self.state != STATE_RUNNING:
            data_send["state"] = self.state
        self.connection.send(data_send)
        
    def _get_memory(self):
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 # Memory in KB

    def swap(self, array, first, second):
        self.reads += 2
        self.writes += 2

        a = array[first]
        array[first] = array[second]
        array[second] = a

    def enumerate(self, iterable):
        for var in enumerate(iterable):
            self.reads += 1
            self.iterations += 1
            yield var

    @staticmethod
    def check_sorted(array):
        last = array[0] - 1
        for x in array:
            if x < last:
                return False
            last = x
        return True

    @staticmethod
    def shuffle(array):
        for i in range(len(array) - 1):
            j = random.randint(i, len(array) - 1)
            array[i], array[j] = array[j], array[i]

    @staticmethod
    def shuffle_slight(array):
        array.sort()
        for _ in range(len(array) * 2):
            i = random.randint(0, len(array) - 2)
            array[i], array[i+1] = array[i+1], array[i]

    @staticmethod
    def shuffle_reversed(array):
        array.sort(reverse=True)
        for _ in range(len(array) * 10):
            i = random.randint(0, len(array) - 2)
            array[i], array[i+1] = array[i+1], array[i]
