import re
import urllib
import pymongo
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
myFile = soup(r.content, "html.parser")


def get_info_box(url):
    r = requests.get(url)
    myFile = soup(r.content, "html.parser")
    info_box = myFile.find("table", attrs={"class":"infobox vevent"})
    for tag in info_box("sup"):
        tag.decompose()

    titles = info_box.find_all("td")
    headers = info_box.find_all("th")

    titles_list = [title.get_text("\n", strip=True).replace("\xa0", " ") for title in titles]
    titles_list[0] = "Title"
    for value in range(len(titles_list)):
        if titles_list[value].__contains__("\n"):
            titles_list[value] = titles_list[value].split("\n")

    headers_list = [header.get_text(" ", strip=True) for header in headers]
    movies_info = {}

    for value in range(len(headers_list)):
        if value == 0:
            movies_info[titles_list[value]] = headers_list[value]
        else:
            movies_info[headers_list[value]] = titles_list[value]

    return movies_info


table_elements = myFile.select(".wikitable.sortable i a")
wiki_url = "https://en.wikipedia.org"

info_box_list = []

for name in range(len(table_elements)):
    try:
        movie_path = table_elements[name]['href']
        full_path = wiki_url + movie_path

        info_box_list.append(get_info_box(full_path))
    except Exception as e:
        print(table_elements[name].get_text())
        print(e)


def convert_date(date_column):
    try:
        return datetime.strptime(date_column[2], "%Y-%m-%d")
    except:
        return "N/A"


for name in info_box_list:
    if 'Release date' in name:
        name["Release Date"] = convert_date(name['Release date'])
    elif 'Release dates' in name:
        name["Release Date"] = convert_date(name['Release dates'])
    else:
        name["Release Date"] = "N/A"

info_box_list = [name for name in info_box_list if type(name['Release Date']) is datetime]
unique_values = {each['Release Date']: each for each in info_box_list}.values()
info_box_list = [name for name in unique_values]


for name in info_box_list:
    if 'Release date' in name:
        del name['Release date']
    else:
        del name['Release dates']
    name['Release Date'] = name['Release Date'].strftime("%m/%d/%Y")
    name['Release Year'] = int(name['Release Date'][-4:])
    if 'Running time' in name:
        if type(name['Running time']) is list:
            name['Running time in mins'] = int(name['Running time'][0].split(" ")[0])
        else:
            name['Running time in mins'] = int(name['Running time'].split(" ")[0])
    else:
        name['Running time in mins'] = "N/A"


def convert_to_numeric(data_object):
    if type(data_object) is list:
        # data_object = data_object[0]
        if 'million' in data_object[0]:
            data_object = data_object[0]
        else:
            data_object = data_object[1]

    data_object = re.sub('^.*?\$|[-–—>]|to|est.|\(.*?\)', ' ', data_object)
    data_object = data_object.strip()
    if "million" in data_object:
        data_object = data_object.split(" ")[0].strip()
        data_object = data_object.split("million")[0].strip()
        # data_object = data_object.strip()
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


for name in info_box_list:
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
    api_extensions = {"apikey": "7b878af4", "t": movie_title}
    extensions_encoded = urllib.parse.urlencode(api_extensions)
    full_url = api_url + extensions_encoded
    return requests.get(full_url).json()


def extract_rotten_tomato_score(movie_info):
    ratings = movie_info.get('Ratings', [])
    for value in ratings:
        if value['Source'] == 'Rotten Tomatoes':
            return value['Value']
    return 'N/A'


for name in info_box_list:
    movie_info = extract_movie_info(name['Title'])
    name['IMDb'] = movie_info.get("imdbRating", 'N/A')
    name['Metascore'] = movie_info.get("Metascore", "N/A")
    name['Rotten Tomatoes'] = extract_rotten_tomato_score(movie_info)


for name in info_box_list:
    if 'Running time' in name:
        del name['Running time']
    if name['IMDb'] == "N/A":
        continue
    else:
        name['IMDb'] = float(name['IMDb'])
    for value in name.values():
        if type(value) is list:
            for select in value:
                if select == ",":
                    value.remove(select)

client = pymongo.MongoClient("mongodb+srv://agundra001:Final_Project_1@pythonproject.v3r1sg2.mongodb.net/?retryWrites=true&w=majority")
disneyAndMarvelDatabase = client['DisneyAndMarvelDatabase']
disney_collection = disneyAndMarvelDatabase['disney_data']
disney_collection.insert_many(info_box_list)










