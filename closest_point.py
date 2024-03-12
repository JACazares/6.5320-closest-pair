import pygame
import draw_state
import algorithm


class Button:
    """
    A class representing a button.

    Attributes:
        x (int): The x-coordinate of the button's top-left corner.
        y (int): The y-coordinate of the button's top-left corner.
        width (int): The width of the button.
        height (int): The height of the button.
        color (Color): The color of the button.
        hover_color (Color): The color of the button when hovered (default: "grey").
    """

    def __init__(self, x, y, width, height, color, hover_color="grey"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color

    def draw(self, win, hovered=False):
        """
        Draw the button on the given window.

        Args:
            win (pygame.Surface): The window to draw the button on.
            hovered (bool): Whether the button is currently being hovered (default: False).
        """
        if hovered:
            pygame.draw.rect(
                win, self.hover_color, (self.x, self.y, self.width, self.height), 0, 0
            )
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height), 1, 0
        )

    def check_mouse(self, pos):
        """
        Check if the given position is within the button's boundaries.

        Args:
            pos (tuple): The position to check, represented as a tuple (x, y).

        Returns:
            bool: True if the position is within the button's boundaries, False otherwise.
        """
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class Point(draw_state.Point):
    """
    Represents a point in a two-dimensional space.

    This class inherits from the `draw_state.Point` class and adds no additional functionality.
    It is used to represent points in the context of the closest point problem.
    """

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance(self, other):
        """
        Returns the Euclidean distance between this point and another point.
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


def draw_diplay(win, pos):
    """
    Draws the display on the window.

    Parameters:
    - win (pygame.Surface): The window surface to draw on.
    - pos (tuple): The current position of the mouse.

    Returns:
    None
    """
    pygame.draw.rect(win, "black", pygame.Rect(39, 39, 1202, 562), 1, 0)

    pause_button.draw(win, pause_button.check_mouse(pos))
    pygame.draw.rect(win, (102, 102, 102), pygame.Rect(535, 637, 12, 45), 0)
    pygame.draw.rect(win, (102, 102, 102), pygame.Rect(552, 637, 12, 45), 0)

    play_button.draw(win, play_button.check_mouse(pos))
    pygame.draw.polygon(win, (0, 104, 55), [(628, 637), (654, 660), (628, 682)], 0)

    step_button.draw(win, step_button.check_mouse(pos))
    pygame.draw.rect(win, (57, 181, 74), pygame.Rect(709, 637, 12, 45), 0)
    pygame.draw.polygon(win, (57, 181, 74), [(725, 637), (750, 660), (725, 682)], 0)

    reset_button.draw(win, reset_button.check_mouse(pos))
    pygame.draw.rect(win, (193, 39, 45), pygame.Rect(1187, 637, 46, 46), 0)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    point_screen = pygame.Surface((1200, 560))

    clock = pygame.time.Clock()
    RUNNING = True

    pause_button = Button(520, 630, 60, 60, "black")
    play_button = Button(610, 630, 60, 60, "black")
    step_button = Button(700, 630, 60, 60, "black")
    reset_button = Button(1180, 630, 60, 60, "black")

    points_state = {
        "vertical": [],
        "closest": [],
        "combine": False,
        "base": None,
        "second": None,
        "curr": None,
        "strip": None,
        "return": None,
    }

    points = [
        Point(122, 135),
        Point(235, 248),
        Point(305, 414),
        Point(417, 78),
        Point(444, 258),
        Point(509, 474),
        Point(533, 169),
        Point(604, 309),
        Point(608, 277),
        Point(643, 118),
        Point(773, 81),
        Point(774, 372),
        Point(809, 216),
        Point(940, 486),
        Point(995, 198),
        Point(1080, 348),
    ]
    points = sorted(points, key=lambda p: p.x)
    gen = algorithm.closest_pair(points)

    STATE = "stop"
    STEP = False
    PREVIOUS_TIME = 0
    while RUNNING:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        draw_diplay(screen, pygame.mouse.get_pos())
        point_screen.fill("white")
        draw_state.draw_points(point_screen, points)
        draw_state.draw_state(point_screen, points_state)
        screen.blit(point_screen, (40, 40))

        # Check if mouse is clicked over some button
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            PREVIOUS_TIME = pygame.time.get_ticks()
            if STATE == "stop":
                if play_button.check_mouse(mouse_pos):
                    gen = algorithm.closest_pair(points)
                    STATE = "play"
                elif step_button.check_mouse(mouse_pos):
                    gen = algorithm.closest_pair(points)
                    STATE = "pause"
                    STEP = True
                elif reset_button.check_mouse(mouse_pos):
                    points = []
                    points_state = {
                        "vertical": [],
                        "closest": [],
                        "combine": False,
                        "base": None,
                        "second": None,
                        "curr": None,
                        "strip": None,
                        "return": None,
                    }
                    gen = algorithm.closest_pair(points)
                    algorithm.current_state = {
                        "vertical": [],
                        "closest": [],
                        "combine": False,
                        "base": None,
                        "second": None,
                        "curr": None,
                        "strip": None,
                        "return": None,
                    }
                    STATE = "stop"
                clock.tick(10)
            elif STATE == "play":
                if pause_button.check_mouse(mouse_pos):
                    STATE = "pause"
                elif reset_button.check_mouse(mouse_pos):
                    STATE = "pause"
                clock.tick(10)
            elif STATE == "pause":
                if play_button.check_mouse(mouse_pos):
                    STATE = "play"
                elif step_button.check_mouse(mouse_pos):
                    STEP = True
                elif reset_button.check_mouse(mouse_pos):
                    points = []
                    points_state = {
                        "vertical": [],
                        "closest": [],
                        "combine": False,
                        "base": None,
                        "second": None,
                        "curr": None,
                        "strip": None,
                        "return": None,
                    }
                    gen = algorithm.closest_pair(points)
                    algorithm.current_state = {
                        "vertical": [],
                        "closest": [],
                        "combine": False,
                        "base": None,
                        "second": None,
                        "curr": None,
                        "strip": None,
                        "return": None,
                    }
                    STATE = "stop"
                clock.tick(10)

        if STATE == "stop":
            # Check if mouse is in display area, add a point if it is
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] >= 40 and mouse_pos[0] <= 1240:
                    if mouse_pos[1] >= 40 and mouse_pos[1] <= 600:
                        points.append(Point(mouse_pos[0] - 40, mouse_pos[1] - 40))
                        points = sorted(points, key=lambda p: p.x)
                        gen = algorithm.closest_pair(points)
                        algorithm.current_state = {
                            "vertical": [],
                            "closest": [],
                            "combine": False,
                            "base": None,
                            "second": None,
                            "curr": None,
                            "strip": None,
                            "return": None,
                        }
                        clock.tick(10)

        elif STATE == "play":
            try:
                if pygame.time.get_ticks() - PREVIOUS_TIME > 500:
                    points_state = next(gen)
                    print(points)
                    print(points_state)
                    PREVIOUS_TIME = pygame.time.get_ticks()
            except:
                gen = algorithm.closest_pair(points)
                algorithm.current_state = {
                    "vertical": [],
                    "closest": [],
                    "combine": False,
                    "base": None,
                    "second": None,
                    "curr": None,
                    "strip": None,
                    "return": None,
                }
                STATE = "stop"
        elif STATE == "pause":
            if STEP:
                try:
                    points_state = next(gen)
                    print(points_state)
                except:
                    gen = algorithm.closest_pair(points)
                    algorithm.current_state = {
                        "vertical": [],
                        "closest": [],
                        "combine": False,
                        "base": None,
                        "second": None,
                        "curr": None,
                        "strip": None,
                        "return": None,
                    }
                STEP = False
                clock.tick(10)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
