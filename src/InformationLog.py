from collections import OrderedDict

class InformationLog():
    """docstring for InformationLog."""

    def __init__(self):
        """
        """
        self._alertLog = OrderedDict()
        self._alertLog["missingMunis"] = set()  # add municipalties as strings
        self._alertLog["missingData"] = {}      # of the form {"keyword1" : [year1, ...], "keyword2" : [year1, ...]}
        self._alertLog["succeededYears"] = {}    # of the form {"keyword1" : year, "keyword2" : year}
        self._alertLog["sekomCol"] = None       # expects string
        self._alertLog["actualQty"] = {}      # of the form {"keyword1" : int, "keyword2" : int}
        self._alertLog["expectedTot"] = 290     # expects int, preset to all 290 municipalties
        self._alertLog["showSekomAvg"] = False  # True or False

    def addInfo(self, **kwargs):
        """
        Specify any number of information as 'informationKey = info' like this:

        Argument:                           Will inform user of:
        missingMunis = "Municipality"       Which municipalties which aren't included in the plot
        missingData = ("keyword", year)     That all data for the keyword(s) and year(s) is missing
        succeededYears = ("keyword", year)   That data for the keyword(s) will be shown from year instead
        sekomCol = "Color"                  Which SEKOM group is shown/filtered
        actualQty = ("keyword", int)        The actual number of data points in the plot, per keyword
        expectedTot = int                   The expected number of data points in the plot
        showSekomAvg = bool                 if true - the number of municipalties which the avarage was calculated from

        if any other key is used, an IndexError is raised.
        """
        for key, value in kwargs.items():
            if key == "missingMunis":
                self._alertLog[key].add(value)
            elif key == "missingData":
                try:
                    keyword = value[0]
                    year = value[1]
                    self._alertLog[key][keyword].append(year)
                except TypeError or IndexError as e:
                    raise TypeError("Specify as tuple or list with two elements!")
                except KeyError as e:
                    self._alertLog[key][keyword] = [year]
            elif key == "succeededYears" or key == "actualQty":
                try:
                    keyword = value[0]
                    year = value[1]
                    self._alertLog[key][keyword] = year
                except TypeError as e:
                    raise TypeError("Specify as tuple or list with two elements!")
            elif key in ["sekomCol", "expectedTot"]:
                self._alertLog[key] = value
            elif key == "showSekomAvg":
                if value and (self._alertLog["sekomCol"] is None or len(self._alertLog["actualQty"]) == 0 or self._alertLog["expectedTot"] == 290):
                    raise ValueError('Please specify "sekomCol", "actualQty" and "expectedTot" before showSekomAvg')
                else:
                    self._alertLog[key] = value
            else:
                raise IndexError("Unknown information key:" + str(key) +". No logged data saved!")


    def informUser(self, *args, kommun = None):
        """
        Specify any number of information keys as strings, indicating what to write out.

        Argument:           Will print the following:
        missingMunis        Which municipalties which aren't included in the plot
        missingData         That all data for the keyword(s) and year(s) is missing
        succeededYears      That data for the keyword(s) will be shown from year instead
        sekomCol            Which SEKOM group is shown/filtered
        actualQty           The actual number of data points in the plot
        expectedTot         The expected number of data points in the plot - requires actualQty for anything to happen
        showSekomAvg        Requires that sekomCol, actualQty and expectedTot have been changed with addInfo.
                            Removes what they write out, instead shows how many municipalties the avarage was calculated from.
                            If several keys in the actualQty, these are stated directly after one and another.

        If kommun is anything but None or False, the function looks for the given string in missingMunis,
        and writes out information for only this municipality. If not found, nothing is written.
        If kommun is None, no elements in the list missingMunis are listed.
        If kommun is False, all elements in the list missingMunis are listed.

        If any other key is used, an IndexError is raised.

        It is recommended to always specify missingData and succeededYears together.
        It is recommended to always specify actualQty and expectedTot together.
        Specify the keywords in the order which you'd like the messages to appear.
        """
        for infoKey in args:
            if infoKey == "missingMunis":
                if kommun in self._alertLog[infoKey]:
                    # skriver bara ut för den kommunen
                    print("Data saknas för kommunen %s." % kommun)
                elif kommun is False:
                    # är ingen kommun given skrivs alla ut - men bara om missingMunis är specifierat.
                    print("Data saknas för kommunerna", ", ".join(str(x) for x in self._alertLog[infoKey]) + ".")
            elif infoKey == "missingData":
                # gör inget om ingen data lagts till här - allt har gått som det ska
                if len(self._alertLog[infoKey]) != 0:
                    for keyword,years in self._alertLog[infoKey].items():
                        print("Relevant data saknas för nyckeltalet", keyword, "år", ", ".join(str(x) for x in years) + ".")
            elif infoKey == "succeededYears":
                # gör inget om ingen data lagts till här - allt har gått som det ska
                if len(self._alertLog[infoKey]) != 0:
                    for keyword,year in self._alertLog[infoKey].items():
                        print("Visar istället data för nyckeltalet %s år %s." % (keyword, year))
            elif infoKey == "sekomCol" and "showSekomAvg" not in args:
                if self._alertLog[infoKey] is not None:
                    print("Visar kommuner från %s kommungrupp." % self._alertLog[infoKey])
            elif infoKey == "actualQty" and "expectedTot" not in args:
                for value in self._alertLog[infoKey].values():
                    print("Visar data från %s kommuner." % value)
            elif infoKey == "actualQty" and "expectedTot" in args:
                for value in self._alertLog[infoKey].values():
                    print("Visar data från %s av %s kommuner." % (value, self._alertLog["expectedTot"]))
            elif infoKey == "expectedTot":
                pass
            elif infoKey == "showSekomAvg":
                for keyword, value in self._alertLog["actualQty"].items():
                    print("Oviktat medelvärde för nyckeltal %s i %s kommungrupp baserat på data från %s av %s kommuner."
                        % (keyword,self._alertLog["sekomCol"], value,self._alertLog["expectedTot"]))
            else:
                raise IndexError("Unknown information key: %s. See documentation." % infoKey)

    def resetMissingMunis(self):
        """
        Resets the set of missing municipalities
        """
        self._alertLog["missingMunis"] = set()

    def reset(self):
        self.__init__()
