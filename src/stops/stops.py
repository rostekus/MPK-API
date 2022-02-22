import json
import re
import sqlite3
import requests
import sys
sys.path.append('..')
import timetable.timetable
from pathlib import Path
API_KEY ="YOUR_API_KEY"

def data_dir(filename):
    return Path(__file__).resolve().parents[1].joinpath('data/' + filename)

# check regex if adress contains Łódź
def get_location(address, number, added=False):
    """
    Function returns the location of MPK Łódź stop.
    Uses Google Geocoding API

    Parameters
    ----------
    adress : str
        Adress of the stop.
    number : (float,floar)
        Number of the stop.
    added: bool
        If added "Łódź" was added to the adress
        (default = False)

    Returns
    -------
    (float,float)
        Latitude and longitude of the stop, if function can't
        find the location, it return (0,0)
    """
    if not isinstance(address, str):
        raise ValueError('Adress must be a string')
    if not isinstance(number, str):
        raise ValueError('Number must be a string')
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'key': API_KEY,
        'address': f"{address} ({number}), Polska"

    }
    if len(number) == 3:
        number = "0" + number
    if len(number) == 2:
        number = "00" + number
    if len(number) == 1:
        number = "000" + number

    response = requests.get(base_url, params=params)
    response = response.json()

    lat, lng = None, None

    if response['status'] == 'OK':

        if len(response['results']) > 1:

            for number_of_resaults in range(len(response)):
                if(re.search(number, response['results'][number_of_resaults]['address_components'][0]['long_name'])):
                    lat, lng = (
                        response['results'][number_of_resaults]['geometry']['location'].values())

        if(len(response['results']) == 1 or lat is None):

            lat, lng = response['results'][0]['geometry']['location'].values()

    else:
        if not added:
            lat, lng = get_location(address + " Łódź", number, added = True)
        else:
            return (0,0)

    return lat, lng


def get_stops_location():
    """
    Function creates database with stops information

    Function creates sqlite3 database 'mydatabase.db', table stops with
    colums (number , name , lat, lnt)
    number: number of the stop
    name: name of the stop
    lat: latitude
    lnt: longitude
    The stops are obtained from the MPK site

    Returns
    -------
    None
    """
    lineNameIdDB = getLineNameIds('http://www.mpk.lodz.pl/rozklady/linie.jsp')
    conn = sqlite3.connect('mydatabase.db')
    curr = conn.cursor()

    with conn:
        curr. execute("""DROP TABLE IF EXISTS stops
        """)
        curr.execute("""CREATE TABLE stops(
            number integer,
            name text,
            lat real,
            lnt real)
        """)
        conn.commit()

    stops = dict()

    conn = sqlite3.connect('mydatabase.db')
    curr = conn.cursor()

    with conn:
        for lineName in lineNameIdDB.keys():
            try:
                lineId = LineNameModel().find_id_by_name(lineName)['lineId']
                routeTable = LineNameModel().find_routeTable_by_id(lineId)
                _ = list(routeTable.values())
            except BaseException:
                print("Error :", lineName)
                continue
            first = list(list(_)[0].keys())[0]

            for name, stop in list(_)[0][first].items():
                if stop['stopNumber'] not in stops:
                    try:
                        lat, lng = get_location(name, stop['stopNumber'])
                        stops[stop['stopNumber']] = Stop(name, lat, lng)
                        curr.execute(
                            "INSERT INTO stops (number , name , lat, lnt)VALUES(? ,?, ?, ?);",
                            (stop['stopNumber'],
                             name,
                             lat,
                             lng))
                    except BaseException:
                        print("Error :", lineName, name, stop['stopNumber'])
                        continue


def get_timetables_json():
    """
    Function creates json file with stops information

    Function creates json file 'timetables.json'
    Example:
    {"Line Name":
        {Direction:
            {Stop:
                {Timetable}}}}

    The stops are obtained from the MPK site

    Returns
    -------
    None
    """
    lineNameIdDB = getLineNameIds('http://www.mpk.lodz.pl/rozklady/linie.jsp')

    timetable = dict()

    for lineName in lineNameIdDB.keys():
        try:
            lineId = LineNameModel().find_id_by_name(lineName)['lineId']
            routeTable = LineNameModel().find_routeTable_by_id(lineId)

            timetable[lineName] = {}

            for directionName in routeTable[lineId]:
                timetable[lineName][directionName] = {}
                for stopName in routeTable[lineId][directionName]:

                    busStop = routeTable[lineId][directionName][stopName]
                    direction = busStop['direction']
                    timetableId = busStop['timeTableId']
                    stopNumber = busStop['stopNumber']

                    url = 'http://www.mpk.lodz.pl/rozklady/tabliczka.jsp'
                    table = TimeTableModel().get(url, direction, lineName, timetableId, stopNumber)
                    timetable[lineName][directionName][stopName] = table
            print('ADDED', lineName)

        except BaseException:
            print("Error :", lineName)
            continue
    with open(data_dir("timetables.json"), "w") as f:
        json.dump(timetable, f)


def sqlite_to_json(database):
    """
    Function takes database saved in sqlite3 file and transforms
    into json file

    Parameters
    ----------
    database : str
        Filename.
    Returns
    -------
    None
    """
    conn = sqlite3.connect(database)
    curr = conn.cursor()

    curr.execute("SELECT name, lat,lnt from stops")
    location = {}
    for stop in curr.fetchall():
        location[stop[0]] = [stop[1], stop[2]]
    with open(data_dir("location.json"), "w") as f:
        json.dump(location, f)


def get_stops(filename='timetables.json'):
    """
    Function obtaints stops information from json file created by
    get_stops_location() and sorts its by lines and saves into json file
    Example:
    {"Line" : [stop1, stop2, ..., stopN]}
    Parameters
    ----------
    filename : str
        Filename of json file created
        by get_stops_location()

    Returns
    -------
    None
    """
    f = open(filename)
    json_file = json.load(f)
    stops = {}
    for line in json_file:
        stops[line] = []
        for stop in json_file[line][list(json_file[line].keys())[0]]:
            stops[line].append(stop)
    with open(data_dir("stops.json"), "w") as f:
        json.dump(stops, f)


if __name__ == '__main__':
    get_location("Piotrkowska pl. Niepodległości","0686")

