import threading
import random
import time


class BaseSort:
    def __init__(self):
        self.delay = None
        self.reset()

    def reset(self):
        self.thread = None
        self.paused = True
        self.abort = False
        self.sorted = False
        self.running = False

        self.time = 0
        self.time_last = time.time()
        self.time_approximation = 0

        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0

        self.highlight_colored = ()
        self.highlight_sorted = ()

        #self.starting_time = time.time()

    def __del__(self):
        if not self.thread is None:
            self.done = True
            self.thread.join()

    def swap(self, array, first, second):
        self.reads += 2
        self.writes += 2

        a = array[first]
        array[first] = array[second]
        array[second] = a

    def is_sorted(self, array):
        last = array[0] - 1
        for x in array:
            if x < last:
                return False
            last = x
        return True

    def sort_threaded(self, array):
        if not self.thread is None:
            self.abort = True
            self.thread.join()
            self.abort = False
            print("aborted previous thread")

        self.reset()

        self.thread = threading.Thread(
            target=self.sort,
            args=[array],
            daemon=True,
        )

        self.running = True
        self.paused = False
        self.time_last = time.time()
        self.thread.start()

    def thread_wait(self):
        if self.abort:
            raise SystemExit()

        if self.paused:
            time_current = time.time()
            self.time += time_current - self.time_last

            while self.paused:
                if self.abort:
                    raise SystemExit()

            self.time_last = time.time()
            return

        time.sleep(self.delay)

        time_current = time.time()
        self.time += time_current - self.time_last
        self.time_last = time_current

    def enumerate(self, iterable):
        for var in enumerate(iterable):
            self.reads += 1
            yield var

    @staticmethod
    def shuffle(array):
        for i in range(len(array) - 1):
            j = random.randint(i, len(array) - 1)
            array[i], array[j] = array[j], array[i]

    @staticmethod
    def shuffle_slight(array):
        ...
