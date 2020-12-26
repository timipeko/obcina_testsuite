import unittest
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from urllib.parse import urlparse
 
 
class LinkTest(unittest.TestCase):
    
    def setUp(self):
        try:
            # Ensure existance of urls.txt
            if not os.path.exists("urls.txt"):
                print(f'Please provide an "urls.txt" file in working directory, containing the URLs to all tested pages.')
                sys.exit(-1)
 
            # Read all urls 
            urls_in = open('urls.txt', 'r')            
            self.pages_urls = urls_in.read().split('\n')
            urls_in.close()
 
            # Setup seen urls queue 
            self.seen_links = []
 
            # Array for storing unique URL types that denote specific page types
            self.seen_parts = [] 
 
            # Init web driver 
            self.driver = webdriver.Firefox()        
 
            # Flag for sucessful/failed unit test
            self.any_failed = False
 
            self.wait_timeout = 5
 
            self.driver.implicitly_wait(self.wait_timeout)
 
            self.base_url = ""
 
            self.err_counter = 0 
 
        except:
            print("Error in initialisation!")
            sys.exit(-1)
    
    
    def remove_duplicates(self, urls):        
        
        filtered = []
 
        #Filtering step
        for url in urls: 
            if not url is None and '/' in url: 
                ending = url.split("?")[0] if '?' in url else url
                if self.base_url in url and not ending in self.seen_parts: 
                    filtered.append(url)
                    self.seen_parts.append(ending)
                
        return filtered
 
 
 
 
    def process_url(self, url, depth=0, max_depth=4):       
 
        if 'uploads' in url: # Is a file, must skip
            return 
 
        if urlparse(url).netloc != urlparse(self.base_url).netloc: # Is other domain site
            return 
        
        if '#' in url: # Is empty link
            return 
 
        if 'stran' in url: # Is generic next page button
            return 
 
        driver = self.driver
 
        driver.get(url)
        if "Napaka" in driver.page_source: # An url failed 
            print(f"FAILED {url}: Error {driver.find_element(By.ID, 'errorCode').text} thrown on line {driver.find_element(By.ID, 'errorLine').text} of file {driver.find_element(By.ID, 'errorFile').text}")
            self.err_counter += 1 
            self.any_failed = True # Since an url failed, the generic test case will not be successful 
 
        else: 
            #print(f"OK {url}")
            link_elts = driver.find_elements_by_css_selector(".content-wrap a")
            urls = [link_el.get_attribute("href") for link_el in link_elts] # Find all links on page
 
            urls = self.remove_duplicates(urls)                   
 
            if depth < max_depth: # If max url depth not exceeded
                for link in urls: 
                    try:
                        #print(f'Handling url {link}.....')
                        if not link is None and link not in self.seen_links: # link on page has not been crawled yet 
                            self.seen_links.append(link)
                            if "inpis" in link: # Crawl only if is link on same domain..
                                self.process_url(link, depth+1, max_depth)
                    except StaleElementReferenceException as e1:                        
                        print(e1.msg)
                    except NoSuchElementException as e2: 
                        print(e2.msg)
 
    def test_link_crawler(self):                
        # Get all webpage urls that will be crawled and tested 
        for page_url in self.pages_urls:   
 
            self.err_counter = 0 # Reset error counter for this navbar link page        
 
            # For each web page, process all links from navbar
            print(f'Processing {page_url}....',end='')
            self.seen_links.append(page_url)
            self.driver.get(page_url)
 
            if "Napaka" in self.driver.page_source: # An url failed 
                print(f"FAILED {page_url}: Error {self.driver.find_element(By.ID, 'errorCode').text} thrown on line {self.driver.find_element(By.ID, 'errorLine').text} of file {self.driver.find_element(By.ID, 'errorFile').text}")
                self.any_failed = True # Since an url failed, the crawler test case will not be successful 
                self.err_counter+=1
            else:
                nav_links_xpath =  '//*[@id="wrapper"]/header//a[@href]'
                nav_links_elts = self.driver.find_elements_by_xpath(nav_links_xpath)
                nav_links_urls = [nav_link_elt.get_attribute("href") for nav_link_elt in nav_links_elts]
                for nav_links_url in nav_links_urls:                
                    if not nav_links_url in self.seen_links:
                        self.base_url = nav_links_url
                        self.process_url(nav_links_url)
                        self.seen_links.append(nav_links_url)
            
            if self.err_counter == 0: 
                print('OK!')
            else: 
                print(f'Failed with {self.err_counter} errors')
                    
            
 
        assert not self.any_failed, "URLs with errors exist!"
 
    def tearDown(self):
        self.driver.close()
 
if __name__ == "__main__":
<<<<<<< Updated upstream
    unittest.main()
=======
    try:
        unittest.main()
    except AssertionError as msg: 
        print(msg)
>>>>>>> Stashed changes
