"""
Module for obtainting Timetables from MPK LODZ site.

Classes:

    Stop
    LineNameModel
    TimeTableModel
    Table

Functions:

    getLineNameIds -> dict

"""

from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import requests
from pathlib import Path

w1 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
w2 = " (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
l1 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
l2 = "(KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36"
agent = {"User-Agent": l1 + l2}


def data_dir(filename):
    return Path(__file__).resolve().parents[1].joinpath("data/" + filename)


@dataclass(init=True, repr=True, frozen=True)
class Stop:
    """
    A class to represent a Stop. Created with dataclass
    decorator(init=True, repr=True, frozen=True).
    ...
    Attributes
    ----------
    name : str
        first name of the person
    lat : str
        family name of the person
    lng : int
        age of the person

    """

    name: str
    lat: float = 0
    lng: float = 0


class LineNameModel:
    """
    A class for finding line number by name
    and route Table.
    ...
    Methods
    -------
    find_id_by_name(lineName)
        Finds the id of the line.
    find_routeTabel_by_id(lineId)
        Returns routeTable.
    """
    def find_id_by_name(self, lineName):
        """
        Function finds id of the given line.

        Parameters
        ----------
        lineName : str
            Line name.
        Returns
        -------
        dict
            {"lineId": lineId}.
        """
        if lineName in lineNameIdDB:
            lineId = lineNameIdDB["{}".format(lineName)]
            return {"lineId": lineId}
        else:
            return {"Message": None}, 404

    def find_routeTable_by_id(self, lineId):
        """
        Function finds route Table of given line.

        Parameters
        ----------
        lineId : int
            Line id.
        Returns
        -------
        dict
        """
        dateTime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        urlRoot = "http://www.mpk.lodz.pl/rozklady/trasa.jsp"
        urlTail = f"?lineId={lineId}&date={dateTime}"
        url = urlRoot + urlTail

        resp = requests.get(url, headers=agent)
        soup = BeautifulSoup(resp.content, "lxml")

        dRoute = soup.find("div", {"id": "dRoute"})

        routeTableDB = {f"{lineId}": {}}
        dStreetStop = {}
        dDirectionTable = {}

        tData = dRoute.find("table").findAll("tr", recursive=False)
        tDirectionTables = tData[1]
        for Table in tDirectionTables.findAll("td", recursive=False):
            tDirection = Table.find("div", {
                "class": "headSign"
            }).contents[0]  # route direction
            Rows = Table.find("table").findAll("tr", recursive=False)
            for Row in Rows[1:]:  # skipping table header
                Cells = Row.findAll("td", recursive=False)

                sStreet = Cells[0].get_text().strip()
                sStop = Cells[2].get_text().strip()
                sStreetStop = (f"{sStreet} {sStop}").lstrip()

                sDirection = (Cells[2].find("a").get("href").partition("?")
                              [2].split("&")[0].partition("=")[2])
                sTimeTableId = (Cells[2].find("a").get("href").partition("?")
                                [2].split("&")[2].partition("=")[2])
                sNumber = (Cells[2].find("a").get("href").partition("?")
                           [2].split("&")[3].partition("=")[2])

                dStreetStop.update({
                    sStreetStop: {
                        "direction": sDirection,
                        "stopNumber": sNumber,
                        "timeTableId": sTimeTableId,
                    }
                })
            dDirectionTable.update({tDirection: dStreetStop})
            dStreetStop = {}
        routeTableDB.update({lineId: dDirectionTable})

        return routeTableDB


def getLineNameIds():
    """
    Function gets the Line Ids fro MPK site

    Returns
    -------
    dict
        {"lineNameId: lineId}.
    """
    url = "http://www.mpk.lodz.pl/rozklady/linie.jsp"
    if __name__ == "__main__":
        print(f"getting line IDs from {url}")
    resp = requests.get(url, headers=agent)
    soup = BeautifulSoup(resp.text, "html.parser")
    dWrkspc = soup.find("div", {"id": "dWrkspc"})
    dLineTypes = dWrkspc.find_all("div", class_="dLines")
    lineNameId = {}
    for lineType in dLineTypes:
        tData = lineType.find("table").find("td")
        for dataRow in tData.find_all("a"):
            lineName = dataRow.get_text()
            lineId = (dataRow.get("href").partition("?")[2].partition("&")
                      [0].partition("=")[2])
            lineNameId.update({lineName: lineId})

    return lineNameId


lineNameIdDB = getLineNameIds()


class TimeTableModel:
    """
    A class for finding Time Table
    ...
    Methods
    -------
    _get(url, direction, lineName, timetableId, stopNumber)
        Privite method. Returns the time table, based on Ids
    get_bus_table(lineName, directionName, stopName)
        Class method. Returns routeTable based on real names
    """
    def __init__(self):
        pass

    def _get(
        self,
        url,
        direction,
        lineName,
        timetableId,
        stopNumber,
    ):
        """
         Returns the time table, based on Ids

        Parameters
        ----------
        url : str
            MPK site : http://www.mpk.lodz.pl/rozklady/tabliczka.jsp
        direction : str
        lineName: str
        timetableId : int
        stopNumber :int


        Returns
        -------
        dict
        """
        lineId = lineNameIdDB[f"{lineName}"]
        dt = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        curl = f"{url}?direction={direction}&lineId={lineId}&timetableId={timetableId}&stopNumber={stopNumber}&date={dt}"

        resp = requests.get(curl, headers=agent)
        soup = BeautifulSoup(resp.text, "html.parser")

        dTab = soup.find("div", {"id": "dTab"})
        dDayTypeNames = {
            dtname.get_text(): dtname.get("id").replace("_name", "")
            for dtname in dTab.find("div", {
                "id": "dDayTypeNames"
            }).find_all("a")
        }
        dDayTypes = dTab.find("div", {"id": "dDayTypes"})

        dDayTables = {}
        for dName, tName in dDayTypeNames.items():
            dDayTables[dName] = dDayTypes.find("div", {
                "id": "table_{}".format(tName)
            }).find("table")
        bustimetable = {f"{lineName}": ""}
        daytimetable = {}
        timetable = {}

        for dName, tName in dDayTables.items():
            for row in tName.find_all("tr"):
                hour = row.find("th").get_text()
                minute = []
                for cell in row.find_all("a"):
                    minute.append(cell.get_text())
                timetable.update({f"{hour}": minute})
            daytimetable.update({dName: timetable})
            timetable = {}
        bustimetable.update({f"{lineName}": daytimetable})

        return bustimetable

    @classmethod
    def get_bus_table(cls, lineName, directionName, stopName):
        """
         Returns the time table, based on real names which are
         translated into id and than passed to _get()

        Parameters
        ----------
        url : str
            MPK site : http://www.mpk.lodz.pl/rozklady/tabliczka.jsp
        direction : str
        lineName: str
        directionName : str
        stopName : str

        Returns
        -------
        dict
        """
        lineId = LineNameModel().find_id_by_name(lineName)["lineId"]
        routeTable = LineNameModel().find_routeTable_by_id(lineId)

        busStop = routeTable[lineId][directionName][stopName]
        direction = busStop["direction"]
        timetableId = busStop["timeTableId"]
        stopNumber = busStop["stopNumber"]

        url = "http://www.mpk.lodz.pl/rozklady/tabliczka.jsp"
        table = TimeTableModel()._get(
            url,
            direction,
            lineName,
            timetableId,
            stopNumber,
        )
        return table


class Table:
    """
    A class for representing Time Table.
    ...
    Attributes
    ----------
    line : str
        Line Name.
    dir : str
        Direction.
    stop : str
       Stop Name.

    Methods
    -------
    repr():
    Prints the Timetable
    get():
    return the Time Table

    """
    def __init__(self, line, dir, stop):
        a = ()
        self.line = line
        self.dir = dir
        self.stop = stop
        self.table = TimeTableModel.get_bus_table(line, dir, stop)

    def repr(self):
        table = {}
        table["Linia"] = self.line
        table["Kierunek"] = self.dir
        table["Przystanek"] = self.stop

        for h, mins in self.table[self.line]["ROBOCZY"].items():
            table[h] = []
            for minute in mins:
                table[h].append(minute)
        return table

    def get(self):
        return self.table[self.line]["ROBOCZY"].items()
