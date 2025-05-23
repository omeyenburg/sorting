from algorithms.selection_sort import SelectionSort
from algorithms.insertion_sort import InsertionSort
from algorithms.bubble_sort import BubbleSort
from algorithms.quick_sort import QuickSort
from algorithms.shell_sort import ShellSort
from algorithms.merge_sort import MergeSort
from algorithms.radix_sort import RadixSort
from algorithms.tree_sort import TreeSort
from algorithms.heap_sort import HeapSort
from algorithms.bogo_sort import BogoSort
from multiprocessing import Process, Manager, Pipe
import resource
import random
import time


STATE_IDLE = 0
STATE_PAUSED = 1
STATE_RUNNING = 2
STATE_SORTED = 3
STATE_RECURSIONERROR = 4
STATE_CONNECTIONERROR = 5


def process_measure_default_memory(conn):
    memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    conn.send(memory)


def process_sort(Algorithm, connection, shared_dict, array, delay, variant):
    algorithm = Algorithm()
    algorithm.connection = connection
    algorithm.shared_dict = shared_dict
    algorithm.array = array
    algorithm.delay = delay
    algorithm.variant = variant

    try:
        algorithm.thread.start()
        algorithm.sort(array)
        algorithm.state = STATE_SORTED
    except RecursionError:
        print("RECURSIONERROR")
        algorithm.state = STATE_RECURSIONERROR

    algorithm.highlight_index = ()
    algorithm.highlight_group = ()
    algorithm.update = True
    algorithm.thread.join()


class SortProcessWrapper:
    def __init__(self):
        self.array_length = 0
        self.array_uniqueness = "Unique"
        self.array = []
        self.algorithm = None
        self.variants = {}
        self.variant = None
        self.shuffle = SelectionSort.shuffle

        # Stats
        self.reset()

        # Process
        self.default_memory = self._get_default_memory()
        self.process = None
        self.shared_dict = Manager().dict()
        self.process_pipe = Pipe()

    def __del__(self):
        self._process_abort()

    def _get_default_memory(self):
        average_default_memory = 0
        n = 5

        conn1, conn2 = Pipe()

        for _ in range(n):
            process = Process(
                target=process_measure_default_memory,
                args=(conn2,),
                daemon=True,
            )
            process.start()
            process.join()

            if not conn1.poll():
                raise SystemExit("Process did not send required data.")
            average_default_memory += conn1.recv()

        conn1.close()
        conn2.close()

        # Peak Memory in Kilobytes
        return int(average_default_memory / n / 1024)

    def _process_start(self):
        args = (
            self.algorithm,
            self.process_pipe[1],
            self.shared_dict,
            self.array,
            self.delay,
            self.variants.get(self.variant, None),
        )

        self.process = Process(
            target=process_sort,
            args=args,
            daemon=True,
        )
        self.process.start()

    def _process_abort(self):
        if self.process is None:
            self.reset()
            return

        if self.process.is_alive():
            self.process.kill()

        self.process = None
        self.reset()

    def _reset_array(self):
        if self.array_uniqueness == "Unique":
            self.array = [i for i in range(self.array_length)]
        else:
            self.array = [
                random.randint(0, self.array_length - 1)
                for _ in range(self.array_length)
            ]

    def reset(self):
        self.time = 0
        self.memory = 0
        self.iterations = 0
        self.comparisons = 0
        self.writes = 0
        self.reads = 0
        self.state = STATE_IDLE

        self.highlight_index = ()
        self.highlight_group = ()

    def toggle_start(self):
        if self.state in (STATE_SORTED, STATE_RECURSIONERROR):
            return
        if self.state == STATE_IDLE:
            self._process_abort()
            self._process_start()
            self.state = STATE_RUNNING
        elif self.state == STATE_PAUSED:
            self.set_state(STATE_RUNNING)
        else:
            self.set_state(STATE_PAUSED)

    def update(self):
        if self.process is None or self.state not in (
            STATE_RUNNING,
            STATE_PAUSED,
            STATE_SORTED,
        ):
            return

        if self.process.exitcode:
            time.sleep(0.5)
            raise SystemExit("Child process failed.")

        for key, value in self.shared_dict.items():
            if key == "memory":
                self.memory = max(0, value - self.default_memory)
            if key == "array":
                self.array = value
            else:
                self.__dict__[key] = value

    def set_algorithm(self, algorithm):
        self._process_abort()
        self.algorithm = algorithm

        self.variants = {}
        for name, func in algorithm.__dict__.items():
            if name.startswith("variant_"):
                self.variants[func.__doc__] = func

        if self.variants:
            self.variant = tuple(self.variants)[0]
        else:
            self.variant = None

    def set_variant(self, variant):
        var = self.variants.get(variant, None)
        if var is not None:
            self._process_abort()
            self.variant = variant

    def set_array_length(self, length):
        self._process_abort()
        self.array_length = length
        self._reset_array()

    def set_delay(self, delay):
        self.delay = delay
        self.process_pipe[0].send({"delay": delay})

    def set_speed(self, value):
        self.set_delay(pow(1 - value, 2))

    def set_state(self, state):
        self.state = state
        self.process_pipe[0].send({"state": state})

    def set_shuffling(self, shuffling):
        if shuffling == "Normal":
            self.shuffle = SelectionSort.shuffle
        elif shuffling == "Slight":
            self.shuffle = SelectionSort.shuffle_slight
        elif shuffling == "Reversed":
            self.shuffle = SelectionSort.shuffle_reversed

    def set_value_uniqueness(self, value):
        self._process_abort()
        self.array_uniqueness = value
        self._reset_array()

    def randomize(self):
        self._process_abort()
        self.shuffle(self.array)

    def pause(self):
        if self.state == STATE_RUNNING:
            self.set_state(STATE_PAUSED)

    def get_state_name(self):
        return (
            "Idle",
            "Paused",
            "Running",
            "Sorted",
            "Recursion Error",
            "Connection Error",
        )[self.state]

    def get_stats(self):
        return [
            f"Time:  {self.time: .5f} s",
            f"Memory: {self.memory} KB",
            f"Iterations:  {self.iterations}",
            f"Comparisons:  {self.comparisons}",
            f"Array Reads:  {self.reads}",
            f"Array Writes:  {self.writes}",
            f"State:  {self.get_state_name()}",
        ]

    @staticmethod
    def get_algorithms():
        return {
            "Selection Sort": SelectionSort,
            "Insertion Sort": InsertionSort,
            "Bubble Sort": BubbleSort,
            "Quick Sort": QuickSort,
            "Shell Sort": ShellSort,
            "Merge Sort": MergeSort,
            "Tree Sort": TreeSort,
            "Heap Sort": HeapSort,
            "Radix Sort": RadixSort,
            "Bogo Sort": BogoSort,
        }

    @classmethod
    def get_algorithm(cls, name):
        return cls.get_algorithms()[name]
