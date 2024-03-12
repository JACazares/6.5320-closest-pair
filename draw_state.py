import pygame


class Point:
    """
    Represents a point in a 2D coordinate system.

    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win, color):
        """
        Draws a circle representing the point on the given window.

        Args:
            win (pygame.Surface): The window to draw on.
            color (tuple): The color of the circle in RGB format.
        """
        pygame.draw.circle(win, color, (self.x, self.y), 5, 0)

    def draw_vertical(self, win, color):
        """
        Draws a vertical line passing through the point on the given window.

        Args:
            win (pygame.Surface): The window to draw on.
            color (tuple): The color of the line in RGB format.
        """
        pygame.draw.line(win, color, (self.x, 0), (self.x, 720), 1)


def draw_points(win, points):
    """
    Draw a list of points on a given window.

    Args:
        win (pygame.Surface): The window surface to draw the points on.
        points (list): A list of Point objects to be drawn.

    Returns:
        None
    """
    for point in points:
        point.draw(win, "black")


def draw_line(win, point1, point2, color):
    """
    Draws a line on the given window between the specified points with the given color.

    Parameters:
    win (pygame.Surface): The window surface on which to draw the line.
    point1 (pygame.Vector2): The starting point of the line.
    point2 (pygame.Vector2): The ending point of the line.
    color (tuple): The RGB color value of the line.

    Returns:
    None
    """
    pygame.draw.line(win, color, (point1.x, point1.y), (point2.x, point2.y), 1)


def draw_state(win, dict):
    """
    Draws the state of the window based on the given dictionary.

    Parameters:
    - win (pygame.Surface): The window surface to draw on.
    - dict (dict): A dictionary containing information about the state of the window.

    Returns:
    - None

    The dictionary should have the following keys:
    - "vertical" (list): A list of tuples representing vertical lines to be drawn. Each tuple should contain a point (x, y) and a direction (-1 for left, 1 for right).
    - "closest" (list): A list of tuples representing closest points to be connected by lines. Each tuple should contain two points (point1, point2).
    - "combine" (bool): A boolean indicating whether we are in the combine step

    Additionally, if "combine" is True, the dictionary should have the following keys
    - "base" (Point): The base point currently being considered.
    - "second" (Point): The second point currently being considered against the base point.
    - "curr" (tuple): A tuple containing two points (point1, point2) to be connected by a line, the current closest pair of points in the combine step.
    - "strip" (int): The radius of the strip to be drawn around the last vertical line.

    Note:
    - The function assumes that the pygame module has been imported.
    - The function assumes that the necessary helper functions (e.g., draw_line, draw_vertical) are defined.

    Example usage:
    ```
    state = {
        "vertical": [((100, 200), -1), ((300, 400), 1)],
        "closest": [((100, 200), (300, 400)), ((500, 600), (700, 800))],
        "combine": True,
        "base": Point(100, 200),
        "second": Point(300, 400),
        "curr": (Point(500, 600), Point(700, 800)),
        "strip": 50
    }
    draw_state(window_surface, state)
    ```
    """

    if dict["vertical"] is not None and len(dict["vertical"]) > 0:
        min_x = 0
        max_x = 1200

        for point, dir in dict["vertical"]:
            if dir == -1:
                max_x = point.x
            if dir == 1:
                min_x = point.x
            point.draw_vertical(win, "black")

        dict["vertical"][-1][0].draw_vertical(win, "red")

        s = pygame.Surface((min_x, 560), pygame.SRCALPHA)
        s.fill((192, 192, 192, 100))
        win.blit(s, (0, 0))

        s = pygame.Surface((1200 - max_x, 560), pygame.SRCALPHA)
        s.fill((192, 192, 192, 100))
        win.blit(s, (max_x, 0))

    if dict["closest"] is not None:
        if len(dict["closest"]) == 1:
            (point1, point2) = dict["closest"][0]
            draw_line(win, point1, point2, "blue")
            point1.draw(win, "blue")
            point2.draw(win, "blue")
        else:
            for point1, point2 in dict["closest"]:
                draw_line(win, point1, point2, "red")

    if dict["combine"] == True:
        if dict["base"] is not None:
            dict["base"].draw(win, "green")
            # draw a horizontal line passing through the base point, covering the whole strip, in black
            pygame.draw.line(
                win,
                "black",
                (
                    dict["vertical"][-1][0].x - dict["strip"],
                    dict["base"].y - dict["strip"],
                ),
                (
                    dict["vertical"][-1][0].x + dict["strip"],
                    dict["base"].y - dict["strip"],
                ),
                1,
            )
            pygame.draw.line(
                win,
                "black",
                (
                    dict["vertical"][-1][0].x - dict["strip"],
                    dict["base"].y + dict["strip"],
                ),
                (
                    dict["vertical"][-1][0].x + dict["strip"],
                    dict["base"].y + dict["strip"],
                ),
                1,
            )

        if dict["second"] is not None:
            draw_line(win, dict["base"], dict["second"], "green")

        if dict["curr"] is not None:
            draw_line(win, dict["curr"][0], dict["curr"][1], "green")

        if dict["strip"] is not None:
            # draw a strip of radius dict["strip"] around the last vertical line
            s = pygame.Surface((2 * dict["strip"], 560), pygame.SRCALPHA)
            s.fill((255, 0, 0, 50))
            win.blit(s, (dict["vertical"][-1][0].x - dict["strip"], 0))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 560))
    clock = pygame.time.Clock()
    running = True

    sample_state = {
        "vertical": [(Point(200, 200), 1), (Point(300, 300), 0)],
        "closest": [(Point(100, 100), Point(200, 200))],
        "combine": True,
        "base": Point(100, 150),
        "second": Point(150, 175),
        "curr": (Point(100, 150), Point(100, 175)),
        "strip": 10,
    }

    sample_points = [
        Point(100, 100),
        Point(200, 200),
        Point(300, 300),
        Point(400, 400),
        Point(100, 150),
        Point(150, 175),
        Point(100, 175),
    ]

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # clear the screen
        screen.fill("white")
        draw_points(screen, sample_points)
        draw_state(screen, sample_state)

        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
