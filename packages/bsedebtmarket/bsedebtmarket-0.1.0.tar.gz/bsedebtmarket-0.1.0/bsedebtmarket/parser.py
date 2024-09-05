import http.client
from bs4 import BeautifulSoup
import json

def fetch_html():
    conn = http.client.HTTPSConnection("www.bseindia.com")
    payload, headers = '', {}
    conn.request("GET", "/markets/debt/tradereport.aspx", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data

def parse_table(html_content):
    soup = BeautifulSoup(html_content.decode("utf-8"), 'html.parser')

    table = soup.find('div', id='ContentPlaceHolder1_divCT1').find('table')

    headers = [header.get_text(strip=True) for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr')[2:]:
        cells = row.find_all('td')
        if len(cells) > 0: # Skipping Total
            row_data = {headers[i]: cell.get_text(strip=True) for i, cell in enumerate(cells)}
            rows.append(row_data)

    return rows

def table_to_json():
    html_content = fetch_html()
    data = parse_table(html_content)
    return json.dumps(data, indent=4)
