import re
import urllib
from datetime import datetime
import requests
from bs4 import BeautifulSoup as soup
import pymongo

get_marvel_movie_page = requests.get("https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_films")
movie_file = soup(get_marvel_movie_page.content, "html.parser")
get_marvel_series_page = requests.get("https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_television_series")
series_file = soup(get_marvel_series_page.content, "html.parser")


def get_info_box(movie_title):
    r = requests.get(movie_title)
    myFile = soup(r.content, "html.parser")

    info_box = myFile.find("table", attrs={"class": "infobox vevent"})
    for tag in info_box("sup"):
        tag.decompose()

    table_headers = info_box.find_all("th", class_="infobox-label")
    table_header_data = info_box.find_all("td", class_="infobox-data")

    table_headers_list = [header.get_text(" ", strip=True) for header in table_headers]
    table_data_list = [data.get_text("\n", strip=True).replace("\xa0", " ") for data in table_header_data]

    table_headers_list.insert(0, "Title")
    table_data_list.insert(0, " ".join([text for text in myFile.find("th").stripped_strings]))
    for value in range(len(table_data_list)):
        if table_data_list[value].__contains__("\n"):
            table_data_list[value] = table_data_list[value].strip().split("\n")

    movies_info_list = {}
    for value in range(len(table_headers_list)):
        movies_info_list[table_headers_list[value]] = table_data_list[value]

    return movies_info_list


movie_table_elements = movie_file.select('.wikitable.plainrowheaders.defaultcenter th[scope="row"] i a')
series_table_elements = series_file.select('.wikitable.plainrowheaders th[scope="row"] i a')

wiki_url = "https://en.wikipedia.org"

movie_data_list = []
series_data_list = []


def get_info_box_data(table_elements, data_list):

    for name in range(len(table_elements)):
        try:
            movie_path = table_elements[name]['href']
            full_path = wiki_url + movie_path

            data_list.append(get_info_box(full_path))
        except Exception as e:
            print(table_elements[name].get_text())
            print(e)


get_info_box_data(movie_table_elements, movie_data_list)
get_info_box_data(series_table_elements, series_data_list)

unique_movie_values = {each['Title']: each for each in movie_data_list}.values()
unique_series_values = {each['Title']: each for each in series_data_list}.values()

movie_and_series_data = [name for name in unique_movie_values] + [data for data in unique_series_values]


def convert_date(date_column):
    try:
        return datetime.strptime(date_column[2], "%Y-%m-%d")
    except:
        return "N/A"


for name in movie_and_series_data:
    if 'Release date' in name:
        name["Release Date"] = convert_date(name['Release date'])
    elif 'Release dates' in name:
        name["Release Date"] = convert_date(name['Release dates'])
    elif 'Original release' in name:
        name['Release Date'] = convert_date(name['Original release'])
    else:
        name["Release Date"] = "N/A"

movie_and_series_data = [name for name in movie_and_series_data if type(name['Release Date']) is datetime]

for name in movie_and_series_data:
    if 'Original release' in name:
        del name['Original release']
    elif 'Release date' in name:
        del name['Release date']
    else:
        del name['Release dates']
    name['Release Date'] = name['Release Date'].strftime("%m/%d/%Y")
    name['Release Year'] = int(name['Release Date'][-4:])


def convert_to_numeric(data_object):
    if type(data_object) is list:
        if 'million' in data_object[0]:
            data_object = data_object[0]
        else:
            data_object = data_object[1]

    data_object = re.sub('^.*?\$|[-–—>]|to|est.|\(.*?\)', ' ', data_object)
    data_object = data_object.strip()
    if "million" in data_object:
        data_object = data_object.split(" ")[0].strip()
        data_object = data_object.split("million")[0].strip()
        try:
            return round(float(data_object) * 1000000, 0)
        except:
            return "N/A"

    elif "billion" in data_object:
        data_object = data_object.split("billion")[0]
        data_object = data_object.strip()
        try:
            return round(float(data_object) * 1000000000, 0)
        except:
            return 'N/A'
    else:
        return data_object.replace(",", "")


for name in movie_and_series_data:
    if ('Budget' in name) & ('Box office' in name):
        name['Budget (in USD)'] = convert_to_numeric(name['Budget'])
        name['Box office (in USD)'] = convert_to_numeric((name['Box office']))
    elif 'Budget' in name:
        name['Budget (in USD)'] = convert_to_numeric(name['Budget'])
        name['Box office (in USD)'] = 'N/A'
    elif 'Box office' in name:
        name['Box office (in USD)'] = convert_to_numeric(name['Box office'])
        name['Budget (in USD)'] = "N/A"
    else:
        name['Budget (in USD)'] = "N/A"
        name['Box office (in USD)'] = "N/A"


def extract_movie_info(movie_title):
    api_url = "http://www.omdbapi.com/?"
    api_extensions = {"apikey": "[api_key]", "t": movie_title}
    extensions_encoded = urllib.parse.urlencode(api_extensions)
    full_url = api_url + extensions_encoded
    return requests.get(full_url).json()


def extract_rotten_tomato_score(movie_info):
    ratings = movie_info.get('Ratings', [])
    for value in ratings:
        if value['Source'] == 'Rotten Tomatoes':
            return value['Value']
    return 'N/A'


for name in movie_and_series_data:
    movie_info = extract_movie_info(name['Title'])
    name['IMDb'] = movie_info.get("imdbRating", 'N/A')
    name['Metascore'] = movie_info.get("Metascore", "N/A")
    name['Rotten Tomatoes'] = extract_rotten_tomato_score(movie_info)


for name in movie_and_series_data:
    if name['IMDb'] == "N/A":
        continue
    else:
        name['IMDb'] = float(name['IMDb'])
    for value in name.values():
        if type(value) is list:
            for select in value:
                if select == ",":
                    value.remove(select)


client = pymongo.MongoClient("mongodb+srv://agundra001:[enviroment_variable]@pythonproject.v3r1sg2.mongodb.net/?retryWrites=true&w=majority")
disneyAndMarvelDatabase = client['DisneyAndMarvelDatabase']
marvel_collection = disneyAndMarvelDatabase['marvel_data']
marvel_collection.insert_many(movie_and_series_data)
