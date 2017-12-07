# -*- coding: utf-8 -*-
import unittest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class ControlFAQTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('%s%s' % (self.live_server_url, '/faqs/new/'))
        self.submit = self.driver.find_element_by_id("create")
        self.confirm_pregs = self.driver.find_element_by_id("check")
        self.add_more = self.driver.find_element_by_id("add_more")
        self.confirm_tema = self.driver.find_element_by_id("tema_check")

    def tearDown(self):
        self.driver.close()

class TestCamposVacios(ControlFAQTest):
    #@unittest.skip("Verificada")
    def runTest(self):
        self.confirm_pregs.click()
        self.submit.send_keys(Keys.RETURN)
        self.assertTrue(u"This field is required." in self.driver.page_source)

class TestRespuestaVacia(ControlFAQTest):
    #@unittest.skip("Verificada")
    def runTest(self):
        self.text_preg = self.driver.find_element_by_id("id_form-0-pregunta")
        self.text_preg.send_keys("Pregunta1?")
        self.confirm_pregs.click()
        self.submit.send_keys(Keys.RETURN)
        self.assertTrue(u"This field is required." in self.driver.page_source)

class TestPreguntaVacia(ControlFAQTest):
    #@unittest.skip("Verificada")
    def runTest(self):
        self.text_resp = self.driver.find_element_by_id("id_form-0-respuesta")
        self.text_resp.send_keys("Respuesta1")
        self.confirm_pregs.click()
        self.submit.send_keys(Keys.RETURN)
        self.assertTrue(u"This field is required." in self.driver.page_source)

class TestUnaPreguntaRespuesta(ControlFAQTest):
    #@unittest.skip("Verificada")
    def runTest(self):
        self.text_preg = self.driver.find_element_by_id("id_form-0-pregunta")
        self.text_resp = self.driver.find_element_by_id("id_form-0-respuesta")
        self.text_preg.send_keys("Pregunta1?")
        self.text_resp.send_keys("Respuesta1")
        self.confirm_pregs.click()
        self.submit.send_keys(Keys.RETURN)
        self.assertTrue(u"Pregunta1?" in self.driver.page_source)
        self.assertTrue(u"Respuesta1" in self.driver.page_source)

class TestUnaPreguntaRespuestaConTema(ControlFAQTest):
    #@unittest.skip("Verificada")
    def runTest(self):
        self.confirm_tema.click()
        self.driver.find_element_by_id("id_nombre").send_keys("Tema1")
        self.text_preg = self.driver.find_element_by_id("id_form-0-pregunta")
        self.text_resp = self.driver.find_element_by_id("id_form-0-respuesta")
        self.text_preg.send_keys("Pregunta1?")
        self.text_resp.send_keys("Respuesta1")
        self.confirm_pregs.click()
        self.submit.send_keys(Keys.RETURN)
        self.assertTrue(u"Pregunta1?" in self.driver.page_source)
        self.assertTrue(u"Respuesta1" in self.driver.page_source)
        self.assertTrue(u"Tema1" in self.driver.page_source)


#if __name__ == '__main__':
    #unittest.main()
