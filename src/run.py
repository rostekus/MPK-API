from stops.stops import (
    get_stops_location,
    get_stops,
    get_timetables_json,
)
from kdtree.kdtree import kdtree_from_db, dump_kdtree


def main():

    get_stops_location()
    # creates mydatabase.db

    kdtree = kdtree_from_db()
    dump_kdtree(kdtree)
    # kdree from mydatabase.db
    # saved into kdree.json

    get_timetables_json()
    # timetables.json
    get_stops()
    # from timetables.json
    # creates stops.json


if __name__ == "__main__":
    main()
