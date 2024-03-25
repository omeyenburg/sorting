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

        self.iterations = 0
        self.comparisons = 0

        self.highlight_colored = ()
        self.highlight_sorted = ()

        self.starting_time = time.time()
        self.time = 0

    def __del__(self):
        if not self.thread is None:
            self.done = True
            self.thread.join()

    def swap(self, array, first, second):
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

        self.starting_time = time.time()
        self.running = True
        self.paused = False
        self.thread.start()

    def thread_wait(self):
        if self.abort:
            raise SystemExit()

        if self.paused:
            while self.paused:
                pass
            return

        time.sleep(self.delay)

    @staticmethod
    def shuffle(array):
        for i in range(len(array) - 1):
            j = random.randint(i, len(array) - 1)
            array[i], array[j] = array[j], array[i]

    @staticmethod
    def shuffle_slight(array):
        ...
