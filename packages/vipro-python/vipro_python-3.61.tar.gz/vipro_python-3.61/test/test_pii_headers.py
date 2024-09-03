# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

import unittest
import pandas as pd
from vipro_python.lacf.pii_headers import extract_postcode_from_address, extract_postcode_from_address_series

class ExtractPostcodes(unittest.TestCase):
  def testExtractPostcode(self):
    addr, pcode = extract_postcode_from_address('10 Cyber Road_x000D_Colchester_x000D_CO4 5NF')
    self.assertEqual(pcode, 'CO4 5NF')
    self.assertEqual(addr, '10 Cyber Road_x000D_Colchester_x000D_')

  def testExtractPostcodeSeries(self):
    s = pd.Series(data=['10 Cyber Road_x000D_Colchester_x000D_CO4 5NF'], index=['address_1'])
    df = pd.DataFrame([s])
    df[['address_1', 'postcode']] = df.apply(extract_postcode_from_address_series, axis=1)
    s = df.iloc[0]
    self.assertEqual(s['postcode'], 'CO4 5NF')
    self.assertEqual(s['address_1'], '10 Cyber Road_x000D_Colchester_x000D_')


class TestNoPostcode(unittest.TestCase):
    
    def testRaisesError(self):
      with self.assertRaises(Exception) as ctx:
        extract_postcode_from_address('10 Cyber Road_x000D_Colchester_x000D_')
        self.assertTrue('unable to extract postcode from address' in ctx.exception)

    def testDefaultsToEmptyPostcodeForSeries(self):
      s = pd.Series(data=['10 Cyber Road_x000D_Colchester_x000D_'], index=['address_1'])
      df = pd.DataFrame([s])
      df[['address_1', 'postcode']] = df.apply(extract_postcode_from_address_series, axis=1)
      df = df.dropna(subset=['postcode'])
      self.assertEqual(0, len(df), f'postcode should be empty so dropped, but is: {df.to_json()}')

    def testRaisesNoErrorWhenPrompted(self):
      extract_postcode_from_address('10 Cyber Road_x000D_Colchester_x000D_', False)
      self.assertTrue(True)
      