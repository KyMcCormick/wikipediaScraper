import re
import requests
import math
import random
from bs4 import BeautifulSoup
from datetime import date

def getSiteData():
	# main driver. gets the site data using an html request. we then feed to process.

	facts_to_add = []
	current_date = getDate()
	requestor = requests.get(current_date)

	# code 200 means a successful connection an dreturn response from the page. if this fails we cannot go forward.
	if(requestor.status_code != 200):
		raise Exception("error creating a connection: Code " + requestor.status_code)
		
	facts_to_add = processData(requestor)
	return facts_to_add

def getDate():
	today = date.today()
	date_string = today.strftime("%B_%d")

	return "https://en.wikipedia.org/wiki/" + date_string

def getRandomEvents(event_list):
	# returns a number of events from the current section

	random_events = []

	if(len(event_list) < 3):
		num_events = len(event_list)
	else:
		num_events = 3

	for i in range(num_events):
		rand = random.randint(0, len(event_list) - 1)
		event = event_list[rand]
		event_list.pop(rand)
		random_events.append(event)

	return random_events

def processSection(event_string):
	# function to process wikipedia section, ie events, births, deaths, etc
	# takes the inputted string and splits into three lists for each subsection, pre1600, early modern period, and modern period
	# lists comprise of each li element from the original html in plain text form.
	events_chosen = []
	event_string = re.sub("\[[0-9]+\]", "", event_string)
	eras = event_string.split("[edit]")
	
	# converting raw data into list of events broken down by respective header from wikipedia page
	# -1 to ignore headers, list comp to remove "" members

	pre1600 = eras[1].split("\n")[:-1]
	pre1600 = [i for i in pre1600 if i] 
	
	early_modern = eras[2].split("\n")[:-1]
	early_modern = [i for i in early_modern if i]

	modern = eras[3].split("\n")[:-1]
	modern = [i for i in modern if i]

	events_chosen = events_chosen + getRandomEvents(pre1600) +  getRandomEvents(early_modern) + getRandomEvents(modern)
	return events_chosen

def processData(requestor):
	# Beautiful soup is an html parser/interpreter. We use that to pull all text out of the site 
	# and then check it into the sections we want from word x to word y where x and y are headers

	todays_events = []

	soup = BeautifulSoup(requestor.content, 'html.parser')
	text = soup.get_text()

	events = text.split("Events[edit]")[1].split("Births[edit]")[0]
	births = text.split("Births[edit]")[1].split("Deaths[edit]")[0]
	deaths = text.split("Deaths[edit]")[1].split("Holidays and observances[edit]")[0]

	todays_events = processSection(events)
	return todays_events
	
def main():
	
	html_path = "../../resumeSite/resumeSite/today.html"
	facts_to_add = getSiteData()
	html = BeautifulSoup(open(html_path), 'html.parser')
	li_elements = html.find_all('li')

	print(facts_to_add)

	for i in range(len(facts_to_add)):
		li_elements[i].string = facts_to_add[i]

	#for subsection in range(9):
		#facts_html = '\n'.join(['<li>'.rjust(8) + fact + '</li>' for fact in facts_to_add[subsection]])
		#print(facts_html + '\n')


	print(html.prettify())

	
	with open(html_path, "w", encoding = 'utf-8') as file:# prettify the soup object and convert it into a string
		file.write(str(html.prettify()))
	
if __name__ == "__main__":
	main()