from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
import time
from PIL import Image
import requests

URL = 'https://www.peco-online.ro/'
browser = StatefulBrowser()

fuel_types = ['Benzina Standard', 'Motorina Standard',
              'Benzina Superioara', 'Motorina Superioara', 'GPL']
locations = ['sfantu gheorghe', 'miercurea ciuc',
             'brasov', 'cluj napoca',
             'covasna', 'targu secuiesc']
# main list to save all necessary data
fuel_info = None


def get_data_from_URL(URL):
    temp_fuel_info = list()
    temp_images = list()

    browser.open(URL)
    browser.select_form('form[name="display"]')
    browser['carburant'] = fuel_types[0]
    browser['nume_locatie'] = locations[0]
    response = browser.submit_selected()
    # now scrape the results
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', class_="float-left mt-1 mr-1")
    for image in images:
        src_value = image['src']
        #print(src_value)
        temp_images.append(src_value)
    temp_images = temp_images[1:]


    table = soup.find('table', id='tabelaRezultate')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        data = [col.text for col in cols]
        # print(data)
        # time.sleep(.2)
        temp_fuel_info.append(data)
    temp_fuel_info = temp_fuel_info[1:]

    return dict(zip(temp_images, temp_fuel_info))



fuel_info = get_data_from_URL(URL)

#print(fuel_info)
def save_svg(URL):
    iterator = iter(fuel_info.items())
    first_key, first_val = next(iterator)
    print("First-Key:",first_key)
    print("First-val:",first_val)
    URL = URL + first_key
    response = requests.get(URL)
    if response.status_code == 200:
        file_name = first_key.split("/")[-1]
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    print(URL)

    response = requests.get(URL)


save_svg(URL)
