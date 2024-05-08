from selenium.webdriver.common.by import By
from selenium import webdriver
# Importing libraries to send input to the text box
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# getting driver
cService = webdriver.ChromeService(executable_path='C:/Users/HP/Downloads/scraping/chromedriver.exe')
driver = webdriver.Chrome(service = cService)
driver.get('https://www.google.com/')

# Maximize the window
driver.maximize_window()

# Getting the input box by xpath
input_box = driver.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
input_box.send_keys('Hospitals in Bangalore')
input_box.send_keys(Keys.ENTER)
time.sleep(2)
driver.find_element('xpath', '/html/body/div[4]/div/div[13]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/h3/g-more-link/a/div/span[2]').click()
time.sleep(4)

lists = []
k = 0
for i in range(1, 12):
    try:
        k = k+1    
        prod_card = driver.find_elements(By.CLASS_NAME, 'rllt__details')
        a = 2 
        for j in prod_card:
            x = j.text.strip()
            lists.append(x.split('/n'))
        driver.find_element(By.ID, 'pnnext').click()
        print(k)
        time.sleep(3)
    except:
        pass

split_data = [item[0].split('\n') for item in lists]
split_data[0]
# Creating DataFrame
df = pd.DataFrame(split_data, columns=['Hospital_name', 'Rating', 'No_of_people_rated Type', 'Address', 'Timings phone', 'Highlighted_review'])


#Data Cleaning 
def splitting(x):
    original_string = x
    words = original_string.split()
    try:
        words.remove('·')
    except:
        pass
    return words

df['No_of_people_rated Type'] = df['No_of_people_rated Type'].apply(splitting)

def extract_values(row):
    values = row[1:-1].split(',')
    if len(values) == 1:
        return values[0], None
    else:
        return values[0], values[1]
df[['No_of_people_rated', 'Type']] = df['No_of_people_rated Type'].apply(lambda x: pd.Series([str(x).strip('[]').split(',')[0], str(x).strip('[]').split(',')[1] if len(str(x).strip('[]').split(',')) > 1 else None]))

def splitting_2(x):
    original_string = x
    if "·" in list(x):
        words = original_string.split('·')
        return words[-1]
    else:
        return original_string
    
def to_str(x):
    return str(x)

df['Timings phone'] = df['Timings phone'].apply(to_str)
df['Phone_number'] = df['Timings phone'].apply(splitting_2)
df.drop(['No_of_people_rated Type', 'Timings phone'], axis=1, inplace=True)
df = df[['Hospital_name', 'Rating', 'No_of_people_rated', 'Type', 'Address', 'Phone_number', 'Highlighted_review']]

df.to_csv('data_bangalore.csv')