import unittest 
from unittest.mock import patch, Mock, PropertyMock


from main import filter_tickers

class TestFilterTickers(unittest.TestCase):
    def test_filter_tickers(self):
        tickers = filter_tickers()
        

        

if __name__ == '__main__':
    unittest.main()
