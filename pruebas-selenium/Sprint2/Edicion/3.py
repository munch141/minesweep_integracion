# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Form(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_form(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//ul[@id='exampleAccordion']/li[2]/a/span").click()
        time.sleep(5)

        driver.find_element_by_xpath("//span[contains(.,'Subida de archivo')]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li/div[1]/a[2]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li/div[3]/div/div[4]/div/input").send_keys("Hola Mundo")
        driver.find_element_by_link_text("Cerrar").click()


        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Título')]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[2]/div[1]/a[2]").click()
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[2]/div[3]/div/div[1]/div/div").send_keys("Prueba")
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[2]/div[3]/div/div[3]/div/input").send_keys("Hola Mundo")
        #driver.find_element_by_link_text("Cerrar").click()

        #driver.find_element_by_xpath("//span[contains(.,'Seleccionable')]").click()
        #driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[3]/div[1]/a[2]").click()
        #driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[3]/div[3]/div/div[9]/div/ol/li[1]/input[2]").send_keys("Hola")
        #driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[3]/div[3]/div/div[9]/div/ol/li[2]/input[2]").send_keys("que")
        #driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/ul/li[3]/div[3]/div/div[9]/div/ol/li[3]/input[2]").send_keys("tal")
        

        driver.find_element_by_xpath("//span[contains(.,'Botón')]").click()
    

        driver.find_element_by_xpath("//button[contains(.,'Guardar')]").click()

        '''
        

        
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Campo oculto')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[6]/div[1]/a[2]")

        
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Párrafo')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[7]/div[1]/a[2]")


        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Número')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[8]/div[1]/a[2]")


        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Grupo de Selección')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[9]/div[1]/a[2]")
 

        time.sleep(5)



        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Campo de Texto')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[11]/div[1]/a[2]")


        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'tinyMCE')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[12]/div[1]/a[2]")


        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Botón')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/ul/li[13]/div[1]/a[2]")



        driver.find_element_by_xpath("//button[contains(.,'Guardar')]").click()

        #print(driver.find_element_by_css_selector(".toggle-form"))
        #driver.find_elements_by_class_name('test_button4')
        '''
        time.sleep(10)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
