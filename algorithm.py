class Point:
    """
    Represents a point in a two-dimensional space.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distance(self, other):
        """
        Returns the Euclidean distance between this point and another point.
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


current_state = {
    "vertical": [],
    "closest": [],
    "combine": False,
    "base": None,
    "second": None,
    "curr": None,
    "strip": None,
    "return": None,
}


def closest_pair(points):
    """
    Finds the closest pair of points in a given list of points, step by step.

    Args:
        points (list): A list of points.

    Yields:
        dict: The current state of the algorithm, including the closest pair of points found so far.

    """
    global current_state

    # Base cases
    if len(points) == 1:
        current_state["return"] = None
        yield current_state
    elif len(points) == 2:
        return_pair = (points[0], points[1])
        current_state["closest"].append(return_pair)
        current_state["return"] = return_pair
        yield current_state
    else:
        # Divide step
        mid = len(points) // 2 - 1
        current_state["vertical"].append((points[mid], -1))
        yield current_state
        yield from closest_pair(points[: mid + 1])
        left_pair = current_state["return"]

        current_state["vertical"].pop()
        current_state["vertical"].append((points[mid], 1))
        yield current_state
        yield from closest_pair(points[mid + 1 :])
        right_pair = current_state["return"]

        current_state["vertical"].pop()
        current_state["vertical"].append((points[mid], 0))
        if left_pair is not None:
            current_state["closest"].pop()
        current_state["closest"].pop()

        # Combine step
        current_state["combine"] = True
        median_x = points[mid].x
        if left_pair is None:
            min_distance = right_pair[0].distance(right_pair[1])
            current_state["closest"].append(right_pair)
        else:
            if left_pair[0].distance(left_pair[1]) < right_pair[0].distance(
                right_pair[1]
            ):
                min_distance = left_pair[0].distance(left_pair[1])
                current_state["closest"].append(left_pair)
            else:
                min_distance = right_pair[0].distance(right_pair[1])
                current_state["closest"].append(right_pair)

        current_state["strip"] = min_distance

        combine_pair = (Point(0, 0), Point(1200, 560))
        left_strip = [p for p in points[0 : mid + 1] if p.x >= median_x - min_distance]
        right_strip = [p for p in points[mid + 1 :] if p.x <= median_x + min_distance]

        left_strip = sorted(left_strip, key=lambda p: p.y)
        right_strip = sorted(right_strip, key=lambda p: p.y)

        print(left_strip, right_strip)

        initial_right = 0
        for left_point in left_strip:
            if left_point.x < median_x - min_distance:
                continue

            while (
                initial_right < len(right_strip)
                and right_strip[initial_right].y < left_point.y - min_distance
            ):
                initial_right += 1

            final_right = initial_right
            while (
                final_right < len(right_strip)
                and right_strip[final_right].y <= left_point.y + min_distance
            ):
                final_right += 1

            current_state["base"] = left_point
            current_state["second"] = None
            yield current_state

            for right in range(initial_right, final_right):
                if right_strip[right].x > median_x + min_distance:
                    continue

                current_state["second"] = right_strip[right]
                yield current_state

                if left_point.distance(right_strip[right]) < min_distance:
                    min_distance = left_point.distance(right_strip[right])
                    combine_pair = (left_point, right_strip[right])
                    current_state["curr"] = (left_point, right_strip[right])
                    current_state["strip"] = min_distance
                    yield current_state

        if left_pair is None:
            return_pair = min(
                [right_pair, combine_pair], key=lambda p: p[0].distance(p[1])
            )
            if return_pair == combine_pair:
                current_state["closest"].pop()
                current_state["closest"].append(combine_pair)

            current_state["return"] = return_pair
            yield current_state
        else:
            return_pair = min(
                [left_pair, right_pair, combine_pair], key=lambda p: p[0].distance(p[1])
            )
            if return_pair == combine_pair:
                current_state["closest"].pop()
                current_state["closest"].append(combine_pair)

            current_state["return"] = return_pair
            yield current_state

        current_state["vertical"].pop()
        current_state["combine"] = False


if __name__ == "__main__":
    points = [
        Point(100, 100),
        Point(201, 201),
        Point(304, 304),
        Point(409, 409),
        Point(516, 516),
    ]
    points = sorted(points, key=lambda p: p.x)

    for i in closest_pair(points):
        print(i)
    pass
