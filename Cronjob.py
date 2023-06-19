import requests
from bs4 import BeautifulSoup
import csv
import os.path
import datetime

def get_data():
    url = "https://agriplus.in/price/onion/maharashtra/nashik/lasalgaon"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return data

def append_data(file_path, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Price Date', 'Variety', 'Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)'])
        writer.writerows(data)

def main():
    today = datetime.date.today().strftime("%d-%m-%Y")
    file_path = 'onions.csv'
    data = get_data()
    existing_data = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if today in row:
                    print('Data already exists for today')
                    return
                existing_data.append(row)
    data_to_append = [row for row in data if row not in existing_data]
    if data_to_append:
        append_data(file_path, data_to_append)
        print(f'Successfully appended {len(data_to_append)} rows to {file_path}')
    else:
        print('No new data to append')
        
if __name__ == '__main__':
    main()
