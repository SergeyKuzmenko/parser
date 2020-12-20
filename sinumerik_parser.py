import requests
from bs4 import BeautifulSoup
import sqlite3

def get_html(url):
    print('get_html: {}'.format(url))
    r = requests.get(url)
    try:
        return r.text
    except Exception as e:
        print(e)

def get_current_page(html):
    print('get_current_page: Parsing current page')
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find("div", class_="entry-content").find_all("li")
    urls = []
    for title in content:
        urls.append(title.find('a').get('href'))
    return urls

def get_page_data(html):
    print('get_page_data: Parsing HTML')
    soup = BeautifulSoup(html, 'html.parser')
    
    AlarmId = int((soup.find("h1", class_="post-title").text).split(' ')[2].lstrip().rstrip())
    content = soup.find("div", class_="entry-content").find_all("p")
    AlarmName = (content[0].text.lstrip().rstrip())[7:]
    Description = " ".join(str(x) for x in content)

    print('Code: {}'.format(AlarmId))
    save_to_db(AlarmId, AlarmName, Description)

def connect_db():
    return sqlite3.connect('data.db')

def save_to_db(AlarmId, AlarmName, Description):
    print('DB: Save result')
    db = connect_db()
    db.cursor()
    db.execute('INSERT INTO sinumerik_errors (code, name, description) VALUES (?, ?, ?);', [AlarmId, AlarmName, Description])
    db.commit()
    db.close()
    print('Status: OK')

def main():

    for page in range(1, 3):
        url = f'http://www.helmancnc.com/sinumerik-840d-alarm-list/{page}/'
        html = get_html(url)
        current = get_current_page(html)
        for alarm in current:
            try:
                print('--- Start ---')
                html_page = get_html(alarm)
                alarm_text = get_page_data(html_page)
                print('--- Done ---')
            except AttributeError:
                continue

if __name__ == '__main__':
    main()