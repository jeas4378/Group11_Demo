import requests
import json
import time

# Ändringsbara variabler (Om data för andra nyckeltal eller år vill hämtas, lägg till dessa i respektive textsträng):
# Programmet tar ~15-20 min att köra, körs bara vid ny inhämtning av data från kolada.

NYCKELTAL = "N15419,N15505,N15436,U15461,N15485,N15488,N15574,N15573,N15572,N15571,N15570,N15569,N15814,N15034,N15008,N15902,N15823,N15820"
YEARS = "2019,2018,2017,2016"


def write_json_to_file(Name, a_dict):
    """
    Converts a dict to JSON-format and writes to file.
    """

    json_format = json.dumps(a_dict)
    f = open(Name,"w",encoding="utf-8")
    f.write(json_format)
    f.close()


def link_municipalities_to_id():
    """
    Map municipalities against their corresponding ID-number on Kolada,
    and does the same for the whole country.
    """

    URL = "http://api.kolada.se/v2/municipality" 
    municipality_map = dict()
    kommun_info = requests.get(URL).json()

    for post in kommun_info["values"]:
        if post["type"] == "K":
            municipality_map[post["id"]] = post["title"]
        elif post["title"] == "Riket":
            country_id = post["id"]
    
    return municipality_map,country_id
    

def kolada_call_by_municipality(ID):
    """
    Collects data for the years and key values, for a single municipality.
    """

    URL = "http://api.kolada.se/v2/data/kpi/{}/municipality/{}/year/{}".format(NYCKELTAL,ID,YEARS)
    kommun_data = requests.get(URL).json()
    data = dict()

    for post in kommun_data["values"]:
        nyckeltal = post["kpi"]
        year = post['period']
        if nyckeltal not in data.keys():
            data[nyckeltal] = dict()
        
        data[nyckeltal][year] = dict()

        for item in post['values']:
            gender = item['gender']
            value = item['value']
            data[nyckeltal][year][gender] = value
    
    return data


def all_kolada_calls(ID_map,country_id):
    """
    Collects the data for all municipalites.
    """

    country_data = kolada_call_by_municipality(country_id)
    municipalities_data = dict()

    number_of_municipalities = len(ID_map)
    count = 0

    for muni_id, muni_name in ID_map.items():
        municipalities_data[muni_name] = kolada_call_by_municipality(muni_id)
        time.sleep(3)
        count +=1
        if (count % 10 == 0):
            print("{} kommuner utav {} hanterade.".format(count,number_of_municipalities))
    
    return country_data, municipalities_data

if __name__ == "__main__":

    # Datainhämtning

    Kommuner_ID, Riket_ID = link_municipalities_to_id()
    Riket_Data,Kommun_Data = all_kolada_calls(Kommuner_ID,Riket_ID)


    # Skriv den inhämtade och strukturerade datan till filer

    write_json_to_file("../data/MasterData.txt", Kommun_Data)
    write_json_to_file("../data/riket.txt", Riket_Data)
