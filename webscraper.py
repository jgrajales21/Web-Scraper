from selenium.webdriver.common.keys import Keys
from selenium import webdriver    
import os
from googlesearch import search
import webbrowser
import requests
import bs4
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def valid_input(x):
    '''
    signature: Str~> bool
    bools input; needed for input verifcation for g() function
    '''
    return x == 'A' or x == "B"

def valid_number(x):
    '''
    signature: any type
    bool statement confirms whether the number x is an integer
    '''
    return type(x) == int

def save_links(listoflinks):
    '''
    signature: list(urls) ~> none (saves to or pre-existing file)
    saves urls form search to an exsiting file or a pre-exsiitng one
    '''
    import os
    try:
        x = int(input('Would you like to save your links to:\n 1. A new file\n 2. A pre-exisitng one.\n 3. Do not save links.\n'))
        while x != 3:
            if x == 1:
                try:
                    y = input("Please enter a full path to directory. Note input format must be: 'C:\\Users\\Owner\\... ' ")
                    if os.path.isdir(y) == True:
                        f = open(y + '\\out_path.txt', 'x')
                        for links in listoflinks:
                            f.write(links + ' \n')
                        f.close()
                        print('Check' + y + ' for a file named out_path.text, your links are there!')
                        return 
                    else:
                        print(y  + "is not a valid path to a directory. Note input format must be: 'C:\\Users...\\out_path.text' ")
                        return
                except FileExistsError:
                    print('File already exists.')
            if x == 2:
                z = input("Enter a full path to the file you want to append links. Note input format must be: 'C:\\Users\\Owner\\...\\out_path.text' ")
                if os.path.isfile(z) == True:
                    f = open(z, 'a')
                    for links in listoflinks:
                        print(links)
                        f.write(links + ' \n')
                    f.close()
                    print('Links were added to' + z + '!')
                    return

                else:
                    print(z + "is not a valid path to a file.")
        return
    except ValueError:
        print('Please select one of the integers listed above.')
    return

def g():
    '''
    Searches through google search bar and opens up n number of tabs. The tabs opened are the most popular searches for the input given
    '''
    query = input("Enter your query: ")
    method = input("Would you like:\n A: A list of links\n B: Open Windows\n")
    
    
    if valid_input(method) == True:
        
        if method == "A" or method == 'a':
            n = int(input('How many links would you like to retrieve? Please enter an integer. '))
            if valid_number(n) == True:
                acc = []
                for i in search(query, tld = 'com', num = n , stop = n, pause = 2):
                    print(i)
                    acc.append(i)
                return save_links(acc)
            else:
                print('Please enter an integer. Try Again.')
                return
                

        if method == "B" or method == 'b':
            n = int(input('How many windows would you like to open? Please enter an integer. '))
            if valid_number(n) == True:
                for i in search(query, tld = 'com', lang = 'en', num = n , stop = n, pause = 2):
                    webbrowser.open(i)
            else:
                print('Please enter an integer. Try Again.')
                return
    else:
            print('Please eneter a "A" or "B". Try again.')
            return
        
def shvi(n):
    '''
    sig: str~> bool 
    checks that depth two inputs of main are valid
    '''
    return n == 'A' or n == 'B' or n == 'C' or n == 'D'

def arxlinks():
    '''
    retrieves all links from arx, number of pages deep == 0 only retrieves links from first page
    '''
    x = input("What would you like to search for on arx? ")
    y = int(input('How many pages deep? '))

    driver = webdriver.Chrome (executable_path = 'C:\Program Files (x86)\chromedriver.exe')
    driver.maximize_window()
    driver.get("https://arxiv.org/search/")

    search = driver.find_element_by_id('query') 
    search.send_keys(x)
    search.send_keys(Keys.RETURN)
    curl = str(driver.current_url)

    res = requests.get(curl) 
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    links = []
    for li in soup.find_all(class_='arxiv-result'):
        links.append(li.a.get('href'))

    try:
        i = 0
        while i != y:
            link = driver.find_element_by_link_text('Next')
            link.click()
            curl = str(driver.current_url)

            res = requests.get(curl) 
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            links = []
            for li in soup.find_all(class_='arxiv-result'):
                links.append(li.a.get('href'))
            i = i + 1
    except:
        return
        
    driver.quit()
    if len(links) == 0:
        print('Sorry, your query for all: ' + x + ' produced no results.')
    else:
        print(links)
        return save_links(links)

def biorx():
    '''
    retrieves links from biorx; "deep" works in the same fashion as in the arxlinks function
    '''
    
    x = input("What would you like to search for on bioRxiv? ")
    y = int(input('How many pages deep? '))
    
    driver = webdriver.Chrome (executable_path='C:\Program Files (x86)\chromedriver.exe')
    driver.maximize_window()
    driver.get("https://www.biorxiv.org/")

    search = driver.find_element_by_id('edit-keywords')
    search.send_keys(x)
    search.send_keys(Keys.RETURN)

    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main-content"))
        )
        elems = driver.find_elements_by_css_selector('[class="highwire-cite-linked-title"][href]')
        links = [elem.get_attribute('href') for elem in elems]
        
        
        try:
            i = 0
            while i != y:
                link = driver.find_element_by_link_text('Next')
                link.click()
                curl = str(driver.current_url)
                
                main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "main-content"))
                )
                elems = driver.find_elements_by_css_selector('[class="highwire-cite-linked-title"][href]')
                for elem in elems:
                    links.append(elem.get_attribute('href'))
                i = i + 1
        except:
            pass
        
    except:
        pass
    driver.quit()
    if len(links) == 0:
        print('Sorry, your query for all: ' + x + ' produced no results.')
    else:
        print(links)
        return save_links(links)

def gslinks():
    x = input("What would you like to search for on Google Scholar? ")#a3

    driver = webdriver.Chrome (executable_path = 'C:\Program Files (x86)\chromedriver.exe')
    driver.maximize_window()
    driver.get("https://scholar.google.com/") #a1

    search = driver.find_element_by_id('gs_hdr_tsi') #a2
    search.send_keys(x) 
    search.send_keys(Keys.RETURN)
    curl = str(driver.current_url)
    
    res = requests.get(curl) #a1
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    links = []
    for li in soup.find_all(class_='gs_r gs_or gs_scl'):#a4
        links.append(li.a.get('href'))

    driver.quit()
    if len(links) == 0:
        print('Sorry, your query for all: ' + x + ' produced no results.')
    else:
        print(links)
        return save_links(links)

def readabs(url):
    '''
    sig: str~> Nonetype
    reads the abstract for a given arx paper
    '''
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    lst = soup.select('blockquote')
    for i in lst:
        print(i.text)
    return
        

def opens(url):
    '''
    sig: str ~> NoneType
    opens the input url
    '''
    webbrowser.open(url)

def main():
    from googlesearch import search
    import webbrowser
    import requests
    import bs4
    try:
        x = int(input('Welcome! Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))
        if x == 1 or x == 2 or x == 5 or x == 3 or x == 4:
            while x != 5:
                if x == 1:
                    g()
                    x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                if x == 2:
                    y = input("Where would you like to search:\n A: ARXIV\n B: bioRx\n C: Google Scholar\n D. None\n")
                    if shvi(y) == True:
                        if y == 'A':
                            arxlinks()                              
                            x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                        if y == 'B':
                            biorx()
                            x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                        if y == 'C':
                            gslinks()
                            x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                        if y == 'D':
                            x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                    else:
                        print('Invalid input, please try again (case sensitive).')
                        return
                if x == 3:
                    y = input('Input the url of paper as given above. ')
                    readabs(y)
                    x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))        
                if x == 4:
                    y = input('Input the url you would like to open. ')
                    opens(y)
                    x = int(input('Please choose an action:\n 1. Search google\n 2. Personal Search\n 3. Read ARX abstract\n 4. Open link\n 5. Quit\n'))
            if x == 5:
                print("Thank You!")
                return
        else:
            print("Please select one of the numbers listed above.")
            return
    except ValueError:
        print('Please enter an valid integer')
