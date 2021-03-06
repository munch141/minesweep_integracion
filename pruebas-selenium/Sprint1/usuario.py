# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Usuario(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_usuario(self):
        driver = self.driver
        driver.get(self.base_url + "/demo/")
        time.sleep(1)
        driver.find_element_by_id("actualizarCaptcha").click()
        time.sleep(1)
        driver.find_element_by_id("actualizarCaptcha").click()
        time.sleep(1)
        driver.find_element_by_id("actualizarCaptcha").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_id("reproducirAudio").click()
        time.sleep(3)
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        driver.find_element_by_id("exampleModal").click()
        driver.find_element_by_id("captcha-answer").clear()
        driver.find_element_by_id("captcha-answer").send_keys("e80M7K")
        driver.find_element_by_id("enviar").click()
        time.sleep(2)
        driver.find_element_by_id("actualizarCaptcha").click()
        driver.find_element_by_id("captcha-answer").clear()
        driver.find_element_by_id("captcha-answer").send_keys("P5ty05")
        driver.find_element_by_id("enviar").click()
        driver.find_element_by_id("actualizarCaptcha").click()
    
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
