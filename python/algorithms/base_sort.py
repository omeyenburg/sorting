import threading
import random
import time


class BaseSort:
    def __init__(self):
        self.delay = None
        self.thread = None
        self.reset()

    def reset(self):
        self.paused = True
        self.sorted = False
        self.running = False
        self.should_abort = False

        self.time = 0
        self.time_last = time.time()
        self.time_approximation = 0

        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0

        self.highlight_colored = ()
        self.highlight_sorted = ()

        self.abort()

    def sort_threaded(self, array):
        if not self.thread is None:
            self.should_abort = True
            self.thread.join()
            self.should_abort = False

        self.reset()

        self.thread = threading.Thread(
            target=self.thread_wrapper,
            args=[array],
            daemon=True,
        )

        self.running = True
        self.paused = False
        self.time_last = time.time()
        self.thread.start()

    def thread_wrapper(self, array):
        try:
            self.thread_wait()
            self.sort(array)
            self.highlight_colored = ()
            self.highlight_sorted = ()
            self.sorted = True
        finally:
            self.running = False

        return array

    def thread_wait(self):
        if self.should_abort:
            self.running = False
            raise SystemExit()

        if self.paused:
            time_current = time.time()
            self.time += time_current - self.time_last

            while self.paused:
                if self.should_abort:
                    self.running = False
                    raise SystemExit()

            self.time_last = time.time()
            return

        time.sleep(self.delay)

        time_current = time.time()
        self.time += time_current - self.time_last
        self.time_last = time_current

    def abort(self):
        if not self.thread is None:
            self.should_abort = True
            self.thread.join()
            self.thread = None
            self.should_abort = False
            self.running = False

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
        for _ in range(len(array) * 2):
            i = random.randint(0, len(array) - 2)
            array[i], array[i+1] = array[i+1], array[i]

