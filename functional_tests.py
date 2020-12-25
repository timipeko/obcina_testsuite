import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class InvalidUrlTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_404_on_invalid(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        driver.get("http://test.zavrc.inpis.eu/invalid")
        assert "Napaka" in driver.page_source, "No error thrown on invalid URL"

    def test_valid_not404_on_valid(self):
        driver = self.driver
        driver.get("http://test.zavrc.inpis.eu/")
        try:
            assert "Napaka" not in driver.page_source
        except:
            code = driver.find_element(By.ID, 'errorCode').text
            line = driver.find_element(By.ID, 'errorLine').text
            file = driver.find_element(By.ID, 'errorFile').text
            print("Error "+code+" thrown on line "+line+" of file "+file)



    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()