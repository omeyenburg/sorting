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
import pygame.freetype
import pygame
import math
import time


class Page:
    def __init__(self):
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def add_widgets(self, *widgets):
        self.widgets.extend(widgets)

    def update(self, window):
        for widget in self.widgets:
            widget.update(window)


class Label:
    def __init__(self, text, size=20, pos=None, center=None):
        self.text = text
        self.size = size
        self.pos = pos
        self.center = center

    def update(self, window):
        if isinstance(self.text, str):
            lines = self.text.split("\n")
        else:
            lines = self.text

        text_rect = window.font.get_rect(max(lines, key=len), size=self.size)
        if not self.pos is None:
            dest = (self.pos[0] * window.size[0], self.pos[1] * window.size[1])
        else:
            dest = (self.center[0] * window.size[0] - text_rect[2] / 2,
                    self.center[1] * window.size[1] - text_rect[3] / 2)
        for i, line in enumerate(lines):
            window.font.render_to(window.window, (dest[0], dest[1] + 20 * i), line,
                                  (255, 255, 255), size=self.size)


class Button:
    def __init__(self, text, callback, size=20, pos=None, center=None, keep=False, toggled=False):
        self.text = text
        self.size = size
        self.callback = callback
        self.pos = pos
        self.center = center
        self.keep = keep
        self.clicked = toggled

    def update(self, window):
        if not self.pos is None:
            rect = pygame.Rect(
                self.pos[0] * window.size[0], self.pos[1] * window.size[1], 200, 30)
        else:
            rect = pygame.Rect(
                self.center[0] * window.size[0] - 100, self.center[1] * window.size[1] - 15, 200, 30)

        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos) or self.clicked:
            if window.clicked or self.clicked:
                color = (150, 150, 150)
                rect[0] += 2
                rect[1] += 2
                rect[2] -= 4
                rect[3] -= 4
                if window.clicked == 5 and not self.clicked:
                    if self.keep:
                        for widget in window.opened_page.widgets:
                            if isinstance(widget, Button):
                                widget.clicked = False
                        self.clicked = True
                    self.callback()
            else:
                color = (150, 150, 150)
        else:
            color = (100, 100, 100)

        pygame.draw.rect(window.window, color, rect, border_radius=3)

        text_rect = window.font.get_rect(self.text, size=self.size)
        dest = (rect.centerx - text_rect[2] //
                2, rect.centery - text_rect[3] // 2)
        window.font.render_to(window.window, dest, self.text,
                              size=self.size, fgcolor=(255, 255, 255))


class Slider:
    def __init__(self, _range, pos, callback, show=False, integer=False, out=None):
        self.start = _range[0]
        self.end = _range[1]
        self.value = round(_range[2]) if integer else _range[2]
        self.pos = pos
        self.callback = callback
        self.float_value = (self.value - self.start) / (self.end - self.start)
        self.clicked = False
        self.show = show
        self.integer = integer
        self.out = out

    def update(self, window):
        rect = (
            self.pos[0] * window.size[0],
            self.pos[1] * window.size[1] - 2,
            100,
            4,
        )
        pygame.draw.rect(window.window, (100, 100, 100), rect, border_radius=3)

        radius = 8
        circle_pos = (
            rect[0] + self.float_value * rect[2],
            rect[1] + rect[3] / 2
        )
        mouse_pos = pygame.mouse.get_pos()

        if math.dist(circle_pos, mouse_pos) <= radius and window.clicked:
            self.clicked = (
                circle_pos[0] - mouse_pos[0],
                circle_pos[1] - mouse_pos[1]
            )
        elif self.clicked and not any(pygame.mouse.get_pressed()):
            self.clicked = False
            if self.out is None:
                self.callback(self.value)
            else:
                self.callback(self.out(self.value))

        if self.clicked:
            self.float_value = min(
                1,
                max(0, (mouse_pos[0] + self.clicked[0] - rect[0]) / rect[2])
            )
            self.value = (self.start + self.float_value *
                          (self.end - self.start))

            if self.integer:
                self.value = round(self.value)
                self.float_value = ((self.value - self.start) /
                                    (self.end - self.start))
            color = (200, 200, 200)
        else:
            color = (150, 150, 150)

        pygame.draw.circle(window.window, color, circle_pos, radius)
        if self.show:
            if self.out is None:
                text = str(self.value)
            else:
                text = str(self.out(self.value))

            height = window.font.get_rect("A")[3]
            rect = (rect[0] + rect[2] + height, rect[1] - height / 2)
            window.font.render_to(window.window, rect, text, (255, 255, 255))


class SortingChart:
    def __init__(self, values, algorithm):
        self.values = values
        self.algorithm = algorithm()
        self.iteration_delay = 0.5
        self.shuffle = algorithm.shuffle
        self.array = [i for i in values]

    def set_speed(self, value):
        self.iteration_delay = value
        self.algorithm.delay = self.iteration_delay

    def set_count(self, count):
        self.values = range(count)
        self.array = [i for i in self.values]
        self.algorithm.reset()

    def set_shuffling(self, shuffling):
        if shuffling == "Normal":
            self.shuffle = self.algorithm.shuffle
        elif shuffling == "Slight":
            self.shuffle = self.algorithm.shuffle_slight
        elif shuffling == "Reversed":
            self.shuffle = self.algorithm.shuffle_reversed

    def toggle_pause(self):
        self.algorithm.paused = not self.algorithm.paused

    def set_paused(self, value):
        self.algorithm.paused = value

    def reset(self):
        self.shuffle(self.array)
        self.algorithm.reset()

    def run(self):
        if self.algorithm.sorted or len(self.array) <= 1:
            return

        if self.algorithm.running:
            self.algorithm.paused = not self.algorithm.paused
            return

        self.algorithm.delay = self.iteration_delay
        self.algorithm.sort_threaded(self.array)

    @staticmethod
    def get_algorithms():
        return {
            SelectionSort: "Selection Sort",
            InsertionSort: "Insertion Sort",
            BubbleSort: "Bubble Sort",
            QuickSort: "Quick Sort",
            ShellSort: "Shell Sort",
            MergeSort: "Merge Sort",
            TreeSort: "Tree Sort",
            HeapSort: "Heap Sort",
            RadixSort: "Radix Sort",
            BogoSort: "Bogo Sort",
        }

    def update(self, window):
        if self.algorithm.running and not (self.algorithm.sorted or self.algorithm.paused):
            self.algorithm.time_approximation += window.delta_time
            window.stats_label.text = [
                f"Time:  {self.algorithm.time_approximation: .5f} s",
                f"Iterations:  {self.algorithm.iterations}",
                f"Comparisons:  {self.algorithm.comparisons}",
                f"Array Reads:  {self.algorithm.reads}",
                f"Array Writes:  {self.algorithm.writes}",
            ]
        elif self.algorithm.sorted:
            window.stats_label.text = [
                f"Time:  {self.algorithm.time: .5f} s",
                f"Iterations:  {self.algorithm.iterations}",
                f"Comparisons:  {self.algorithm.comparisons}",
                f"Array Reads:  {self.algorithm.reads}",
                f"Array Writes:  {self.algorithm.writes}",
            ]

        colors = [
            (45, 227, 32),
            (33, 161, 252),
            (161, 69, 247),
            (230, 165, 37),
            (156, 11, 45),
        ]

        padding = 10
        surface_position = (250, padding)

        blit_size = (
            window.size[0] - surface_position[0] - padding,
            window.size[1] - padding * 2
        )

        total_bar_width = blit_size[0] / len(self.array)
        bar_width = math.ceil(total_bar_width * 0.9)
        space_width = math.floor(total_bar_width * 0.1 / 2) * 2
        total_bar_width = bar_width + space_width
        bar_height = window.size[1] / len(self.array)

        surface_size = (
            len(self.array) * total_bar_width,
            window.size[1]
        )

        surface = pygame.Surface(surface_size)
        surface.fill((20, 20, 20))

        for x, y in enumerate(self.array):
            for i, pos in enumerate(self.algorithm.highlight_index):
                if x == pos:
                    color = colors[i]
                    break
            else:
                if x in self.algorithm.highlight_group:
                    color = (200, 200, 200)
                else:
                    color = (100, 100, 100)

            rect = (
                x * (bar_width + space_width),
                0,
                bar_width,
                bar_height * (y + 1)
            )

            pygame.draw.rect(surface, color, rect)

        surface = pygame.transform.flip(surface, 0, 1)
        surface = pygame.transform.scale(surface, blit_size)
        window.window.blit(
            surface,
            surface_position,
            special_flags=pygame.BLEND_ADD
        )


class Window:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.size = (info.current_w / 3 * 2, info.current_h / 5 * 3)
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.font = pygame.freetype.SysFont(None, 15)
        self.clicked = False
        pygame.display.set_caption("Sorting Algorithms")

        self.page_sorting = Page()
        self.page_options = Page()
        self.opened_page = self.page_options
        self.sorting_chart = SortingChart(range(20), SelectionSort)

        self.algorithm_label = Label("Selection Sort", pos=(0.015, 0.03))
        self.stats_label = Label([""], pos=(0.015, 0.5))
        self.measure_count = 10

        self.page_sorting.add_widgets(
            self.algorithm_label,
            Button(
                "Options",
                lambda: (self.open_page(self.page_options),
                         self.sorting_chart.set_paused(True)),
                pos=(0.015, 0.13)
            ),
            Button(
                "Play/Pause",
                self.sorting_chart.run,
                pos=(0.015, 0.23)
            ),
            Button(
                "Randomize",
                self.sorting_chart.reset,
                pos=(0.015, 0.33)
            ),
            self.stats_label,
            self.sorting_chart,
        )

        self.page_options.add_widgets(
            Label("Sorting Algorithms", center=(0.5, 0.1), size=30),
            Label("Algorithm", center=(0.3, 0.2)),

            Label("Options", center=(0.8, 0.2)),
            Label("Sorting Speed", pos=(0.65, 0.3)),
            Slider(
                (0, 1, 0.5),
                (0.65, 0.37),
                self.sorting_chart.set_speed,
                out=lambda val: pow(1 - val, 2),
            ),
            Label("Sorting Numbers", pos=(0.65, 0.5)),
            Slider(
                (0, 4, 1),
                (0.65, 0.57),
                self.sorting_chart.set_count,
                show=True,
                out=lambda var: round(10 ** var),
            ),
            Label("Shuffling", pos=(0.65, 0.7)),
            Slider(
                (0, 2, 0),
                (0.65, 0.77),
                self.sorting_chart.set_shuffling,
                show=True,
                integer=True,
                out=lambda val: ("Normal", "Slight", "Reversed")[val],
            ),

            Button(
                "Done",
                lambda: self.open_page(self.page_sorting),
                center=(0.5, 0.9)
            ),
        )

        for i, (algorithm, name) in enumerate(SortingChart.get_algorithms().items()):
            button = Button(
                name,
                lambda a=algorithm: self.set_algorithm(a),
                center=(0.15 + 0.3 * (i % 2), 0.3 + 0.09 * (i // 2)),
                keep=True,
                toggled=isinstance(self.sorting_chart.algorithm, algorithm)
            )
            self.page_options.add_widget(button)

    def set_measure_count(self, value):
        self.measure_count = value

    def measure(self):
        algorithm = self.sorting_chart.algorithm.__class__()
        length = self.measure_count
        array = [x for x in range(length)]

        if length >= 100000:
            n = 3
        elif isinstance(algorithm, BogoSort) or length >= 10000:
            n = 10
        elif length >= 1000:
            n = 100
        else:
            n = 1000
        total_iterations = 0
        total_comparisons = 0

        start = time.time()

        for _ in range(n):
            algorithm.shuffle(array)
            algorithm.reset()
            iterations, comparisons = algorithm.sort(array)
            if iterations == -1:
                n -= 1
            total_iterations += iterations
            total_comparisons += comparisons

        end = time.time()

        if not n:
            self.measure_label.text = "Time limit exceeded"
            return

        self.measure_label.text = f"Time: {(end - start) / n * 1000:3f}ms\nIterations: {total_iterations // n}\nComparisons: {total_comparisons // n}"

    def set_algorithm(self, algorithm):
        name = self.sorting_chart.get_algorithms()[algorithm]
        self.algorithm_label.text = name
        self.sorting_chart.algorithm = algorithm()
        self.sorting_chart.algorithm.delay = self.sorting_chart.iteration_delay

    def open_page(self, page):
        self.opened_page = page

    def events(self):
        if self.clicked:
            self.clicked -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = 5

    def run(self):
        while True:
            self.events()
            self.window.fill((0, 0, 0))
            self.opened_page.update(self)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000


if __name__ == "__main__":
    Window().run()
