import pygame
import random


class GUI(object):
    FPS = 30
    FPS_VARIANT = 5

    def __init__(self):
        pygame.init()

        self.running = True
        self.typing = False

        self.neural_network = None

        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = self.screen.get_size()

        self.font = pygame.font.SysFont("Monospace", 15)

        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        pygame.event.get()

    def bind(self, neural_network):
        self.neural_network = neural_network

    def draw(self):
        def place_text(text, x, y):
            rendered_text = self.font.render(text, 1, (0, 0, 0))
            self.screen.blit(rendered_text, (x, y))
            return y + rendered_text.get_height()

        if self.neural_network:
            if self.neural_network.training:
                self.screen.fill((150, 200, 150))
            else:
                self.screen.fill((255, 255, 255))

            y = 0
            y = place_text("Neural Network!", 0, y)
            y = place_text("Iteration #%d" % self.neural_network.iteration, 0, y)
            y = place_text("Input Word: %s" % self.neural_network.word.upper(), 0, y)
            o = self.neural_network.languages[self.neural_network.desired_output]
            if self.typing:
                o = "???"
            y = place_text("Expected Output: %s" % o, 0, y)
            y = place_text("Step Size: %f" % self.neural_network.brain.alpha, 0, y)
            y = place_text("Min Word Len: %d" % self.neural_network.MINIMUM_WORD_LENGTH, 0, y)
            y = place_text("Possible Languages:", 0, y)
            for i in self.neural_network.counted_languages:
                y = place_text(self.neural_network.languages[i], 15, y)

            if self.typing:
                s = "HOW'D I DO?"
            else:
                if self.neural_network.last_one_was_correct:
                    s = "RIGHT"
                else:
                    s = "WRONG"
            y = place_text(
                "Actual Prediction: %s (%s)" % (self.neural_network.languages[self.neural_network.brain.top_output], s),
                0, y)
            y = place_text("Confidence: %f%%" % round(self.neural_network.brain.confidence * 100, 6), 0, y)
            y = place_text("%% of last %d correct: %f%%" % (self.neural_network.guess_window, round(100.0 * (
                (1.0 * self.neural_network.recent_right_count) / max(1, min(self.neural_network.iteration,
                                                                            self.neural_network.guess_window))), 6)), 0,
                           y)
            y = place_text("Current streak: %d" % self.neural_network.streak, 0, y)
            y = place_text("Longest streak: %d" % self.neural_network.long_streak, 0, y)

        else:
            self.screen.fill((random.randint(180, 220), 50, 50))

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.neural_network.training:
                        self.neural_network.training = False
                        self.neural_network.word = ""
                        self.typing = True
                    else:
                        self.neural_network.training = True
                if self.typing:
                    if event.key == pygame.K_BACKSPACE:
                        self.neural_network.word = self.neural_network.word[:-1]
                    elif 97 <= event.key <= 122:
                        self.neural_network.word += chr(event.key).upper()
                self.neural_network.get_brain_error_from_line(self.neural_network.word, 0, False)

    def mainloop(self):
        while self.running:
            self.draw()
            self.events()
            fTime = self.clock.tick(self.FPS)
            if fTime > (1000. / self.FPS) + self.FPS_VARIANT:
                print "[WARNING] Frame took %d ms!" % fTime


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
