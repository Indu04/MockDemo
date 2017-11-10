'''
Created on Sep 5, 2017

@author: jpi1
'''
import unittest
from mock import patch, MagicMock, Mock
# from person import Person
import person
# from per
import dataBase
from mock.mock import _return_values
from selenium.webdriver.remote.utils import return_value_if_exists

def local_mock_get_name():
        return "XYZ"

class testPerson(unittest.TestCase):

    @patch('person.Person.get_name', return_value="Bob")
    def test_name(self, mock_get_name):
#         mock_get_name.return_value = "Bob"
        p = person.Person()
        name = p.name()
        self.assertEqual(name, "Bob")
  
    def test_name_magic_mock(self):
        person.Person.get_name = MagicMock(return_value="testName")
        p = person.Person()
        name = p.name()
        self.assertEqual(name, "testName")

    @patch('person.Person.get_name', side_effect= local_mock_get_name)
    def test_name_side_effect(self, mock_get_name):
        p = person.Person()
        name = p.name()
        self.assertEqual(name, "XYZ")

if __name__ == '__main__':
    unittest.main()