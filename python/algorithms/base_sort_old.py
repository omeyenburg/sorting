import threading
import random
import psutil
import time
import os


class BaseSort:
    variants = {}

    def __init__(self):
        self.delay = None
        self.thread = None
        self.status = "Running"
        self.reset()

        self.variants = self.__class__.variants
        if self.variants:
            self.variant = list(self.variants)[0]
            self.variant_func = self.variants[self.variant]
        else:
            self.variant = None
            self.variant_func = None

    def reset(self):
        self.paused = True
        self.sorted = False
        self.running = False
        self.should_abort = False
        self.status = "Ready"

        self.time = 0
        self.time_last = time.time()
        self.time_approximation = 0

        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0
        self.memory = 0

        self.highlight_index = ()
        self.highlight_group = ()

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
        self.status = "Running"
        self.time_last = time.time()
        self.thread.start()

    def thread_wrapper(self, array):
        try:
            self.thread_wait()
            self.sort(array)
            self.sorted = True
            self.status = "Sorted"
        #except Exception as e:
        #    self.status = e.__class__.__name__
        finally:
            self.highlight_index = ()
            self.highlight_group = ()
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

        # Memory is shared between threads
        # TODO:
        # 1. Replace thread with separate process
        # 2. Move measurement to main process and use pid to identify child process
        # pid = os.getpid()
        # python_process = psutil.Process(pid)
        # self.memory = python_process.memory_info().rss / 2**20

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
        for _ in range(len(array) * 10):
            i = random.randint(0, len(array) - 2)
            array[i], array[i+1] = array[i+1], array[i]
