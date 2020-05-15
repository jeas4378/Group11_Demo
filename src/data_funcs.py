from plot_funcs import *
from API_Anrop import YEARS
from InformationLog import *

def sort_by_fst_lst(df, reverse = False):

    """
    Sort multiple lists based on a single list.
    """
    return zip(*sorted(zip(*df), key=lambda x:x[0], reverse=reverse))

def checkYearsOrder(year, years = YEARS):
    '''
    Accepts a year in the range specified in YEARS in the API_Anrop file.
    Returns a permutation of the years from YEARS in which order to look for data, including the given year.
    Prioritizes data closer to the given year, and rather more recent years than not.
    Example: If YEARS are "2016,2017,2018,2019" and input is 2018 the function returns [2018,2019,2017,2016].
    YEARS can be "unchoosen" with the years argument, for testing purposes.
    '''
    year = int(year)
    available_years = list(map(int,years.split(",")))
    if year not in available_years:
        return None

    orderOfChecks = [year]
    i = 1
    while (min(available_years) not in orderOfChecks) or (max(available_years) not in orderOfChecks):
        year += (-1)**(i+1) * i
        orderOfChecks.append(year)
        i += 1
    return [str(value) for value in orderOfChecks if value in available_years]

def get_data(keyword,given_year,infoLog,gender="T"):
    """
    Create data sets by collecting the
    specified data for all municipalities in Sweden.

    Arguments:
    keyword     -- Specifies which keyword
    given_year  -- The year that the data is retrieved from, if available.
    infoLog     -- An InformationLog instance, where user messages are saved.
    gender      -- If gender is omitted, this function returns the avarage.
                    Otherwise specify "K"/"M" to get avarage only for girls/boys.

    Returns a list of ints/floats, with None-values if data is missing for some municipalities (see infoLog for more information on which).
    If data is missing for all municipalities the given year, data from the closest available year is returned (see function checkYearsOrder
    for more information on which year will be shown). When this happens, it is documented in the InformationLog.
    Note that the municipalities' names aren't included, but since mdata is an ordered dictionary, the order of the list will always conform
    with the order which a 'for kommun in mdata.keys()'-clause iterates in.
    """

    def local_get_data(year):
        result = []
        for kommun in mdata.keys():
            result.append(get_single_data(keyword, year, infoLog, kommun=kommun, gender=gender))
        return result

    yearsToCheck = checkYearsOrder(given_year) #Skapar en ordning att leta efter data i.
    resLst = None
    if yearsToCheck:
        for year in yearsToCheck:
            infoLog.resetMissingMunis()
            try:
                resLst = local_get_data(year)
            except KeyError as e:
                infoLog.addInfo(missingData = (keyword,year))
                continue
            if resLst == [None] * len(resLst):
                infoLog.addInfo(missingData = (keyword,year))
                continue
            elif resLst and year == yearsToCheck[0]:
                break
            elif resLst:
                infoLog.addInfo(succeededYears = (keyword,year))
                break
    if not resLst:
        raise ValueError("Nyckeltalet" + str(keyword) + "verkar sakna data för alla år.")
    return resLst

def get_single_data(keyword, year, infoLog, kommun=None, gender = "T"):
    """
    Create data sets by collecting the
    specified data for a single municipality or all of Sweden.

    Arguments:
    keyword   -- Specifies which keyword
    year      -- The year that the data is retrieved from.
    infoLog   -- An InformationLog instance, where user messages are saved.
    kommun    -- If a municipality is omitted, this function returns the avarage of sweden.
    gender    -- If gender is omitted, this function returns the avarage.
                    Otherwise specify "K"/"M" to get avarage only for girls/boys.
    Returns int or float, and None if data is missing (see infoLog for more information).
    """
    if kommun:
        res = mdata[kommun][keyword][year][gender]
    else:
        res = riket_data[keyword][year][gender]
    if res:
        return res
    else:
        if kommun:
            infoLog.addInfo(missingMunis = kommun)
        else:
            pass
            # Bör inte krävas ett specifikt meddelande här - saknas rikssnitt saknas garanterat annat
            # så det löser sig själv
        return None


def calc_sekom_avg(keyword, year, given_kommun, infoLog, gender = "T"):
    """
    Calculates the avarage of the SEKOM group which given_kommun belongs to,
    given a specified year and keyword.
    Documents information in infoLog
    """

    total, kommuner = 0, 0
    sekomColor = sekom_data[given_kommun]
    for kommun,values in mdata.items():
        if sekom_data[kommun] == sekomColor:
            current_value = values[keyword][year][gender]
            if current_value:
                kommuner += 1
                total += float(current_value)

    try:
        res = round(total / kommuner, 1)
        infoLog.addInfo(sekomCol = sekomColor, actualQty = (keyword,kommuner), expectedTot = no_per_sekom(given_kommun), showSekomAvg = True)
        return res
    except ZeroDivisionError:
        # Kräver inget specifikt meddelande, visar aldrig enbart sekom-medel.
        return None

def get_comparison_list(keyword, given_year, kommun, infoLog):
    """
    Given a keyword, year and kommun, a list with three elements is returned.
    First element is the value for the municipality the given keyword and year
    Second element is the avarage for the SEKOM group which the municipality belongs to
    Third element is the avarage for all of Sweden

    If one, two or three values are missing, data from another year is returned, with the order
    from the checkYearsOrder-function.
    This is documented in the infoLog.
    """

    yearsToCheck = checkYearsOrder(given_year) #Skapar en ordning att leta efter data i.
    resLst = None
    for year in yearsToCheck:
        infoLog.resetMissingMunis()
        try:
            resLst = [  get_single_data(keyword, year, infoLog, kommun=kommun),
                        calc_sekom_avg(keyword, year, kommun, infoLog),
                        get_single_data(keyword, year, infoLog)]
        except KeyError as e:
            infoLog.addInfo(missingData = (keyword,year))
            continue
        if None in resLst:
            infoLog.addInfo(missingData = (keyword,year))
            continue
        elif resLst and year == yearsToCheck[0]:
            break
        elif resLst:
            infoLog.addInfo(succeededYears = (keyword,year))
            break
    if not resLst:
        raise ValueError("Nyckeltalet" + str(keyword) + "verkar sakna data för alla år.")
    return resLst


def get_all_municipalties():
    """
    Returns all municipalties in Sweden, sorted alphabetically
    """
    return [kommun for kommun in mdata.keys()]


def normalize_data(kommuner, data_x, data_y = None):
    """
    Given two or three lists, this function returns the same lists with None-values removed
    If data_x has a None value on index 10, the data on the same position in the other two
    lists are removed as well. Does not handle None-values in kommuner.
    Ex: [1,2,None,4] and ['a',None,'c','d'] as data_x and data_y respectively returns (..., [1,4], ['a','d'])
    """
    zippedData = zip(kommuner, data_x, data_y) if data_y else zip(kommuner, data_x, ['?']*290)
    cleanData = []
    for kommun, xVal, yVal in zippedData:
        if xVal is not None and yVal is not None:
            cleanData.append((kommun, xVal, yVal))
    kommuner, data_x, data_y = zip(*cleanData)
    if '?' in data_y:
        return (list(kommuner), list(data_x))
    else:
        return (list(kommuner), list(data_x), list(data_y))

def filter_on_SEKOM(given_kommun, kommuner, data_x, data_y = None):
    """
    Given a municipality and two or three lists, this function returns the same lists
    with only the corresponding values for the municipalties in the same SEKOM group as the given one.
    """
    zippedData = zip(kommuner, data_x, data_y) if data_y else zip(kommuner, data_x, ['?']*290)
    filteredData = []
    sekomColor = sekom_data[given_kommun]
    for kommun, xVal, yVal in zippedData:
        if sekom_data[kommun] == sekomColor:
            filteredData.append((kommun, xVal, yVal))

    kommuner, data_x, data_y = zip(*filteredData)
    if '?' in data_y:
        return (list(kommuner), list(data_x))
    else:
        return (list(kommuner), list(data_x), list(data_y))

def move_to_last(given_kommun, kommuner, data_x, data_y = None):
    """
    Given a municipality and two or three lists, this function returns the same lists
    but with the values corresponding the given municipaltiy moved to last.
    Precondition: lists are the same length.
    """
    oldIdx = kommuner.index(given_kommun)
    newIdx = len(kommuner) - 1
    allLsts = [kommuner, data_x, data_y] if data_y else [kommuner, data_x]
    for lst in allLsts:
        lst.insert(newIdx, lst.pop(oldIdx))

    if data_y:
        return (kommuner, data_x, data_y)
    else:
        return (kommuner, data_x)

def create_list_of_colors(kommuner, infoLog, std_col, hgl_col, kommun):
    """
    Creates a list of colors for data points.
    Will return a list of the same length as kommuner, consisting of the
    color std_col, given as a string with a HEX-value
    The corresponding position of kommun in kommuner
    is highlighted with the hgl_col, also given as a string with a HEX-value.
    """
    colors = [std_col]*len(kommuner)
    try:
        colors[kommuner.index(kommun)] = hgl_col
    except ValueError:
        if kommun is not None:
            infoLog.addInfo(missingMunis = kommun)
    return colors

def no_per_sekom(kommun):
    """
    Returns the number of municipalties in the SEKOM group which kommun belongs to.
    If kommun is not a valid name, an KeyError is raised.
    """
    res = 0
    correctCol = sekom_data[kommun]
    for k, color in sekom_data.items():
        if color == correctCol:
            res += 1
    return res

def round_values(*args):
    
    """
    Takes up to three lists containing floats and returns them rounded to the closest integer.
    """
    result = []

    for arg in args:
        #[0 if v is None else v for v in arg]
        if None not in arg:         #If there exists a None in args then the function will just return same value it got as an input
            result.append(list(map(round,list(map(lambda x: x + 0.001,arg)))))
        else:
            result.append(arg)
    if len(args) == 1:
        return tuple(result[0])
    else:
        return tuple(result)