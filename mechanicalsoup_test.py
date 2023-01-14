from bs4 import BeautifulSoup
from mechanicalsoup import StatefulBrowser
from time import sleep
URL = 'https://www.peco-online.ro/'

browser = StatefulBrowser()
browser.open(URL)

#print(browser.page.find(id='carburant'))
browser.select_form('form[name="display"]')
#browser.form.print_summary()

browser['carburant'] = 'Motorina Standard'
browser['nume_locatie'] = 'sfantu gheorghe'
response = browser.submit_selected()

browser.launch_browser()

#browser['Submit']
print(response.text)

