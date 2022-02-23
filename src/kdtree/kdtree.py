"""
Kdtree Module
"""
import json
import sqlite3
from pathlib import Path
from collections.abc import Iterable


def data_dir(filename):
    return Path(__file__).resolve().parents[1].joinpath("data/" + filename)


def distance(p1, p2):
    """
    Function for calculating squared of Euclidian
    distance

    Parameters
    ----------
    p1 : (float,float)
        First point.
    p1 : (float,floar)
        Second point.

    Returns
    -------
    (float,float)
        Squared Euclidian distance.
    """
    if len(p1) != len(p1):
        raise ValueError("Please specify the  points in the same dimentions")
    
    if not((all(isinstance(i, int) for i in p1)) or all(isinstance(i, float) for i in p1)):
        raise ValueError(f"Cordinates must me int or floats {p1}")

    if not((all(isinstance(i, int) for i in p2)) or all(isinstance(i, float) for i in p2)):
        raise ValueError(f"Cordinates must me int or floats {p2}")

    if p1 == p2:
        return 0
    else:
        return sum((x - y)**2 for x, y in zip(p1, p2))


def build_kdtree(points, depth=0):
    """
    Bulding kdree (dict) from list of points on the 2D plane

    Parameters
    ----------
    points : list of tuples (float, float)
        The list from which kdree will be created.
    depth: int
        Depth of the kdtree (default = 0)


    Returns
    -------
    dict
       Kdtree.
    """
    if not isinstance(points, Iterable):
        raise ValueError("Points must be iterable")

    n = len(points)
    if n <= 0:
        return None

    axis = depth % 2

    # l1 and l2 has to be numpy arrays

    sorted_points = sorted(points, key=lambda point: point[axis])

    return {
        "point": sorted_points[n // 2],
        "left": build_kdtree(sorted_points[:n // 2], depth + 1),
        "right": build_kdtree(sorted_points[n // 2 + 1:], depth + 1),
        "name": sorted_points[n // 2],
    }


def closer_distance(pivot, p1, p2):
    """
    Returning closer point to the pivot

    Parameters
    ----------
    pivot: (float,float)
        Pivot point
    p1 : (float,float)
        First point.
    p1 : (float,floar)
        Second point.

    Returns
    -------
    p1 or p2, if points are the same, return (p1,p2)
    """
    if pivot is None:
        raise ValueError("Please specify pivot point")
    if p1 is None:
        if p2 is not None:
            return p2
        else:
            return None
    else:
        if p2 is None:
            return p1
    if p1 == p2:
        return (p1, p2)

    values = [p1, p2, pivot]
    for x in values:
        if not all(len(v) == len(values[0]) for v in values):
            raise TypeError("Dimention of the variables must be the sam,e")
    for x in values:
        if isinstance(x, list) or isinstance(x, tuple):
            if not (all(isinstance(n, int)
                        for n in x) and all(isinstance(n, float) for n in x)):
                raise TypeError(f"{x} must be list or tuple")
        else:
            raise TypeError(f"{x} must be list or tuple")

    d1 = distance(pivot, p1)
    d2 = distance(pivot, p2)

    if d1 < d2:
        return p1
    else:
        return p2


def kdtree_closest_point(root, point, depth=0):
    """
    Returning closer point from kdree to the point

    Parameters
    ----------
    root: dict
        Kdtree.
    point : (float,float)
        Point.
    depth: int
        Depth of the kdtree (default = 0)

    Returns
    -------
    (float, float)
    Closer point from kdtree to the point
    """
    if root is None:
        return None
    k = 2
    axis = depth % k

    next_branch = None
    opposite_branch = None

    if point[axis] < root["point"][axis]:
        next_branch = root["left"]
        opposite_branch = root["right"]
    else:
        next_branch = root["right"]
        opposite_branch = root["left"]

    best = closer_distance(
        point,
        kdtree_closest_point(next_branch, point, depth + 1),
        root["point"],
    )

    if distance(point, best) > (point[axis] - root["point"][axis])**2:
        best = closer_distance(
            point,
            kdtree_closest_point(opposite_branch, point, depth + 1),
            best,
        )

    return best


def kdtree_from_db(db_file) -> dict:
    """
    Creating kdtree from sqlite3 database

    Parameters
    ----------
    db_file: str
        Name of sqlite3 database.

    Returns
    -------
    dict
    Kdree
    """
    try:
        conn = sqlite3.connect(db_file)
    except BaseException:
        print(f"Cannot open database {db_file}.")
        return

    curr = conn.cursor()
    curr.execute("SELECT lat, lnt, name from stops")
    rows = curr.fetchall()

    return build_kdtree(rows)


def dump_kdtree(root, filename="kdtree.json"):
    """
    Saves kdree to json file


    Parameters
    ----------
    root: dict
        Kdtree
    filename: str
        Name of file
    Returns
    -------
    None
    """

    with open(data_dir(filename), "w") as f:
        json.dump(root, f)


if __name__ == "__main__":
    pass
