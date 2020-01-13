
# coding: utf-8

# In[1]:

"""Importing Libraries"""

import requests #allows to send HTTP requests
from urllib.request import urlopen #open up the url
from bs4 import BeautifulSoup #web scraping library
import pandas as pd
import calendar
import dateutil.parser as parser


# In[2]:

"""Get the data and create the bs4 object"""

def get_data(url):
    #url = "https://en.wikipedia.org/wiki/2019_in_spaceflight" #link to the required wiki page
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser') #create the beautifulsoup object with html content and html parser
    return soup


# In[3]:

"""Inspecting the web-page and Extracting the number of orbital luanches"""

def extract(soup):
    my_table = soup.find('table',{'class':'wikitable collapsible'}) #after inspection
    table_rows = my_table.find_all('tr')

    result = {}
    acceptable_status = ['operational', 'successful', 'en route']
    i = 4 #since we are interested with data from the 4th row of the table
    while i < len(table_rows):
        row = table_rows[i].find_all('td')
        row_len = len(row)
        if row_len == 5 or row_len == 6: #rows with date and outcome
            try:
                num_payloads = int(row[0]['rowspan'])-1
                date = row[0].find('span').next #text and excluding those reference links
                j=i+1
                while j <= (num_payloads+i):
                    row = table_rows[j].find_all('td')
                    row_len = len(row) 
                    if row_len == 5 or row_len == 6:
                        status = ((row[-1].text)[:-1]).lower() #extract status
                        if status in acceptable_status:
                            result[date] = result.get(date,0)+1
                            break
                    j+=1
                i+=(num_payloads)
            except Exception as e:
                print(row)
        i+=1
    return result


# In[4]:

"""Dictionary for all dates of 2019"""

def create_date_dict():
    my_dict = {}
    num_month = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 
                9:'September', 10:'October', 11:'November', 12:'December'}

    for month in range(1, 13):
        last_date = calendar.monthrange(2019, month)[1]
        for i in range(1,last_date+1):
            my_dict[str(i)+" "+num_month[month]] = 0
    return my_dict


# In[5]:

def final(my_dict, result):

    """Update the result(final) dictionary"""

    df = pd.DataFrame(columns=['date', 'value'])
    for key in my_dict.keys():
        if key in result.keys():
            my_dict[key] = result[key]

    """Create the dataframe and use ISO format"""

    for key, value in my_dict.items():
        text = key + ' 2019 00:00:00 +0000'
        date = parser.parse(text)
        df = df.append({'date': date.isoformat(), 'value': value}, ignore_index=True)

    """Convert dataframe to .csv file"""

    df.to_csv('final.csv', index=False)


# In[6]:

def main():
    url = "https://en.wikipedia.org/wiki/2019_in_spaceflight" #link to the required wiki page
    soup = get_data(url)
    
    result = extract(soup)
    
    my_dict = create_date_dict()
    final(my_dict, result)


# In[7]:

main()

