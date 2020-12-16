import requests
from bs4 import BeautifulSoup
import sqlite3

def get_html(url):
	print('URL: {}'.format(url))
	headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
	r = requests.get(url, headers)
	return r.text

def get_page_data(html):
	print('SOUP: Parsing HTML')
	soup = BeautifulSoup(html, 'html.parser')
	content = soup.find("div", class_="entry-content").find_all("p")

	AlarmId = int(((content[0].text.lstrip().rstrip())[16:]).split(' ')[0])
	Alarm = (content[0].text.lstrip().rstrip())[16:]
	Description = " ".join(str(x) for x in content)

	print('Code: {}'.format(AlarmId))
	save_to_db(AlarmId, Alarm, Description)

def connect_db():
	return sqlite3.connect('data.db')

def save_to_db(AlarmId, Alarm, Description):
	print('DB: Save result')
	db = connect_db()
	db.cursor()
	db.execute('INSERT INTO sinumerik_errors (code, name, description) VALUES (?, ?, ?);', [AlarmId, Alarm, Description])
	db.commit()
	db.close()
	print('Status: OK')

def main():
	with open("AllLinks.txt", "r") as links:
		for link in links:
			try:
				print('--- Start ---')
				get_page_data(get_html(link.split(';')[0]))
				print('--- Done ---')
			except AttributeError:
				continue

if __name__ == '__main__':
	main()