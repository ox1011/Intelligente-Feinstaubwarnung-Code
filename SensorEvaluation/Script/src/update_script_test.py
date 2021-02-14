import unittest
import json
import update_script

class UpdateScriptTest(unittest.TestCase):      
   
   # get_JSON_data tests
   def test_url_without_JSON(self):
      have = update_script.get_JSON_data("https://www.google.de")
      self.assertFalse(have)

   def test_url_with_parameter_none(self):
      have = update_script.get_JSON_data(None)
      self.assertFalse(have)

   def test_url_With_JSON(self): 
      data = update_script.get_JSON_data("http://api.luftdaten.info/static/v1/data.json") 
      have = ("" in data) or (type(data) == type(list()))
      self.assertTrue(have)

   # prepare_location_data tests
   def test_prepare_location_data_with_parameter_none(self):
      have = update_script.prepare_location_data(None)
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)

   def test_prepare_location_data_with_parameter_empty_string(self):
      have = update_script.prepare_location_data("")
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)

   def test_prepare_location_data_with_parameter_normal_string(self):
      have = update_script.prepare_location_data("Hello World")
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)

   # prepare_sensordatavalues_data tests
   def test_prepare_sensordatavalues_data_with_parameter_none(self):
      have = update_script.prepare_sensordatavalues_data(None)
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)

   def test_prepare_sensordatavalues_data_with_parameter_empty_string(self):
      have = update_script.prepare_sensordatavalues_data("")
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)

   def test_prepare_sensordatavalues_data_with_parameter_normal_string(self):
      have = update_script.prepare_sensordatavalues_data("Hello World")
      want = type(have) == type(list()) and (not have) 
      self.assertTrue(want)


if __name__ == "__main__":
    unittest.main()
