"""
Unit tests for parser module
"""
import unittest
import pandas as pd
from src.parser import ChemicalDataParser

class TestChemicalDataParser(unittest.TestCase):
    """Test cases for ChemicalDataParser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = ChemicalDataParser()
    
    def test_is_element_symbol(self):
        """Test element symbol recognition"""
        # Valid elements
        self.assertTrue(self.parser.is_element_symbol('C'))
        self.assertTrue(self.parser.is_element_symbol('Fe'))
        self.assertTrue(self.parser.is_element_symbol('Mn'))
        
        # Invalid
        self.assertFalse(self.parser.is_element_symbol('ABC'))
        self.assertFalse(self.parser.is_element_symbol('123'))
    
    def test_parse_numeric_value(self):
        """Test numeric value parsing"""
        # Simple number
        value, unit = self.parser.parse_numeric_value('0.05')
        self.assertEqual(value, 0.05)
        
        # With unit
        value, unit = self.parser.parse_numeric_value('0.15 wt.%')
        self.assertEqual(value, 0.15)
        self.assertIn('%', unit)
        
        # Less than
        value, unit = self.parser.parse_numeric_value('<0.01')
        self.assertEqual(value, 0.01)
        
        # Balance
        value, unit = self.parser.parse_numeric_value('Balance')
        self.assertIsNone(value)
        self.assertEqual(unit, 'balance')
        
        # Trace
        value, unit = self.parser.parse_numeric_value('Trace')
        self.assertEqual(value, 0.001)
    
    def test_clean_ocr_text(self):
        """Test OCR text cleaning"""
        # Number context
        self.assertEqual(self.parser.clean_ocr_text('O.O5'), '0.05')
        self.assertEqual(self.parser.clean_ocr_text('l.23'), '1.23')
    
    def test_get_element_name(self):
        """Test element name lookup"""
        self.assertEqual(self.parser.get_element_name('C'), 'Carbon')
        self.assertEqual(self.parser.get_element_name('Fe'), 'Iron')
        self.assertEqual(self.parser.get_element_name('Mn'), 'Manganese')
        
        # Unknown element
        self.assertEqual(self.parser.get_element_name('XYZ'), 'XYZ')

if __name__ == '__main__':
    unittest.main()
