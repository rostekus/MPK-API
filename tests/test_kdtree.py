from re import A
import sys
import pytest

import kdtree.kdtree as kdtree


@pytest.mark.parametrize("p1, p2, expected_result", [
    ((1,1), (0,0), 2),
    ((1,1,1),(0,0,0),3),
    ((1,2,4), (1,2,4),0),


])
def test_distance(p1, p2,expected_result):
    assert kdtree.distance(p1, p2) == expected_result


def test_distance():
    with pytest.raises(ValueError):
        assert kdtree.distance((1,"",""),(1,2,""))
        assert kdtree.distance((1,2),(1,2,2))


@pytest.mark.parametrize("points, expected_result", [
    ([], None),
    ([(0,0),(1,1),(2,2)],{'point': (1, 1), 'left': {'point': (0, 0), 'left': None, 'right': None, 'name': (0, 0)}, 'right': {'point': (2, 2), 'left': None, 'right': None, 'name': (2, 2)}, 'name': (1, 1)}),
    ([(0,0),(0,0),(0,0)],{'point': (0, 0), 'left': {'point': (0, 0), 'left': None, 'right': None, 'name': (0, 0)}, 'right': {'point': (0, 0), 'left': None, 'right': None, 'name': (0, 0)}, 'name': (0, 0)}),
])
def test_build_kdtree(points, expected_result):
    assert kdtree.build_kdtree(points) == expected_result


def  test_build_kdtree():
    with pytest.raises(TypeError):
        assert kdtree.build_kdtree([3,2,4,3,""])
        assert kdtree.build_kdtree(342243423)
        assert kdtree.build_kdtree("hgfdfdghytgrf")

@pytest.mark.parametrize("pivot,p1,p2, expected_result", [
    ((0,1), None, None, None),
    ((0,1), (0,2), None, (0,2)),
    ((0,1), None, (0,2), (0,2)),
    ((0,1), (0,2), (0,2),((0,2),(0,2))),

    

])
def test_closer_distance(pivot,p1,p2, expected_result):
    assert kdtree.closer_distance(pivot, p1,p2) == expected_result

def  test_closer_distance():
    with pytest.raises(TypeError):
        assert kdtree.build_kdtree()
        assert kdtree.build_kdtree(342243423)
        assert kdtree.build_kdtree("hgfdfdghytgrf")
        assert kdtree.build_kdtree((1,2,2), (1,1),(1,2))
        assert kdtree.build_kdtree((1,2,2), (1,1),(1,2))
        assert kdtree.build_kdtree((1,2,2), (1,"3"),(1,2))

def  test_closer_distance():
    with pytest.raises(ValueError):
        assert kdtree.closer_distance(None,(0,1),(0,2))
