import algorithms
import pygame.freetype
import pygame
import random


class Main:
    def __init__(self, title, n):
        pygame.init()

        self.size = (705, 400)
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.freetype.SysFont(None, 15)
        pygame.display.set_caption(title)

        self.array = [i for i in range(n)]
        random.shuffle(self.array)

        self.iterations = 0
        self.algorithm = algorithms.SelectionSort()
        self.timer = 0
        self.paused = True
        self.done = False
        self.speed = 300
        self.button_cooldown = 0

    def reset(self):
        self.iterations = 0
        self.done = False
        self.paused = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()

    def run(self):
        while True:
            # Get events
            self.events()
            self.window.fill((0, 0, 0))

            # Draw buttons
            buttons = [
                "Fps: " + str(round(self.clock.get_fps())),
                "",
                "> Selection Sort",
                "> Insertion Sort",
                "> Bubble Sort",
                "> Quick Sort",
                "> Bogo Sort",
                "",
                "> Iterate",
                "> Play",
                "> Measure",
                "> Randomize",
                "> Increase Speed",
                "> Decrease Speed",
                "",
                "Stats:",
                " Iterations: " + str(self.iterations),
            ]
            if isinstance(self.algorithm, algorithms.SelectionSort):
                buttons[2] = "-" + buttons[2][1:]
            elif isinstance(self.algorithm, algorithms.InsertionSort):
                buttons[3] = "-" + buttons[3][1:]
            elif isinstance(self.algorithm, algorithms.BubbleSort):
                buttons[4] = "-" + buttons[4][1:]
            elif isinstance(self.algorithm, algorithms.QuickSort):
                buttons[5] = "-" + buttons[5][1:]
            elif isinstance(self.algorithm, algorithms.BogoSort):
                buttons[6] = "-" + buttons[6][1:]

            if not self.paused:
                buttons[9] = "> Pause"

            self.button_cooldown += 1
            for i, text in enumerate(buttons):
                color = (255, 255, 255)

                if text and text[0] == ">":
                    m = pygame.mouse.get_pos()
                    hover = m[0] < 100 and i < (m[1] - 10) / 20 < i + 1
                    if hover:
                        color = (200, 200, 200)

                    mouse_pressed = pygame.mouse.get_pressed()[0]
                    if self.button_cooldown > 10 and mouse_pressed and hover:
                        self.button_cooldown = 0
                        if text == "> Selection Sort":
                            self.algorithm = algorithms.SelectionSort()
                            self.reset()
                        elif text == "> Insertion Sort":
                            self.algorithm = algorithms.InsertionSort()
                            self.reset()
                        elif text == "> Bubble Sort":
                            self.algorithm = algorithms.BubbleSort()
                            self.reset()
                        elif text == "> Quick Sort":
                            self.algorithm = algorithms.QuickSort()
                            self.reset()
                        elif text == "> Bogo Sort":
                            self.algorithm = algorithms.BogoSort()
                            self.reset()
                        elif text == "> Iterate":
                            self.iter()
                            self.paused = True
                        elif text == "> Play":
                            self.paused = False
                        elif text == "> Pause":
                            self.paused = True
                        elif text == "> Randomize":
                            random.shuffle(self.array)
                            self.algorithm.reset()
                            self.reset()
                        elif text == "> Increase Speed":
                            self.speed = max(10, self.speed - 10)
                        elif text == "> Decrease Speed":
                            self.speed += 10

                self.font.render_to(
                    self.window,
                    (10, 10 + 20 * i),
                    text,
                    color
                )

            # Draw chart
            for i, x in enumerate(self.array):
                if i == self.algorithm.highlight_sorting:
                    color = (100, 255, 150)
                elif i == self.algorithm.highlight_comparing:
                    color = (255, 150, 200)
                elif i in self.algorithm.highlight_sorted:
                    color = (200, 200, 200)
                else:
                    color = (100, 100, 100)
                pygame.draw.rect(
                    self.window,
                    color,
                    (205 + i * 25, self.size[1] - 5 - 20 * x, 20, 20 * x)
                )

            # Update display
            pygame.display.flip()
            self.timer += self.clock.tick(30)

            # Sorting iteration
            if self.timer > self.speed:
                self.timer = 0
                if not (self.paused or self.done):
                    self.iter()

    def iter(self):
        self.algorithm.sort(self.array)
        if self.algorithm.done:
            self.done = True
            return
        self.iterations += 1


if __name__ == "__main__":
    Main("Sorting Algorithms", 20).run()
