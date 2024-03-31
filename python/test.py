from multiprocessing import Process, Pipe
import resource
import psutil
import time
import os


class classproperty(property):
    def __get__(self, cls, owner):
        return staticmethod(self.fget).__get__(None, owner)()


class SortingAlgorithm:
    def __init__(self, array, conn):
        self.array = array
        self.conn = conn
        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0
        self.memory = 0
        self.delay = 0
        self.status = "Ready"
        self.variant = 0
        self.paused = True
        self.sorted = False
        self.running = False
        self.should_abort = False
        self.time = 0
        self.time_last = time.time()
        self.time_approximation = 0
        self.highlight_index = ()
        self.highlight_group = ()


def process(data, conn2):
    print("Begin memory:", resource.getrusage(
        resource.RUSAGE_SELF).ru_maxrss / 2**20)
    begin_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    iterations = 0
    comparisons = 0

    a = []

    for i in range(len(data)):
        # Perform sorting operations and update iteration and comparison counts
        # Here the data at the index is sorted by an algorithm, which is irrelevant for the example
        comparisons += 1
        iterations += 1
        ...

        # Send data (in this example only index i)
        conn2.send(i)
        print("Sending:", i)

        pid = os.getpid()
        python_process = psutil.Process(pid)
        # print("Memory:", python_process.memory_info().rss / 2**20)
        print("Memory:", (resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss - begin_memory) / 1024**2)
        # print(resource.getrusage(resource.RUSAGE_SELF))
        a.extend(data * 100)
        if i > 10:
            a = []

    conn2.close()


def f():
    a = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20

    array = [x for x in range(100_000_000)]

    b = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20

    print(a, b, b-a)


if __name__ == '__main__' and 0:
    p = Process(target=f)
    p.start()
    p.join()

    conn1, conn2 = Pipe(True)  # duplex = True --> bidirectional
    data = [2, 1, 5, 9, 7, 4, 3, 6, 8, 0] * 10
    data = ()

    p = Process(target=process, args=(data, conn2))
    p.start()
    print("Process id:", p.pid)

    latest_update = None

    while p.is_alive():
        print("\nPolling")
        while conn1.poll():
            latest_update = conn1.recv()

        if not latest_update is None:
            print("Received:", latest_update, "\n")
            latest_update = None

        time.sleep(0.01)

    print("\nDone")

    p.join()
    conn1.close()
